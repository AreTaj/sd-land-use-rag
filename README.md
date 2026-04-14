# San Diego Land Use RAG

-- Project Status: [Completed]

## Project Intro/Objective

The main purpose of this project is to build a Retrieval-Augmented Generation (RAG) system designed to provide intelligent querying and analysis of the San Diego Municipal Code (Land Development Code). This project implements a complete 10-stage pipeline spanning document ingestion, domain-adapted model fine-tuning, and rigorous end-to-end evaluation of both retrieval precision and generative quality. The goal is to make complex municipal zoning and land use regulations highly accessible to urban planners, developers, and researchers.

## Methods Used
*   Natural Language Processing (NLP)
*   Machine Learning (Domain Adaptation)
*   Deep Learning (Contrastive Fine-Tuning)
*   Data Manipulation & Cleaning
*   Information Retrieval (Hybrid Search & Reranking)
*   Generative AI (LLM Evaluation)

## Technologies
*   Python
*   HuggingFace Transformers (PyTorch)
*   ChromaDB
*   Ollama (Phi-4)
*   Jupyter Notebooks / Google Colab
*   Git / GitHub

## Project Description

This project focuses on the intricate domain of San Diego land development regulations. We utilized the raw PDF documents from the San Diego Municipal Code (specifically chapters 11-15, focusing on land development). The dataset was processed from unstructured text into thousands of semantic chunks, enriched with hierarchical metadata. Key hypotheses explored include demonstrating that domain-specific contrastive fine-tuning of an existing legal language model (Legal-BERT) significantly outperforms generic dense retrievers in specialized zoning-law queries. Our analysis included statistical benchmarking of retrieval hit rates and LLM-as-a-judge evaluation of generative faithfulness. The primary technical roadblock was overcoming embedding anisotropy (representation collapse) during the initial Masked Language Modeling phase, which we successfully addressed using MultipleNegativesRankingLoss on a synthetic ground truth validation set.

## Project Structure

- `scripts/`: Standalone utilities for data ingestion and system evaluation.
  - `ingest.py`: CLI tool for downloading Municipal Code chapters as PDFs.
  - `display_demo.py`: Terminal-based visualization of RAG performance.
  - `original_comparison_metrics.py`: Evidence script for verifying representation collapse.
- `data/`: Local storage for raw and processed documents (directory is Git-ignored).
- `notebooks/`: Stage-based notebooks for document processing and RAG development.
  - `01_raw_pdf_inspection.ipynb`: Preliminary audit identifying layout complexity and OCR needs.
  - `02_document_parsing.ipynb`: Extracts structured text and metadata from PDFs.
  - `03_parsed_data_eda.ipynb`: Empirical analysis of the parsed records for RAG fitness.
  - `04_data_cleaning_and_chunking.ipynb`: Semantic text cleaning and citation-aware chunking.
  - `05_vector_store_ingestion.ipynb`: Embeddings generation and ChromaDB persistence.
  - `06_advanced_retrieval_enhancement.ipynb`: Implementation of Hybrid Search and Neural Reranking.
  - `07_finetuning_domain_adaptation.ipynb`: MLM-based domain adaptation of Legal-BERT (Colab).
  - `07b_contrastive_finetuning.ipynb`: Contrastive fine-tuning for dense retrieval.
  - `08_eval_data.ipynb`: Synthetic ground truth generation via Ollama/Phi-4 (Colab).
  - `09_comparative_retrieval_benchmarking.ipynb`: Statistical benchmarking of retrieval architectures.
  - `10_generative_evaluation.ipynb`: End-to-end generative evaluation with ROUGE-L, BERTScore, and Faithfulness (Colab).
- `models/`: Fine-tuned model weights (directory is Git-ignored).
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

### Stage 1: Ingesting and Auditing Data
The `ingest.py` CLI tool identifies and downloads Division PDFs for specific chapters of the San Diego Municipal Code. The accompanying notebook (`01_raw_pdf_inspection.ipynb`) audits these files for layout complexity and OCR requirements.

**Download target chapters:**
```bash
python3 scripts/ingest.py --chapters 11 12 13 14 15
```

### Stage 2: Document Parsing
The `02_document_parsing.ipynb` notebook extracts structured text and metadata from the downloaded PDFs. Output is written to `data/processed/parsed_records.jsonl`.

### Stage 3: Exploratory Data Analysis
The `03_parsed_data_eda.ipynb` notebook analyzes parsed records for data quality and citation density, informing the downstream cleaning strategy.

### Stage 4: Cleaning and Chunking
The `04_data_cleaning_and_chunking.ipynb` notebook removes noise, normalizes legal identifiers, and segments text into overlapping chunks that preserve citation context.

