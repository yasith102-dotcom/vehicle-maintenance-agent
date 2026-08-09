import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from app.agents.diagnosis import diagnose_vehicle
from app.rag.rag_agent import get_rag_context
from app.agents.risk_agent import assess_risk


def coordinate_request(user_input: str) -> str:
    """
    Coordinator Agent manages communication between
    the RAG, Diagnosis, and Risk Assessment agents.
    """

    print("\n[Coordinator Agent] Request received.")

    print("[Coordinator Agent] Retrieving vehicle knowledge...")

    context = get_rag_context(user_input)

    print("[Coordinator Agent] Sending request to Diagnosis Agent...")

    diagnosis = diagnose_vehicle(user_input, context)

    print("[Coordinator Agent] Diagnosis Agent responded.")

    print(
        "[Coordinator Agent] Sending diagnosis "
        "to Risk Assessment Agent..."
    )

    risk_assessment = assess_risk(diagnosis)

    print(
        "[Coordinator Agent] Risk Assessment Agent responded."
    )

    return f"""
DIAGNOSIS
=========

{diagnosis}

RISK ASSESSMENT
===============

{risk_assessment}
"""


if __name__ == "__main__":

    user_input = input(
        "Describe your vehicle problem: "
    )

    result = coordinate_request(user_input)

    print("\n========== FINAL RESULT ==========")
    print(result)