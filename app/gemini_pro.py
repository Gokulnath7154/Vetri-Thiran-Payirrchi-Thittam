from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, GEMINI_STORY_MODEL
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def _fallback(outline):
    return "\n\n".join(
        f"Panel {p['panel']}: {p['title']}\nCaption: The story moves forward.\n"
        f"Narration: {p['scene_description']}\nDialogue: \"We can do this!\""
        for p in outline)

def generate_story(outline, character_name, setting, tone, art_style):
    if not client:
        return _fallback(outline)
    formatted = "\n".join(f"Panel {p['panel']}: {p['title']} | {p['scene_description']}" for p in outline)
    prompt = f"""You are a comic-book writer.
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
Outline:
{formatted}
Write exactly 5 connected panels. For each provide:
Panel N: title
Caption: one short atmospheric caption
Narration: 2-4 sentences
Dialogue: 1-2 natural lines
Do not add extra panels."""
    r = client.models.generate_content(
        model=GEMINI_STORY_MODEL, contents=prompt,
        config=types.GenerateContentConfig(temperature=0.85, max_output_tokens=1800)
    )
    return r.text
