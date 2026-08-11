# Vehicle Maintenance Agent

## Overview

Vehicle Maintenance Agent is an Agentic AI application designed to assist users in identifying possible vehicle problems and assessing the associated risk.

The system combines multiple AI agents with Retrieval-Augmented Generation (RAG) to provide vehicle diagnosis based on user-provided symptoms and domain-specific vehicle maintenance knowledge.

## Key Features

* AI-based vehicle problem diagnosis
* Multiple cooperating AI agents
* Retrieval-Augmented Generation (RAG)
* PDF-based vehicle maintenance knowledge base
* Risk assessment
* Recommended diagnostic actions
* Streamlit web interface
* Groq LLM integration
* Public cloud deployment

## System Architecture

The application uses a coordinator-based multi-agent architecture.

```text
User
  ↓
Streamlit Interface
  ↓
Coordinator Agent
  ↓
RAG Agent
  ↓
Vehicle Knowledge Base
  ↓
Diagnosis Agent
  ↓
Risk Assessment Agent
  ↓
Final Diagnosis + Risk Assessment
```

## Agents

### Coordinator Agent

The Coordinator Agent manages the workflow between the different components of the system.

It:

1. Receives the user's vehicle symptoms.
2. Requests relevant knowledge from the RAG Agent.
3. Sends the retrieved context and symptoms to the Diagnosis Agent.
4. Sends the diagnosis to the Risk Assessment Agent.
5. Returns the final result to the user.

### RAG Agent

The RAG Agent retrieves relevant information from the vehicle maintenance knowledge base.

The knowledge base contains vehicle maintenance documents in PDF and text formats. The retrieved information is used to provide domain-specific context to the Diagnosis Agent.

### Diagnosis Agent

The Diagnosis Agent analyzes the vehicle symptoms together with the retrieved knowledge and identifies:

* Possible causes
* Most likely cause
* Severity level
* Recommended diagnostic steps

### Risk Assessment Agent

The Risk Assessment Agent evaluates the diagnosis and provides:

* Risk level
* Safety concerns
* Whether the vehicle should be driven
* Recommended action

## Technologies Used

* Python
* FastAPI
* Streamlit
* Groq
* LangChain
* ChromaDB
* Pydantic
* Uvicorn
* HTML/CSS/JavaScript
* Git and GitHub

## Project Structure

```text
vehicle-maintenance-agent/
│
├── app/
│   ├── agents/
│   │   ├── coordinator.py
│   │   ├── diagnosis.py
│   │   └── risk_agent.py
│   │
│   ├── rag/
│   │   └── rag_agent.py
│   │
│   └── api.py
│
├── data/
│   └── vehicle_manuals/
│
├── frontend/
│   └── index.html
│
├── tests/
│
├── streamlit_app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How the System Works

The user enters a vehicle problem through the web interface.

The Coordinator Agent receives the request and communicates with the RAG Agent to retrieve relevant vehicle maintenance information.

The retrieved information is passed to the Diagnosis Agent together with the user's symptoms.

The Diagnosis Agent produces a diagnosis, which is then passed to the Risk Assessment Agent.

Finally, the system returns the diagnosis and risk assessment to the user.

## Example

### User Input

```text
My car makes a clicking noise when I try to start the engine.
```

### System Output

The system identifies possible causes such as:

* Weak or discharged battery
* Corroded or loose battery terminals
* Faulty starter motor
* Faulty starter solenoid

The system also provides a severity level, recommended diagnostic steps, and a risk assessment.

## Running the Application Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the FastAPI backend

```bash
python -m uvicorn app.api:app --reload
```

### Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

The Streamlit application can then be accessed through the local URL provided by Streamlit.

## Environment Variables

The application requires a Groq API key.

Create a `.env` file locally:

```text
GROQ_API_KEY=your_groq_api_key
```

For Streamlit Cloud deployment, configure the key through Streamlit Secrets instead of committing it to GitHub.

## Deployment

The application is deployed using Streamlit Community Cloud.

Live Application:

https://vehicle-maintenance-agent-jwpwrzkxxm9jtdo6nsryyq.streamlit.app/

Source Code:

https://github.com/yasith102-dotcom/vehicle-maintenance-agent

## Security

API keys and other sensitive environment variables should not be committed to the GitHub repository.

The `.env` file is excluded using `.gitignore`, while the deployed application uses Streamlit Secrets for the Groq API key.

## Project Purpose

This project demonstrates the practical application of Agentic AI concepts including:

* Multi-agent architecture
* Agent-to-agent communication
* Retrieval-Augmented Generation
* LLM integration
* Knowledge-grounded reasoning
* Risk assessment
* Cloud deployment
* Software engineering and version control
