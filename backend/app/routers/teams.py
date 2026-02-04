from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas, models
from ..utils import MOCK_AMOUNT, QR_ASSET_PATH, generate_order_no, load_or_generate_qr_base64

router = APIRouter(prefix="/api/v1", tags=["teams"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_captcha(db: Session, token: str, code: str) -> None:
    captcha = crud.get_captcha_by_token(db, token)
    if not captcha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码无效")
    if captcha.used_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码已使用")
    if captcha.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码已过期")
    if captcha.code.lower() != code.lower():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码错误")
    crud.mark_captcha_used(db, captcha)


@router.post("/teams", response_model=schemas.TeamCreateResponse, status_code=status.HTTP_201_CREATED)
def create_team(payload: schemas.TeamCreate, db: Session = Depends(get_db)):
    existing = crud.find_team_by_email(db, str(payload.team_email))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="团队邮箱已存在")

    validate_captcha(db, payload.captcha_token, payload.captcha_code)

    team: models.Team = crud.create_team(db, payload)

    data = {
        "team_id": team.id,
        "payment_mode": team.payment_mode,
        "payment_status": team.payment_status,
    }

    if team.payment_mode == "immediate":
        order_no = generate_order_no()
        payment = crud.create_payment(db, team_id=team.id, order_no=order_no, amount=MOCK_AMOUNT)
        qr_base64 = load_or_generate_qr_base64(f"mock-pay:{order_no}")
        data["order"] = {
            "order_id": payment.id,
            "order_no": payment.order_no,
            "amount": float(payment.amount),
            "payment_status": payment.payment_status,
            "qr_image_base64": qr_base64,
            "qr_image_url": "/static/qr.png" if QR_ASSET_PATH.exists() else None,
        }

    return {"message": "Team created", "data": data}
