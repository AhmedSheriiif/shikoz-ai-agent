import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

POLICY_PDF_FILE = "./data/policy.pdf"
COLLECTION_NAME = "policy"

# Extracting all text from pdf
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    full_text = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text("text")
        text = text.strip()
        if text:
            full_text.append(text)
    doc.close()
    return "\n".join(full_text)

# Splitting Text
def split_text(text: str):
    """Split text into chunks for RAG"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=[
            '\n\n',
            '\n',
            '. ',
            ' ',
            ''
        ]
    )
    return splitter.split_text(text)

def create_collection():
    """Create or get ChromaDB collection"""
    client = chromadb.PersistentClient(
        path="./chromadb",
    )
    collection = client.get_or_create_collection(COLLECTION_NAME)
    return collection

def store_chunks(collection, chunks):
    """Store chunks in collection"""
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "source": POLICY_PDF_FILE,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas,
    )


if __name__ == "__main__":
    text = extract_text_from_pdf(POLICY_PDF_FILE)
    chunks = split_text(text)
    collection = create_collection()
    store_chunks(collection, chunks)
    print(f"Stored {len(chunks)} chunks successfully.")

    results = collection.get()
    for i, doc in enumerate(results['documents']):
        print(f"\n--- Chunk {i} ---")
        print(doc[:200])  # first 200 chars of each chunk