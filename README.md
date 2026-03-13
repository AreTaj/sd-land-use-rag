# San Diego Land Use RAG

A Retrieval-Augmented Generation (RAG) system designed to provide intelligent querying and analysis of the San Diego Municipal Code (Land Development Code). This project implements a multi-stage data pipeline that automates ingestion, structured parsing, and exploratory analysis of municipal documents in preparation for a production AI retrieval system.

## Project Structure

- `sd_land_use/`: Core Python package containing ingestion and processing logic.
  - `ingest.py`: CLI tool for downloading Municipal Code chapters as PDFs.
- `data/`: Local storage for raw and processed documents (directory is Git-ignored).
- `notebooks/`: Stage-based notebooks for document processing and RAG development.
  - `01_data_ingestion.ipynb`: Validates downloaded PDFs and documents the ingestion result.
  - `02_document_parsing.ipynb`: Extracts structured text and metadata from PDFs into a JSONL record file.
  - `03_parsed_data_eda.ipynb`: Empirical analysis of the parsed records for data quality, noise characterization, and RAG fitness.
- `tests/`: Diagnostic and unit tests.

## Getting Started

### Prerequisites

- Python 3.10+
- Virtual Environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AreTaj/sd-land-use-rag.git
   cd sd-land-use-rag
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Stage 1: Ingesting Data

The `ingest.py` script identifies and downloads Division PDFs for specific chapters of the San Diego Municipal Code. It includes built-in handling for pagination and polite scraping delays.

**Download specific chapters (e.g., Chapters 11 and 14):**
```bash
python3 sd_land_use/ingest.py --chapters 11 14
```

**Download all target chapters (11-15):**
```bash
python3 sd_land_use/ingest.py
```

### Stage 2: Parsing Documents

Run `notebooks/02_document_parsing.ipynb` to extract structured text and metadata from the downloaded PDFs. Output is written to `data/processed/parsed_records.jsonl`.

### Stage 3: Exploratory Data Analysis

Run `notebooks/03_parsed_data_eda.ipynb` to analyze the parsed records for data quality, noise characterization, symbol distribution, citation density, and structural element relationships. Results inform the cleaning and chunking strategy for vector store ingestion.

## Data Source

The data is sourced from the [San Diego City Clerk Official Municipal Code](https://www.sandiego.gov/city-clerk/officialdocs/municipal-code).

## Ethical Scraping Note

This project uses a polite `User-Agent` and respect-based delays to ensure it does not overwhelm the city's servers. It is intended for academic research purposes.