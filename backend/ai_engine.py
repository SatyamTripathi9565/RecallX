import uuid
import os
from gtts import gTTS


# ===============================
# 🔥 FAST SUMMARY
# ===============================
def summarize_text(text):
    return text[:100]


# ===============================
# 🔥 LOCAL "AI" ANSWER (NO API)
# ===============================
def generate_answer(query, context):
    try:
        if not context:
            return f"I don’t have enough memory to answer your question: '{query}'"

        return f"""
You asked: "{query}"

Here’s what I remember:
{context[:300]}

👉 Based on this, it seems related to your previous input.
"""

    except Exception as e:
        return f"Error generating answer: {str(e)}"


# ===============================
# 🔊 TEXT TO SPEECH
# ===============================
def text_to_speech(text):
    try:
        os.makedirs("media", exist_ok=True)

        filename = f"audio_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("media", filename)

        tts = gTTS(text)
        tts.save(filepath)

        return filepath

    except Exception as e:
        return None