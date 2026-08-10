import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def diagnose_vehicle(symptoms: str, context: str = "") -> str:
    """
    Diagnosis Agent powered by Groq.
    """

    prompt = f"""
You are a Vehicle Diagnosis Agent.

Analyze the vehicle symptoms provided by the user.

Identify:

1. Possible causes
2. Most likely cause
3. Severity level: LOW, MEDIUM, or HIGH
4. Recommended next diagnostic step

Do not claim to provide a definitive mechanical diagnosis.
For safety-critical problems, recommend professional inspection.

Relevant vehicle maintenance knowledge:
{context}

Vehicle symptoms:
{symptoms}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful vehicle maintenance "
                    "diagnosis assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    symptoms = input("Enter vehicle symptoms: ")

    result = diagnose_vehicle(symptoms)

    print("\n--- Diagnosis Result ---")
    print(result)