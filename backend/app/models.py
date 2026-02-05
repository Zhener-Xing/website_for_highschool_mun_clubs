from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    school: Mapped[str] = mapped_column(String(150), nullable=False)
    advisor_name: Mapped[str] = mapped_column(String(50), nullable=False)
    advisor_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    leader_name: Mapped[str] = mapped_column(String(50), nullable=False)
    leader_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    leader_qq: Mapped[str] = mapped_column(String(20), nullable=False)
    team_email: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    team_size: Mapped[int] = mapped_column(Integer, nullable=False)
    registration_form_url: Mapped[str] = mapped_column(Text, nullable=False)
    payment_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, default="unpaid")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Captcha(Base):
    __tablename__ = "captcha"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    request_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    order_no: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="CNY")
    payment_status: Mapped[str] = mapped_column(String(20), default="pending")
    payment_method: Mapped[str] = mapped_column(String(50), default="mock")
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
