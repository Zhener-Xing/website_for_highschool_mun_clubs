from pydantic import BaseModel, EmailStr, Field


class CaptchaResponse(BaseModel):
    captcha_token: str
    image_base64: str


class TeamCreate(BaseModel):
    school: str = Field(..., min_length=2, max_length=150)
    advisor_name: str = Field(..., min_length=1, max_length=50)
    advisor_phone: str = Field(..., min_length=6, max_length=20)
    leader_name: str = Field(..., min_length=1, max_length=50)
    leader_phone: str = Field(..., min_length=6, max_length=20)
    leader_qq: str = Field(..., min_length=4, max_length=20)
    team_email: EmailStr
    remark: str | None = Field(default=None, max_length=1000)
    team_size: int = Field(..., ge=1, le=200)
    registration_form_url: str = Field(..., min_length=5)
    payment_mode: str = Field(..., pattern="^(immediate|deferred)$")
    captcha_token: str = Field(..., min_length=6)
    captcha_code: str = Field(..., min_length=3, max_length=10)


class TeamCreateResponse(BaseModel):
    message: str
    data: dict


class PaymentCreateResponse(BaseModel):
    message: str
    data: dict


class PaymentStatusUpdate(BaseModel):
    payment_status: str = Field(..., pattern="^(pending|paid|failed|refunded)$")
