from database.mongodb import chat_history
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

FATIGUE_THRESHOLD = 65
LOAD_THRESHOLD = 70
ATTENTION_FLOOR = 35
FOCUS_THRESHOLD = 70


def evaluate(metrics):
    attention = metrics["attention"]
    meditation = metrics["meditation"]
    load = metrics["cognitive_load"]
    fatigue = metrics["fatigue"]

    if fatigue >= FATIGUE_THRESHOLD:
        status = "fatigued"
        recommendation = (
            "Fatigue is running high. Take a 10-minute break before continuing — "
            "NeuroLearn will shorten your next session and lower difficulty automatically."
        )
    elif load >= LOAD_THRESHOLD:
        status = "overloaded"
        recommendation = (
            "Cognitive load is elevated. Switching to easier practice questions and "
            "slowing the pace so concepts have time to settle."
        )
    elif attention < ATTENTION_FLOOR:
        status = "distracted"
        recommendation = (
            "Attention has dipped. Try a quick 2-minute meditation break, or switch to a "
            "shorter, more interactive activity to re-engage focus."
        )
    elif attention >= FOCUS_THRESHOLD and load < LOAD_THRESHOLD:
        status = "focused"
        recommendation = (
            "You're in a strong focus state. This is a good moment to tackle the "
            "harder material — difficulty has been nudged up for this session."
        )
    else:
        status = "steady"
        recommendation = (
            "Cognitive state is stable. Continuing at your current pace and difficulty level."
        )

    return {
        **metrics,
        "status": status,
        "recommendation": recommendation,
    }


def assistant_reply(message, metrics):
    text = (message or "").lower()

    fatigue = metrics["fatigue"]
    load = metrics["cognitive_load"]
    attention = metrics["attention"]

    if any(w in text for w in ["break", "tired", "rest", "fatigue"]):
        if fatigue >= FATIGUE_THRESHOLD:
            return (
                f"Your fatigue is {fatigue}%. "
                "Yes, this is a good time to take a 10-minute break."
            )
        else:
            return (
                f"Your fatigue is {fatigue}%. "
                "You can continue studying for another 25–30 minutes."
            )

    if any(w in text for w in ["status", "state", "how am i doing"]):
        result = evaluate(metrics)
        return (
            f"Attention: {attention}%\n"
            f"Cognitive Load: {load}%\n"
            f"Fatigue: {fatigue}%\n\n"
            f"Overall Status: {result['status']}\n\n"
            f"{result['recommendation']}"
        )

    prompt = f"""
You are NeuroLearn AI, an educational tutor.

Current student EEG state:
- Attention: {attention}%
- Cognitive Load: {load}%
- Fatigue: {fatigue}%

Student question:
{message}

Instructions:
- Answer clearly and accurately.
- Keep the answer under 250 words.
- If fatigue or cognitive load is high, naturally mention it before answering.
- If appropriate, encourage effective study habits.
"""

    try:
     response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    chat_history.insert_one({
        "user_message": message,
        "ai_response": response.text,
        "attention": attention,
        "fatigue": fatigue,
        "cognitive_load": load,
    })

    return response.text
    except Exception as e:
    import traceback
    traceback.print_exc()
    return f"ERR`OR: {str(e)}"
