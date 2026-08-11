from pathlib import Path

import chromadb
from pypdf import PdfReader


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_FILE = (
    PROJECT_ROOT
    / "data"
    / "vehicle_manuals"
    / "basic_vehicle_maintenance.txt"
)

KNOWLEDGE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vehicle_manuals"
)


# ============================================================
# CHROMA DATABASE
# ============================================================

CHROMA_DIR = (
    PROJECT_ROOT
    / "data"
    / "chroma_db"
)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="vehicle_maintenance"
)


# ============================================================
# LOAD TEXT KNOWLEDGE BASE
# ============================================================

def load_text_knowledge():
    """
    Load the existing TXT knowledge base.
    """

    sections = []

    if not KNOWLEDGE_FILE.exists():
        print(
            f"[RAG Agent] TXT file not found: "
            f"{KNOWLEDGE_FILE}"
        )
        return sections

    try:
        text = KNOWLEDGE_FILE.read_text(
            encoding="utf-8"
        ).strip()

        if text:
            sections.append(text)

            print(
                "[RAG Agent] Loaded TXT knowledge base."
            )

    except Exception as e:
        print(
            f"[RAG Agent] Error reading TXT file: {e}"
        )

    return sections


# ============================================================
# LOAD PDF KNOWLEDGE
# ============================================================

def load_pdf_knowledge():
    """
    Read all PDF files from the vehicle_manuals folder
    and extract their text.
    """

    documents = []

    pdf_files = sorted(
        KNOWLEDGE_DIR.glob("*.pdf")
    )

    print(
        f"[RAG Agent] Found {len(pdf_files)} PDF files."
    )

    for pdf_file in pdf_files:

        try:
            reader = PdfReader(
                str(pdf_file)
            )

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            text = text.strip()

            if text:

                documents.append(
                    {
                        "source": pdf_file.name,
                        "text": text
                    }
                )

                print(
                    f"[RAG Agent] Loaded PDF: "
                    f"{pdf_file.name}"
                )

            else:

                print(
                    f"[RAG Agent] WARNING: "
                    f"No text extracted from "
                    f"{pdf_file.name}"
                )

        except Exception as e:

            print(
                f"[RAG Agent] Error reading "
                f"{pdf_file.name}: {e}"
            )

    return documents


# ============================================================
# LOAD ALL KNOWLEDGE INTO CHROMA
# ============================================================

def load_knowledge_base():
    """
    Load TXT and PDF knowledge into Chroma.
    """

    sections = []

    # --------------------------------------------------------
    # Load TXT knowledge
    # --------------------------------------------------------

    text_sections = load_text_knowledge()

    sections.extend(
        text_sections
    )

    # --------------------------------------------------------
    # Load PDF knowledge
    # --------------------------------------------------------

    pdf_documents = load_pdf_knowledge()

    for pdf_document in pdf_documents:

        source = pdf_document["source"]
        text = pdf_document["text"]

        document_text = (
            f"Source: {source}\n\n"
            f"{text}"
        )

        sections.append(
            document_text
        )

    # --------------------------------------------------------
    # Check knowledge base
    # --------------------------------------------------------

    if not sections:

        raise ValueError(
            "Knowledge base is empty."
        )

    print(
        f"\n[RAG Agent] Total knowledge documents: "
        f"{len(sections)}"
    )

    # --------------------------------------------------------
    # Add documents to Chroma
    # --------------------------------------------------------

    if collection.count() == 0:

        collection.add(
            documents=sections,
            ids=[
                f"vehicle_doc_{i}"
                for i in range(len(sections))
            ]
        )

        print(
            f"[RAG Agent] Loaded "
            f"{len(sections)} "
            "knowledge documents into Chroma."
        )

    else:

        print(
            f"[RAG Agent] Chroma already contains "
            f"{collection.count()} documents."
        )

    return sections


# ============================================================
# RETRIEVE RAG CONTEXT
# ============================================================

```python
# ============================================================
# RETRIEVE RAG CONTEXT
# ============================================================

def get_rag_context(
    user_input: str,
    top_k: int = 3
) -> str:
    """
    Retrieve the most relevant vehicle maintenance
    knowledge from Chroma while limiting the amount
    of context sent to the LLM.
    """

    # Make sure knowledge base exists
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

    # --------------------------------------------------------
    # Limit each retrieved document
    # --------------------------------------------------------

    MAX_CHARS_PER_DOCUMENT = 4000
    MAX_TOTAL_CONTEXT_CHARS = 9000

    limited_documents = []

    for document in documents:

        limited_document = document[
            :MAX_CHARS_PER_DOCUMENT
        ]

        limited_documents.append(
            limited_document
        )

    # --------------------------------------------------------
    # Combine retrieved documents
    # --------------------------------------------------------

    context = "\n\n".join(
        limited_documents
    )

    # --------------------------------------------------------
    # Final safety limit
    # --------------------------------------------------------

    context = context[
        :MAX_TOTAL_CONTEXT_CHARS
    ]

    print(
        f"[RAG Agent] Retrieved "
        f"{len(documents)} "
        "relevant knowledge sections."
    )

    print(
        f"[RAG Agent] Context limited to "
        f"{len(context)} characters."
    )

    return context
```



# ============================================================
# TEST RAG AGENT
# ============================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "      VEHICLE MAINTENANCE RAG AGENT"
    )

    print(
        "========================================\n"
    )

    # --------------------------------------------------------
    # Load PDFs
    # --------------------------------------------------------

    pdf_docs = load_pdf_knowledge()

    print(
        f"\nTotal PDFs loaded: "
        f"{len(pdf_docs)}"
    )

    # --------------------------------------------------------
    # Load everything into Chroma
    # --------------------------------------------------------

    print(
        "\nLoading knowledge into Chroma..."
    )

    load_knowledge_base()

    print(
        "\n[RAG Agent] RAG knowledge base "
        "is ready."
    )

    # --------------------------------------------------------
    # TEST RAG RETRIEVAL
    # --------------------------------------------------------

    test_question = (
        "My car engine is overheating. "
        "What should I check?"
    )

    print(
        "\nTesting RAG retrieval..."
    )

    context = get_rag_context(
        test_question,
        top_k=3
    )

    print(
        "\n========== RETRIEVED CONTEXT ==========\n"
    )

    print(context)

    print(
        "\n========================================"
    )