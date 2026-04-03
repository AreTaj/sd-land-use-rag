# San Diego Land Use RAG

A Retrieval-Augmented Generation (RAG) system designed to provide intelligent querying and analysis of the San Diego Municipal Code (Land Development Code). This project implements a multi-stage data pipeline that automates ingestion, structured parsing, and exploratory analysis of municipal documents in preparation for a production AI retrieval system.

## Project Structure

- `sd_land_use/`: Core Python package containing ingestion and processing logic.
  - `ingest.py`: CLI tool for downloading Municipal Code chapters as PDFs.
- `data/`: Local storage for raw and processed documents (directory is Git-ignored).
- `notebooks/`: Stage-based notebooks for document processing and RAG development.
  - `01_raw_pdf_inspection.ipynb`: Preliminary audit identifying layout complexity and OCR needs.
  - `02_document_parsing.ipynb`: Extracts structured text and metadata from PDFs.
  - `03_parsed_data_eda.ipynb`: Empirical analysis of the parsed records for RAG fitness.
  - `04_data_cleaning_and_chunking.ipynb`: Semantic text cleaning and citation-aware chunking.
  - `05_vector_store_ingestion.ipynb`: Embeddings generation and ChromaDB persistence.
  - `06_advanced_retrieval_enhancement.ipynb`: Implementation of Hybrid Search and Neural Reranking.
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

### Stage 1: Ingesting & Auditing Data

The `ingest.py` script identifies and downloads Division PDFs for specific chapters of the San Diego Municipal Code. Run `notebooks/01_raw_pdf_inspection.ipynb` to audit these files for layout and OCR requirements.

**Download target chapters:**
```bash
python3 sd_land_use/ingest.py --chapters 11 12 13 14 15
```

### Stage 2: Parsing Documents

Run `notebooks/02_document_parsing.ipynb` to extract structured text and metadata from the downloaded PDFs. Output is written to `data/processed/parsed_records.jsonl`.

### Stage 3: Exploratory Data Analysis

Run `notebooks/03_parsed_data_eda.ipynb` to analyze records for data quality and citation density, informing the cleaning strategy.

### Stage 4: Cleaning & Chunking

Run `notebooks/04_data_cleaning_and_chunking.ipynb` to remove noise, normalize legal identifiers, and segment text into overlapping chunks that preserve citation context.

### Stage 5: Vector Store Ingestion

Run `notebooks/05_vector_store_ingestion.ipynb` to generate embeddings for the semantic chunks and initialize a persistent ChromaDB vector store.

### Stage 6: Advanced Retrieval Enhancement

Run `notebooks/06_advanced_retrieval_enhancement.ipynb` to transition to a professional two-stage pipeline:
1. **Hybrid Search**: Merging Neural (Semantic) and BM25 (Keyword) results via Reciprocal Rank Fusion.
2. **Neural Reranking**: Utilizing a Cross-Encoder to validate and re-sort candidates for maximum precision.

### Stage 7: Domain-Specific Fine-Tuning

Adapted the `legal-bert-base-uncased` encoder using Masked Language Modeling (MLM) on the San Diego Municipal Code corpus via Google Colab.
*   **Result**: Achieved a final evaluation loss of **0.6786** and a perplexity of **1.9712**.
*   **Artifacts**: Fine-tuned weights are stored locally in `models/san_diego_legal_bert` and backed up to Google Drive.

## Data Source

The data is sourced from the [San Diego City Clerk Official Municipal Code](https://www.sandiego.gov/city-clerk/officialdocs/municipal-code).

## Ethical Scraping Note

This project uses a polite `User-Agent` and respect-based delays to ensure it does not overwhelm the city's servers. It is intended for academic research purposes.