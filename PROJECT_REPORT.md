# ComicCraft — Project Report

## Title
ComicCraft - AI Comic Story Creator using Gemini Models

## Objective
Convert a user's story prompt, character, setting, tone and art-style choices into a connected five-panel comic and PDF.

## Architecture
Frontend: HTML, CSS, Jinja2
Backend: FastAPI + Uvicorn
AI: Gemini for outline and story generation
Image generation: Hugging Face Diffusers / Stable Diffusion-compatible pipeline
Export: FPDF

## Workflow
1. User enters story details.
2. FastAPI receives the form.
3. Gemini creates a 5-panel outline.
4. Gemini creates narration and dialogue.
5. Image generation creates panel images.
6. Layout builder combines text and images.
7. FPDF exports the comic.
8. Preview page displays the result.

## Main files
app/main.py
app/routes.py
app/gemini_flash.py
app/gemini_pro.py
app/image_generator.py
app/layout_builder.py
app/exporters.py
templates/index.html
templates/comic_preview.html
templates/export_success.html
