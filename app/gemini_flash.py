import json
from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, GEMINI_OUTLINE_MODEL

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def _fallback(prompt):
    desc = [
        ("The Beginning", f"Introduce the story idea: {prompt}."),
        ("A New Challenge", "The main character discovers a surprising problem."),
        ("Into Action", "The character takes action and the situation becomes exciting."),
        ("Turning Point", "A clever decision changes the direction of the story."),
        ("The Resolution", "The character solves the problem and reaches a satisfying ending."),
    ]
    return [{"panel": i, "title": t, "scene_description": d,
             "image_prompt": f"comic book illustration, {d}, cohesive character design, {prompt}"}
            for i,(t,d) in enumerate(desc,1)]

def generate_outline(user_prompt):
    if not client:
        return _fallback(user_prompt)
    prompt = f"""You are a professional comic planner.
Create exactly 5 connected comic panels from this idea:
{user_prompt}
Return ONLY valid JSON as an array. Each object must contain:
panel (1-5), title, scene_description, image_prompt.
Keep the character and visual identity consistent."""
    r = client.models.generate_content(
        model=GEMINI_OUTLINE_MODEL, contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.9)
    )
    data = json.loads(r.text)
    if not isinstance(data, list) or len(data) != 5:
        raise ValueError("Gemini did not return exactly five panels.")
    return data
