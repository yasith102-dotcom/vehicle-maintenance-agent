import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


# ============================================================
# IMPORT AGENTS
# ============================================================

from app.agents.diagnosis import diagnose_vehicle
from app.rag.rag_agent import get_rag_context
from app.agents.risk_agent import assess_risk


# ============================================================
# COORDINATOR AGENT
# ============================================================

def coordinate_request(user_input: str) -> str:
    """
    Coordinator Agent manages communication between
    the RAG, Diagnosis, and Risk Assessment agents.
    """

    print(
        "\n[Coordinator Agent] Request received."
    )

    # --------------------------------------------------------
    # Step 1: Retrieve knowledge using RAG Agent
    # --------------------------------------------------------

    print(
        "[Coordinator Agent] "
        "Retrieving vehicle knowledge..."
    )

    context = get_rag_context(
        user_input
    )

    # --------------------------------------------------------
    # Step 2: Send user input + RAG context
    #         to Diagnosis Agent
    # --------------------------------------------------------

    print(
        "[Coordinator Agent] "
        "Sending request to Diagnosis Agent..."
    )

    diagnosis = diagnose_vehicle(
        user_input,
        context
    )

    print(
        "[Coordinator Agent] "
        "Diagnosis Agent responded."
    )

    # --------------------------------------------------------
    # Step 3: Send diagnosis to Risk Agent
    # --------------------------------------------------------

    print(
        "[Coordinator Agent] "
        "Sending diagnosis to Risk Assessment Agent..."
    )

    risk_assessment = assess_risk(
        diagnosis
    )

    print(
        "[Coordinator Agent] "
        "Risk Assessment Agent responded."
    )

    # --------------------------------------------------------
    # Step 4: Return final result
    # --------------------------------------------------------

    return f"""
# DIAGNOSIS

{diagnosis}

# RISK ASSESSMENT

{risk_assessment}
"""


# ============================================================
# TEST COORDINATOR AGENT
# ============================================================

if __name__ == "__main__":

    user_input = input(
        "Describe your vehicle problem: "
    )

    result = coordinate_request(
        user_input
    )

    print(
        "\n========== FINAL RESULT =========="
    )

    print(result)