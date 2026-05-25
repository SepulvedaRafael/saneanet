import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from shared.protocol import DELIMITER, decodificar_json

HOST = "0.0.0.0"
PORT = 9000

DATA_DIR = Path(__file__).parent / "data"
MSGS_FILE = DATA_DIR / "messages.json"
FILES_DIR = DATA_DIR / "files"


def ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    FILES_DIR.mkdir(exist_ok=True)
    if not MSGS_FILE.exists():
        MSGS_FILE.write_text("[]", encoding="utf-8")


def append_message(msg: dict) -> None:
    try:
        messages = json.loads(MSGS_FILE.read_text(encoding="utf-8") or "[]")
    except json.JSONDecodeError:
        messages = []
    messages.append(msg)
    MSGS_FILE.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8"
    )


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    addr = writer.get_extra_info("peername")
    print(f"[+] Inspetor conectado: {addr}")
    try:
        while True:
            header = await reader.readline()
            if not header:
                break
            msg = decodificar_json(header)

            if msg.get("type") == "file":
                file_size = int(msg.get("file_size", 0))
                file_data = await reader.readexactly(file_size)
                await reader.readuntil(DELIMITER)
                fname = msg.get("filename") or "arquivo"
                safe_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{fname}"
                (FILES_DIR / safe_name).write_bytes(file_data)
                msg["stored_as"] = safe_name
                print(f"[FILE] Recebido '{fname}' ({file_size} bytes) -> {safe_name}")
            else:
                print(
                    f"[MSG] {msg.get('inspector_id')} | "
                    f"{msg.get('urgency')} | {msg.get('message')[:50]}"
                )

            append_message(msg)

            writer.write(b'{"status":"ok"}\n')
            await writer.drain()

    except (asyncio.IncompleteReadError, ConnectionResetError):
        print(f"[!] Conexão encerrada abruptamente: {addr}")
    except Exception as e:
        print(f"[ERRO] {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[-] Inspetor desconectado: {addr}")


async def main() -> None:
    ensure_dirs()
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"=" * 60)
    print(f"🌊 SANEANET - Servidor da Secretaria")
    print(f"   Escutando em {HOST}:{PORT}")
    print(f"=" * 60)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
