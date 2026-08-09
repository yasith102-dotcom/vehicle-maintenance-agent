from app.rag.rag_agent import get_rag_context
from app.agents.diagnosis import diagnose_vehicle
from app.agents.risk_agent import assess_risk


def test_rag_retrieves_vehicle_knowledge():
    context = get_rag_context(
        "My car makes a clicking noise when starting."
    )

    assert context
    assert len(context) > 0


def test_diagnosis_agent_returns_result():
    result = diagnose_vehicle(
        "My car makes a clicking noise when starting.",
        "A weak battery can cause repeated clicking during starting."
    )

    assert result
    assert len(result) > 0


def test_risk_agent_returns_result():
    result = assess_risk(
        """
        Possible cause: weak battery.
        Severity level: MEDIUM.
        Recommended next step: check battery terminals.
        """
    )

    assert result
    assert len(result) > 0