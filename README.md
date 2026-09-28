# ComicCraft — AI Comic Story Creator

Built from the supplied SmartInternz ComicCraft reference document.

## Features
- 5-panel outline generation
- Gemini narration/dialogue
- Diffusers-compatible image layer
- Demo mode for ordinary laptops
- FastAPI + Jinja2 frontend
- PDF export
- JSON API
- Image test route

## Run
```bash
python -m venv env
```
Windows:
```bash
env\Scripts\activate
```
macOS/Linux:
```bash
source env/bin/activate
```
Then:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key.

Start:
```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and `/docs`.

## Demo mode
Keep:
```text
DEMO_MODE=true
IMAGE_PROVIDER=demo
```
This lets the complete workflow run without downloading a large image model.

## Full Diffusers mode
Set:
```text
DEMO_MODE=false
IMAGE_PROVIDER=diffusers
```
A GPU is strongly recommended.

## Submission
1. Run and test the app.
2. Capture screenshots.
3. Push this folder to GitHub.
4. Never upload `.env` or API keys.
5. Submit the GitHub link and project-document link in the faculty Google Form.
