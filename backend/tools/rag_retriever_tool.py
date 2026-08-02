import chromadb

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path="../vectorstore/chroma_data")
        _collection = _client.get_or_create_collection(name="autodev_knowledge")
    return _collection


def retrieve_context(query: str, category: str = None, n_results: int = 2) -> list[str]:
    collection = _get_collection()

    where_filter = {"category": category} if category else None

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
    )

    documents = results.get("documents", [[]])[0]
    return documents
