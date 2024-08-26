def chunk_document(document: str, chunk_size: int = 1000) -> list:
    """
    Chunk a document into smaller pieces.

    Args:
        document (str): The document to be chunked.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of document chunks.
    """
    # Split the document into chunks of specified size
    chunks = [document[i:i + chunk_size] for i in range(0, len(document), chunk_size)]
    return chunks
