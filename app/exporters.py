import os
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

BASE_DIR=Path(__file__).resolve().parent.parent
EXPORT_DIR=BASE_DIR/"static"/"exports"; EXPORT_DIR.mkdir(parents=True,exist_ok=True)

def _font():
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(p): return p
    return None

def save_pdf(layout):
    pdf=FPDF(); pdf.set_auto_page_break(auto=True,margin=15)
    fp=_font()
    if fp:
        pdf.add_font("ComicFont","",fp); family="ComicFont"
    else: family="Helvetica"
    for p in layout:
        pdf.add_page(); pdf.set_font(family,size=16)
        pdf.cell(0,12,f"Panel {p['panel']}: {p['title']}",align="C"); pdf.ln(8)
        if os.path.exists(p["image_path"]):
            pdf.image(p["image_path"],x=20,y=35,w=170); pdf.set_y(150)
        else:
            pdf.set_y(45); pdf.multi_cell(0,8,"Image missing")
        pdf.set_font(family,size=11); pdf.multi_cell(0,6,p["text"].replace("\r",""))
    path=EXPORT_DIR/f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(str(path)); return str(path)
