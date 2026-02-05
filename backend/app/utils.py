import base64
import io
import secrets
from datetime import datetime
from pathlib import Path

import qrcode

MOCK_AMOUNT = 199.00
QR_ASSET_PATH = Path(__file__).resolve().parent / "assets" / "qr.png"


def generate_order_no() -> str:
    return "MOCK" + datetime.utcnow().strftime("%Y%m%d%H%M%S") + secrets.token_hex(3).upper()


def load_or_generate_qr_base64(payload: str) -> str:
    if QR_ASSET_PATH.exists():
        data = QR_ASSET_PATH.read_bytes()
        return "data:image/png;base64," + base64.b64encode(data).decode()

    img = qrcode.make(payload)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
