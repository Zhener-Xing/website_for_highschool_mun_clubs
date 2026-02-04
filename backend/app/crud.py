from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def create_team(db: Session, payload: schemas.TeamCreate) -> models.Team:
    payment_status = "pending" if payload.payment_mode == "immediate" else "unpaid"

    team = models.Team(
        school=payload.school,
        advisor_name=payload.advisor_name,
        advisor_phone=payload.advisor_phone,
        leader_name=payload.leader_name,
        leader_phone=payload.leader_phone,
        leader_qq=payload.leader_qq,
        team_email=str(payload.team_email),
        remark=payload.remark,
        team_size=payload.team_size,
        registration_form_url=payload.registration_form_url,
        payment_mode=payload.payment_mode,
        payment_status=payment_status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def find_team_by_email(db: Session, email: str) -> models.Team | None:
    return db.query(models.Team).filter(models.Team.team_email == email).first()


def save_captcha(db: Session, token: str, code: str, expires_at: datetime, request_ip: str | None) -> models.Captcha:
    captcha = models.Captcha(
        token=token,
        code=code,
        expires_at=expires_at,
        request_ip=request_ip,
        created_at=datetime.utcnow(),
    )
    db.add(captcha)
    db.commit()
    db.refresh(captcha)
    return captcha


def get_captcha_by_token(db: Session, token: str) -> models.Captcha | None:
    return db.query(models.Captcha).filter(models.Captcha.token == token).first()


def mark_captcha_used(db: Session, captcha: models.Captcha) -> None:
    captcha.used_at = datetime.utcnow()
    db.add(captcha)
    db.commit()


def create_payment(db: Session, team_id: int, order_no: str, amount: float) -> models.Payment:
    payment = models.Payment(
        team_id=team_id,
        order_no=order_no,
        amount=amount,
        payment_status="pending",
        payment_method="mock",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_by_id(db: Session, payment_id: int) -> models.Payment | None:
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def list_teams(db: Session, payment_status: str | None, page: int, page_size: int) -> tuple[int, list[models.Team]]:
    query = db.query(models.Team)
    if payment_status:
        query = query.filter(models.Team.payment_status == payment_status)
    total = query.count()
    items = query.order_by(models.Team.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def list_payments(db: Session, payment_status: str | None, page: int, page_size: int) -> tuple[int, list[models.Payment]]:
    query = db.query(models.Payment)
    if payment_status:
        query = query.filter(models.Payment.payment_status == payment_status)
    total = query.count()
    items = query.order_by(models.Payment.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def update_payment_status(db: Session, payment: models.Payment, status_value: str) -> models.Payment:
    payment.payment_status = status_value
    payment.updated_at = datetime.utcnow()
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
