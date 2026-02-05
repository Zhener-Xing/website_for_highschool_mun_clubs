import base64
import io
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/api/v1", tags=["captcha"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_code(length: int = 4) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_image(code: str) -> str:
    width, height = 140, 50
    img = Image.new("RGB", (width, height), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font = ImageFont.load_default()

    for i, ch in enumerate(code):
        draw.text((10 + i * 30, 8), ch, font=font, fill=(20, 20, 20))

    for _ in range(6):
        x1, y1 = secrets.randbelow(width), secrets.randbelow(height)
        x2, y2 = secrets.randbelow(width), secrets.randbelow(height)
        draw.line((x1, y1, x2, y2), fill=(120, 120, 120), width=1)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


@router.get("/captcha", response_model=schemas.CaptchaResponse)
def get_captcha(request: Request, db: Session = Depends(get_db)):
    code = generate_code()
    token = secrets.token_hex(8)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    crud.save_captcha(db, token, code, expires_at, request.client.host if request.client else None)

    return schemas.CaptchaResponse(
        captcha_token=token,
        image_base64=generate_image(code),
    )
