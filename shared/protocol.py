"""Protocolo compartilhado entre cliente e servidor.
Formato: JSON codificado em UTF-8 terminado por \\n (DELIMITER).
Para arquivos: header JSON + bytes do arquivo + DELIMITER.
"""
import json
from datetime import datetime

DELIMITER = b"\n"


def make_message(
    inspector_id: str,
    location: dict,
    urgency: str,
    message: str,
    msg_type: str = "text",
    filename: str | None = None,
    file_size: int = 0,
) -> dict:
    return {
        "type": msg_type,
        "inspector_id": inspector_id,
        "location": location,
        "urgency": urgency,
        "message": message,
        "filename": filename,
        "file_size": file_size,
        "timestamp": datetime.now().isoformat(),
    }


def encode(data: dict) -> bytes:
    """Serializa dict em JSON UTF-8 e adiciona delimitador."""
    return json.dumps(data, ensure_ascii=False).encode("utf-8") + DELIMITER


def decode(raw: bytes) -> dict:
    """Decodifica bytes JSON UTF-8 em dict."""
    return json.loads(raw.decode("utf-8").strip())
