import chromadb


COLLECTION_NAME = "policy"
def retrieve(query, n_results: int = 3) -> str:
    client = chromadb.PersistentClient(
        path="./chromadb",
    )
    collection = client.get_collection(COLLECTION_NAME)
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    documents = results.get("documents", [[]])[0]
    context = "\n".join(documents)
    return context


if __name__ == "__main__":
    x = retrieve(
        query = "what is warranty policies?",
        n_results=3
    )
    print(x)