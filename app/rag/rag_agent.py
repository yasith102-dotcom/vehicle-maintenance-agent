from pathlib import Path
import chromadb


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Vehicle knowledge base
KNOWLEDGE_FILE = (
    PROJECT_ROOT
    / "data"
    / "vehicle_manuals"
    / "basic_vehicle_maintenance.txt"
)

# Chroma persistent database
CHROMA_PATH = PROJECT_ROOT / ".chroma"

# Create Chroma client
client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

# Create or load collection
collection = client.get_or_create_collection(
    name="vehicle_maintenance"
)


def load_knowledge_base():
    """
    Load vehicle maintenance knowledge into Chroma.
    """

    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_FILE}"
        )

    text = KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )

    # Split knowledge into individual sections
    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    if not sections:
        raise ValueError(
            "Knowledge base is empty."
        )

    # Add documents only if collection is empty
    if collection.count() == 0:

        collection.add(
            documents=sections,
            ids=[
                f"vehicle_doc_{i}"
                for i in range(len(sections))
            ]
        )

        print(
            f"[RAG Agent] Loaded {len(sections)} "
            "knowledge documents into Chroma."
        )


def get_rag_context(
    user_input: str,
    top_k: int = 3
) -> str:
    """
    Retrieve the most relevant vehicle knowledge
    from Chroma.
    """

    load_knowledge_base()

    results = collection.query(
        query_texts=[user_input],
        n_results=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    if not documents:
        return (
            "No relevant vehicle maintenance "
            "knowledge was found."
        )

    context = "\n\n".join(documents)

    print(
        f"[RAG Agent] Retrieved {len(documents)} "
        "relevant knowledge sections."
    )

    return context