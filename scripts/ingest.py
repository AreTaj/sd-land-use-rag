import os
import requests
from bs4 import BeautifulSoup
import time
import logging
import re
import json
import argparse
from urllib.parse import urljoin
import urllib3

# Suppress insecure request warnings for verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.sandiego.gov/city-clerk/officialdocs/municipal-code"
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
DEFAULT_CHAPTERS = [11, 12, 13, 14, 15]

# A polite, descriptive User-Agent for academic research scraping
HEADERS = {
    'User-Agent': 'SDLandUseRAGBot/1.0 (Academic Research; +https://github.com/AreTaj/sd-land-use-rag)'
}

PDF_PATTERN = re.compile(r'Ch(\d{2})Art(\d{2})Division(\d{2})\.pdf', re.IGNORECASE)

def get_pdf_links(chapter):
    """Crawl the chapter landing page (and subsequent pages) and extract validated Division PDF links."""
    chapter_url = f"{BASE_URL}/chapter-{chapter}"
    links_to_visit = [chapter_url]
    visited_urls = set()
    valid_links = []
    
    while links_to_visit:
        current_url = links_to_visit.pop(0)
        if current_url in visited_urls:
            continue
        
        logger.info(f"Crawling: {current_url}")
        visited_urls.add(current_url)
        
        try:
            response = requests.get(current_url, headers=HEADERS, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve page {current_url}: {e}")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for PDF links
        for link in soup.find_all('a', href=True):
            href = link['href']
            match = PDF_PATTERN.search(href)
            if match:
                # Reconstruct absolute URL to docs.sandiego.gov
                absolute_url = urljoin("https://docs.sandiego.gov", href)
                # Verify the PDF belongs to the target chapter (prevents downloading 
                # cross-referenced links to other chapters that might appear on the page)
                if int(match.group(1)) == chapter:
                    valid_links.append((absolute_url, match.group(1), match.group(2), match.group(3)))
            
            # Look for pagination links (usually have ?page=X)
            if "page=" in href:
                full_pagination_url = urljoin(current_url, href)
                if full_pagination_url not in visited_urls:
                    links_to_visit.append(full_pagination_url)

    # Deduplicate links using a dictionary comprehension keyed by absolute URL
    # This ensures we don't return the same PDF multiple times if it was linked twice on the page
    unique_links = list({v[0]:v for v in valid_links}.values())
    return sorted(unique_links, key=lambda x: (x[1], x[2], x[3]))

def download_pdf(url, chapter, article, division):
    """Download a single PDF and save it to the data/raw/chapter_XX folder."""
    filename = f"Ch{chapter}Art{article}Division{division}.pdf"
    chapter_folder = os.path.join(DATA_DIR, f"chapter_{int(chapter)}")
    os.makedirs(chapter_folder, exist_ok=True)
    
    filepath = os.path.join(chapter_folder, filename)
    
    if os.path.exists(filepath):
        logger.info(f"Skipping {filename}, already exists.")
        return True
        
    logger.info(f"Downloading {filename}...")
    try:
        # We use verify=False because the docs.sandiego.gov subdomain often 
        # lacks a full certificate chain recognized by local Python environments, 
        # leading to SSLCertVerificationError.
        response = requests.get(url, stream=True, headers=HEADERS, timeout=20, verify=False)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
        
    except Exception as e:
        logger.error(f"Failed to download {filename}: {e}")
        return False

def main():
    """
    Main entry point for the ingestion script.
    
    Parses command-line arguments to determine which chapters to download,
    orchestrates the crawling of the Municipal Code website, and manages
    the downloading and saving of PDF files while enforcing respectful delays.
    """
    parser = argparse.ArgumentParser(description="San Diego Municipal Code Ingestion Tool")
    parser.add_argument(
        '--chapters', 
        type=int, 
        nargs='+', 
        default=DEFAULT_CHAPTERS,
        help='Specific chapters to download (e.g., --chapters 11 14). Defaults to 11-15.'
    )
    args = parser.parse_args()

    logger.info(f"Target Chapters: {args.chapters}")
    
    for chapter in args.chapters:
        links_data = get_pdf_links(chapter)
        logger.info(f"Found {len(links_data)} total divisions for Chapter {chapter} after following pagination.")
        
        for url, ch, art, div in links_data:
            success = download_pdf(url, ch, art, div)
            if success:
                time.sleep(1) # Polite delay
            
    logger.info("Ingestion complete.")

if __name__ == "__main__":
    main()
