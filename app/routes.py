from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf


router = APIRouter()
templates = Jinja2Templates(directory="templates")


class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str = "Alex"
    setting: str = "forest"
    tone: str = "funny"
    art_style: str = "comic book"


def _run(story_prompt, character_name, setting, tone, art_style):

    prompt = (
        f"Story idea: {story_prompt}\n"
        f"Main character: {character_name}\n"
        f"Setting: {setting}\n"
        f"Tone: {tone}\n"
        f"Art style: {art_style}"
    )

    outline = generate_outline(prompt)

    story = generate_story(
        outline,
        character_name,
        setting,
        tone,
        art_style
    )

    images = []

    for panel in outline:

        visual = (
            f"{panel['image_prompt']}. "
            f"Character: {character_name}. "
            f"Setting: {setting}. "
            f"Tone: {tone}. "
            f"Art style: {art_style}. "
            f"Keep character appearance consistent."
        )

        images.append(
            generate_image(
                visual,
                f"panel_{panel['panel']}.png"
            )
        )

    layout = build_comic_layout(
        images,
        story,
        outline
    )

    pdf = save_pdf(layout)

    return layout, pdf


@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    try:

        layout, pdf = _run(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style
        )

        pdf_url = "/" + pdf.replace("\\", "/").split(
            "static/",
            1
        )[-1]

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_url": pdf_url
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/generate-comic/json")
async def generate_json(p: PromptRequest):

    layout, pdf = _run(
        p.story_prompt,
        p.character_name,
        p.setting,
        p.tone,
        p.art_style
    )

    pdf_path = "/" + pdf.replace("\\", "/").split(
        "static/",
        1
    )[-1]

    return {
        "layout": layout,
        "pdf_path": pdf_path
    }


@router.get("/export-success")
async def export_success(
    request: Request,
    pdf_path: str
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "request": request,
            "pdf_path": pdf_path
        }
    )


@router.get("/test-image")
async def test_image(
    request: Request,
    prompt: str = "a brave fox in an enchanted forest"
):

    path = generate_image(
        prompt,
        "test_panel.png"
    )

    return templates.TemplateResponse(
        request=request,
        name="test_image.html",
        context={
            "request": request,
            "image_url": "/static/panels/test_panel.png",
            "prompt": prompt
        }
    )