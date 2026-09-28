import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_OUTLINE_MODEL = os.getenv("GEMINI_OUTLINE_MODEL", "gemini-3.8-flash")
GEMINI_STORY_MODEL = os.getenv("GEMINI_STORY_MODEL", "gemini-3.8-flash")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "demo").lower()
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "stable-diffusion-v1-5/stable-diffusion-v1-5")
