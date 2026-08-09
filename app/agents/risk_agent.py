import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def assess_risk(diagnosis: str) -> str:
    """
    Risk Assessment Agent evaluates the diagnosis
    and assigns a risk level.
    """

    prompt = f"""
You are a Vehicle Safety Risk Assessment Agent.

Analyze the following vehicle diagnosis.

Determine:

1. Risk level:
   LOW, MEDIUM, HIGH, or CRITICAL

2. Safety concern

3. Whether the vehicle should be driven

4. Recommended action

Use the following rules:

LOW:
Routine maintenance or minor issue.

MEDIUM:
Vehicle may have a problem that should be inspected soon.

HIGH:
Potentially unsafe condition. Avoid driving until inspected.

CRITICAL:
Immediate safety concern. Do not drive the vehicle and seek professional assistance.

Do not claim to provide a definitive mechanical diagnosis.

Vehicle diagnosis:
{diagnosis}
"""

    response = client.chat.completions.create(
     model="llama-3.1-8b-instant", 
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful vehicle safety "
                    "risk assessment assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    diagnosis = input(
        "Enter the vehicle diagnosis: "
    )

    result = assess_risk(diagnosis)

    print("\n========== RISK ASSESSMENT ==========\n")
    print(result)