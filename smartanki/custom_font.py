import os

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError


def custom_font():
    # Register custom font
    # Construct path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "fonts", "DejaVuSans.ttf")
    try:
        pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
    except FileNotFoundError:
        print(f"[⚠] Font not found at {font_path}")
    except TTFError as e:
        print(f"[⚠] Font loading failed: {e}")
    custom_style = ParagraphStyle(
        "Custom",
        fontName="DejaVuSans",
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
    )
    return custom_style
custom_style = custom_font()