import pytest
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
DB_PATH = Path('data/vector_store/san_diego_code_baseline')
COLLECTION_NAME = "san_diego_code"

@pytest.fixture(scope="module")
def chroma_collection():
    """Fixture to provide access to the ChromaDB collection."""
    if not DB_PATH.exists():
        pytest.fail(f"Vector store not found at {DB_PATH}. Run notebook 05 first.")
    
    client = chromadb.PersistentClient(path=str(DB_PATH))
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception as e:
        pytest.fail(f"Could not load collection '{COLLECTION_NAME}': {e}")

@pytest.fixture(scope="module")
def embedding_model():
    """Fixture to provide the embedding model."""
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def test_collection_not_empty(chroma_collection):
    """Verify that the collection contains data."""
    count = chroma_collection.count()
    assert count > 0, "Collection is empty."

def test_basic_semantic_search(chroma_collection, embedding_model):
    """Verify that basic semantic search returns results."""
    query_text = "How is building height measured?"
    query_emb = embedding_model.encode(query_text).tolist()
    
    results = chroma_collection.query(
        query_embeddings=[query_emb],
        n_results=1
    )
    
    assert len(results['ids'][0]) > 0
    assert results['documents'][0][0] != ""

def test_metadata_citation_filter(chroma_collection, embedding_model):
    """
    Verify that metadata filtering for citations ($contains) works.
    This ensures the metadata schema in notebook 05 was implemented correctly.
    """
    query_text = "building height"
    query_emb = embedding_model.encode(query_text).tolist()
    
    # This specifically tests the $contains operator on the 'citations' list
    where_filter = {"citations": {"$contains": "113.0201"}}
    
    results = chroma_collection.query(
        query_embeddings=[query_emb],
        n_results=1,
        where=where_filter
    )
    
    assert len(results['ids'][0]) > 0
    # Check if the citation is actually in the metadata of the first result
    assert "113.0201" in results['metadatas'][0][0]['citations']
