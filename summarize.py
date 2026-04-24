import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv()

_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
_CLIENT = None

MODEL = "gemini-2.5-pro"
PROMPT = (
    "From transcript, output EXACTLY these 10 lines in same order. "
    "If missing use N/A. "
    "For Caller Name, use the agent's name only as the agent is the caller. "
    "For Duration, use the last timestamp as call duration if no explicit duration is given. "
    "For Date & Time, extract from transcript file name and write EXACTLY as: MM-DD-YYYY HH-MM (24hr). Example: 04-22-2026 01-00 "
    "For Response, summarize the purpose/topic of the call and whether the agent answered all questions and outcome. Max 3-4 lines.\n"
    "Date_&_Time: \n"
    "Caller_Name: \n"
    "Duration: \n"
    "Patient_Name: \n"
    "Medication: \n"
    "Pharmacy: \n"
    "Insurance: \n"
    "insurance_number: \n"
    "Prescriber: \n"
    "Status: \n"
    "Response: "
)


def _get_client():
    global _CLIENT
    if _CLIENT is None:
        if not _API_KEY:
            raise RuntimeError("Missing GOOGLE_API_KEY or GEMINI_API_KEY in .env")
        _CLIENT = genai.Client(api_key=_API_KEY)
    return _CLIENT


def summarize(transcript: str, filename: str = "") -> str:
    """
    Takes transcript as a string and optional filename for date extraction.
    Returns summary as a string.
    """
    client = _get_client()

    full_prompt = (
        f"{PROMPT}\n\n"
        f"Transcript file name: {filename}\n"
        f"Transcript:\n{transcript}"
    )

    response = client.models.generate_content(model=MODEL, contents=full_prompt)
    return (response.text or "").strip()