from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, models, schemas
from ..utils import MOCK_AMOUNT, QR_ASSET_PATH, generate_order_no, load_or_generate_qr_base64

router = APIRouter(prefix="/api/v1", tags=["payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/teams/{team_id}/payments", response_model=schemas.PaymentCreateResponse, status_code=status.HTTP_201_CREATED)
def create_payment(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="团队不存在")

    if team.payment_mode != "immediate":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该团队为延期支付")

    order_no = generate_order_no()
    payment = crud.create_payment(db, team_id=team.id, order_no=order_no, amount=MOCK_AMOUNT)

    qr_base64 = load_or_generate_qr_base64(f"mock-pay:{order_no}")

    return {
        "message": "Payment created",
        "data": {
            "order_id": payment.id,
            "order_no": payment.order_no,
            "amount": float(payment.amount),
            "payment_status": payment.payment_status,
            "qr_image_base64": qr_base64,
            "qr_image_url": "/static/qr.png" if QR_ASSET_PATH.exists() else None,
        },
    }


@router.get("/payments/{payment_id}/status")
def get_payment_status(payment_id: int, db: Session = Depends(get_db)):
    payment = crud.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="订单不存在")

    return {
        "order_id": payment.id,
        "order_no": payment.order_no,
        "payment_status": payment.payment_status,
        "updated_at": payment.updated_at.isoformat() if payment.updated_at else None,
    }
