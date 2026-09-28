import os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .config import DEMO_MODE, IMAGE_PROVIDER, IMAGE_MODEL

BASE_DIR = Path(__file__).resolve().parent.parent
PANEL_DIR = BASE_DIR/"static"/"panels"
PANEL_DIR.mkdir(parents=True, exist_ok=True)

def _font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def _demo(prompt, filename):
    img = Image.new("RGB",(768,512),"#e8f4ff")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((30,30,738,482), radius=24, outline="#17324d", width=5, fill="#f8fcff")
    d.ellipse((275,125,495,345), fill="#ffb84d", outline="#17324d", width=5)
    d.ellipse((330,190,360,220), fill="#17324d")
    d.ellipse((410,190,440,220), fill="#17324d")
    d.arc((330,235,440,310),10,170,fill="#17324d",width=5)
    d.text((65,385),"ComicCraft Demo Panel",font=_font(30),fill="#17324d")
    d.text((65,430),prompt.replace("\n"," ")[:80],font=_font(15),fill="#31546d")
    path=PANEL_DIR/filename; img.save(path); return str(path)

def _diffusers(prompt, filename):
    import torch
    from diffusers import StableDiffusionPipeline
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    pipe=StableDiffusionPipeline.from_pretrained(IMAGE_MODEL, torch_dtype=dtype, use_safetensors=True)
    pipe=pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    img=pipe(prompt=prompt, negative_prompt="blurry, distorted, watermark, text",
             num_inference_steps=20, height=512, width=512).images[0]
    path=PANEL_DIR/filename; img.save(path); return str(path)

def generate_image(prompt, filename=None):
    filename=filename or "panel.png"
    if DEMO_MODE or IMAGE_PROVIDER=="demo":
        return _demo(prompt, filename)
    if IMAGE_PROVIDER=="diffusers":
        return _diffusers(prompt, filename)
    raise ValueError("IMAGE_PROVIDER must be demo or diffusers")
