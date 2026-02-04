from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas, models

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/teams")
def list_teams(
    payment_status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    total, items = crud.list_teams(db, payment_status, page, page_size)
    data = [
        {
            "team_id": t.id,
            "school": t.school,
            "leader_name": t.leader_name,
            "team_email": t.team_email,
            "payment_mode": t.payment_mode,
            "payment_status": t.payment_status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in items
    ]
    return {"total": total, "page": page, "data": data}


@router.get("/payments")
def list_payments(
    payment_status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    total, items = crud.list_payments(db, payment_status, page, page_size)
    data = [
        {
            "order_id": p.id,
            "order_no": p.order_no,
            "team_id": p.team_id,
            "amount": float(p.amount),
            "payment_status": p.payment_status,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in items
    ]
    return {"total": total, "page": page, "data": data}


@router.patch("/payments/{payment_id}/status")
def update_payment_status(
    payment_id: int,
    payload: schemas.PaymentStatusUpdate,
    db: Session = Depends(get_db),
):
    payment = crud.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="订单不存在")

    payment = crud.update_payment_status(db, payment, payload.payment_status)

    team = db.query(models.Team).filter(models.Team.id == payment.team_id).first()
    if team:
        team.payment_status = "paid" if payment.payment_status == "paid" else team.payment_status
        db.add(team)
        db.commit()

    return {
        "message": "Payment status updated",
        "data": {
            "order_id": payment.id,
            "order_no": payment.order_no,
            "payment_status": payment.payment_status,
        },
    }