### Stage 5: Vector Store Ingestion
The `05_vector_store_ingestion.ipynb` notebook generates embeddings for the semantic chunks and persists them to a ChromaDB vector store.

### Stage 6: Advanced Retrieval Enhancement
The `06_advanced_retrieval_enhancement.ipynb` notebook implements a professional two-stage retrieval pipeline:
1. **Hybrid Search**: Merging Neural (Semantic) and BM25 (Keyword) results via Reciprocal Rank Fusion.
2. **Neural Reranking**: Utilizing a Cross-Encoder to validate and re-sort candidates for maximum precision.

### Stage 7: Domain-Specific Fine-Tuning
The `07_finetuning_domain_adaptation.ipynb` notebook adapts the `legal-bert-base-uncased` encoder using Masked Language Modeling (MLM) on the San Diego Municipal Code corpus via Google Colab.
* Achieved a final evaluation loss of **0.6786** and a perplexity of **1.9712**.

### Stage 7b: Contrastive Dense Fine-Tuning
The `07b_contrastive_finetuning.ipynb` notebook addresses the embedding anisotropy problem by fine-tuning the MLM-adapted model using **MultipleNegativesRankingLoss**. The model is trained specifically to map semantic queries to legal document chunks using the 50-query synthetic ground truth dataset.

### Stage 8: Synthetic Evaluation Data Generation
The `08_eval_data.ipynb` notebook implements a high-fidelity data generation pipeline using **Ollama** and the **Phi-4 Mini** model. A total of 50 complex, user-centric queries are synthetically generated and mapped to substantive (>150 char) legal document chunks to establish a Ground Truth dataset for benchmarking.
*   **Framework**: Native Google Colab execution with local unthrottled inference.

### Stage 9: Comparative Retrieval Benchmarking
The `09_comparative_retrieval_benchmarking.ipynb` notebook conducts a rigorous statistical evaluation of three distinct retrieval architectures against the synthetic ground truth:
1.  **Lexical (BM25)**: Baseline keyword search.
2.  **Generic Neural (MiniLM)**: Out-of-the-box contrastive embeddings.
3.  **Domain-Adapted Neural (Fine-Tuned Legal-BERT)**: Custom contrastive retriever.

| Metric | BM25 | MiniLM (Base) | **Legal-BERT (Custom)** |
| :--- | :--- | :--- | :--- |
| **Mean Reciprocal Rank (MRR)** | 0.043 | 0.191 | **0.501** |
| **Hit Rate @ 5** | 4% | 30% | **72%** |

**Conclusion**: The domain-specific, contrastive-trained model outperforms the industry-standard generic retriever by **140%** in retrieval precision.

### Stage 10: End-to-End Generative Evaluation
The `10_generative_evaluation.ipynb` notebook evaluates the complete RAG pipeline (retrieval through response generation) using a hybrid approach combining deterministic NLP metrics with LLM-based hallucination detection. All evaluation is conducted on Google Colab using Ollama and Phi-4 Mini, consistent with the methodology established in Stage 8.

| Metric | Score | Description |
| :--- | :--- | :--- |
| **ROUGE-L (F1)** | 0.2024 | Structural overlap between generated answers and source text. Low score confirms the system generates original paraphrased answers rather than copying legal text verbatim. |
| **BERTScore (F1)** | 0.8493 | Semantic similarity between generated answers and ground truth, accounting for paraphrasing and synonymy. |
| **Faithfulness** | 0.7350 | LLM-judged groundedness score (0.0-1.0). Measures whether generated claims are supported by retrieved context. |

**Conclusion**: The system demonstrates strong semantic alignment (BERTScore 0.85) with minimal hallucination (Faithfulness 0.74). When the retriever lacks sufficient context, the system appropriately declines to answer rather than fabricating information.

## Data Source
The data is sourced from the [San Diego City Clerk Official Municipal Code](https://www.sandiego.gov/city-clerk/officialdocs/municipal-code).

This project uses a polite `User-Agent` and respect-based delays to ensure it does not overwhelm the city's servers. It is intended for academic research purposes.

## License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**. 

You are free to use, modify, and distribute this software and the associated model weights for academic, research, and non-commercial portfolio purposes. However, commercial use (using the software/models for a commercial product or service) is strictly prohibited. If you are interested in commercial licensing, please contact the author.

## Acknowledgments
I would like to thank my wonderful professors and peers in the MS-AAI program at the University of San Diego for their guidance, feedback, and support throughout the development of this capstone, and especially my capstone advisor Professor Anna Marbut.