import streamlit as st

from app.agents.coordinator import coordinate_request


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Vehicle Maintenance AI",
    page_icon="🔧",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🔧 Vehicle Maintenance AI")

st.write(
    "An Agentic AI system for vehicle diagnosis, "
    "RAG-based knowledge retrieval, and risk assessment."
)


# ============================================================
# VEHICLE PROBLEM INPUT
# ============================================================

st.subheader("🚗 Describe Your Vehicle Problem")

symptoms = st.text_area(
    "Enter the vehicle symptoms:",
    placeholder=(
        "Example: My car makes a clicking noise "
        "when I try to start the engine."
    ),
    height=150
)


# ============================================================
# DIAGNOSE BUTTON
# ============================================================

if st.button("🔍 Diagnose Vehicle", type="primary"):

    if not symptoms.strip():

        st.warning(
            "Please describe your vehicle problem first."
        )

    else:

        with st.spinner(
            "🤖 AI agents are analyzing your vehicle problem..."
        ):

            try:

                result = coordinate_request(
                    symptoms.strip()
                )

                st.success(
                    "✓ Analysis Completed"
                )

                st.subheader("📋 Diagnosis Result")

                st.markdown(result)

            except Exception as e:

                st.error(
                    "Unable to complete the diagnosis."
                )

                st.exception(e)


# ============================================================
# INFORMATION
# ============================================================

st.divider()

st.caption(
    "Vehicle Maintenance AI | "
    "Coordinator Agent + RAG Agent + "
    "Diagnosis Agent + Risk Assessment Agent"
)