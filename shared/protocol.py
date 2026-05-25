import json
from datetime import datetime

DELIMITER = b"\n"


def enviar_mensagem(
    inspector_id: str,
    industry: str,
    shift: str,
    urgency: str,
    message: str,
    msg_type: str = "text",
    filename: str | None = None,
    file_size: int = 0,
) -> dict:
    return {
        "type": msg_type,
        "timestamp": datetime.now().isoformat(),
        "inspector_id": inspector_id,
        "industry": industry,
        "shift": shift,
        "urgency": urgency,
        "message": message,
        "filename": filename,
        "file_size": file_size,
    }


def serializar_json(data: dict) -> bytes:
    """Serializa dict em JSON UTF-8 e adiciona delimitador."""
    return json.dumps(data, ensure_ascii=False).encode("utf-8") + DELIMITER


def decodificar_json(raw: bytes) -> dict:
    """Decodifica bytes JSON UTF-8 em dict."""
    return json.loads(raw.decode("utf-8").strip())
