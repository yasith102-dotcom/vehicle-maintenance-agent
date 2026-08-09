from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Knowledge base location
KNOWLEDGE_BASE = (
    BASE_DIR / "data" / "vehicle_manuals" / "basic_vehicle_maintenance.txt"
)


def load_knowledge_base():
    """Load vehicle maintenance documents."""

    loader = TextLoader(
        str(KNOWLEDGE_BASE),
        encoding="utf-8"
    )

    documents = loader.load()

    return documents


def split_documents(documents):
    """Split documents into smaller chunks for retrieval."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    return chunks


def retrieve_vehicle_knowledge(query: str):
    """
    Retrieve relevant vehicle-maintenance information
    from the domain-specific knowledge base.
    """

    documents = load_knowledge_base()

    chunks = split_documents(documents)

    # Simple keyword-based retrieval for the first RAG version.
    query_words = set(query.lower().split())

    scored_chunks = []

    for chunk in chunks:
        text = chunk.page_content.lower()

        score = sum(
            1 for word in query_words
            if len(word) > 2 and word in text
        )

        scored_chunks.append((score, chunk))

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    top_chunks = [
        chunk for score, chunk in scored_chunks[:3]
        if score > 0
    ]

    return top_chunks


def get_rag_context(query: str) -> str:
    """Return retrieved knowledge as context for an AI agent."""

    documents = retrieve_vehicle_knowledge(query)

    if not documents:
        return "No relevant vehicle maintenance information was found."

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context


if __name__ == "__main__":

    question = input(
        "Enter a vehicle maintenance question: "
    )

    context = get_rag_context(question)

    print("\n========== RETRIEVED KNOWLEDGE ==========\n")
    print(context)