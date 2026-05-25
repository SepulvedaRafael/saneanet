import asyncio
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from shared.protocol import DELIMITER, enviar_mensagem, serializar_json

st.set_page_config(page_title="SANEANET - Inspetor", page_icon="🌊")
st.title("🌊 SANEANET — Terminal do Inspetor")

with st.sidebar:
    st.header("⚙️ Conexão com a Secretaria")
    server_ip = st.text_input("IP do servidor", value="127.0.0.1")
    server_port = st.number_input(
        "Porta", value=9999, step=1, min_value=1, max_value=65535
    )
    inspector_id = st.text_input("ID do Inspetor", value="INS-001")
    industry = st.selectbox(
        "🏭 Indústria de Alocação",
        [
            "Indústria A - Salesópolis",
            "Indústria B - Mogi das Cruzes",
            "Indústria C - Guarulhos",
            "Indústria D - São Paulo (Zona Leste)",
        ],
    )
    shift = st.radio(
        "⏰ Turno de Revezamento",
        ["🌅 Manhã", "🌇 Tarde", "🌙 Noite"],
        horizontal=False,
    )

urgency_label = st.selectbox(
    "Nível de urgência",
    [
        "🟢 Verde — Processo normalizado",
        "🟡 Amarelo — Advertência",
        "🔴 Vermelho — Vazamento detectado",
    ],
)
urgency_map = {
    "🟢 Verde — Processo normalizado": "green",
    "🟡 Amarelo — Advertência": "yellow",
    "🔴 Vermelho — Vazamento detectado": "red",
}

message = st.text_area(
    "Descrição da ocorrência", placeholder="Descreva o que foi observado..."
)
uploaded_file = st.file_uploader(
    "📎 Anexar evidência (PDF ou imagem)", type=["pdf", "png", "jpg", "jpeg"]
)


async def enviar_texto(ip: str, port: int, payload: dict) -> tuple[bool, str]:
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.write(serializar_json(payload))
        await writer.drain()
        ack = await reader.readline()
        writer.close()
        await writer.wait_closed()
        return True, ack.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return False, str(e)


async def enviar_arquivo(
    ip: str, port: int, payload: dict, file_bytes: bytes
) -> tuple[bool, str]:
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.write(serializar_json(payload))
        writer.write(file_bytes)
        writer.write(DELIMITER)
        await writer.drain()
        ack = await reader.readline()
        writer.close()
        await writer.wait_closed()
        return True, ack.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return False, str(e)


st.divider()
c_a, c_b = st.columns(2)

with c_a:
    if st.button("📤 Enviar mensagem de texto", use_container_width=True):
        if not message.strip():
            st.warning("Digite uma descrição antes de enviar.")
        else:
            payload = enviar_mensagem(
                inspector_id=inspector_id,
                industry=industry,
                shift=shift,
                urgency=urgency_map[urgency_label],
                message=message,
                msg_type="text",
                filename=uploaded_file.name if uploaded_file else None,
                file_size=len(uploaded_file.getvalue()) if uploaded_file else 0,
            )
            with st.spinner("Transmitindo..."):
                ok, resp = asyncio.run(
                    enviar_texto(server_ip, int(server_port), payload)
                )
            if ok:
                st.success(f"✅ Mensagem entregue à Secretaria! ({resp})")
            else:
                st.error(f"❌ Falha: {resp}")

with c_b:
    if st.button("📎 Enviar arquivo de evidência", use_container_width=True):
        if uploaded_file is None:
            st.warning("Selecione um arquivo (PDF ou imagem).")
        else:
            payload = enviar_mensagem(
                inspector_id=inspector_id,
                industry=industry,
                shift=shift,
                urgency=urgency_map[urgency_label],
                message=message or f"Evidência: {uploaded_file.name}",
                msg_type="file",
                filename=uploaded_file.name,
                file_size=len(uploaded_file.getvalue()),
            )
            with st.spinner("Enviando arquivo..."):
                ok, resp = asyncio.run(
                    enviar_arquivo(
                        server_ip, int(server_port), payload, uploaded_file.getvalue()
                    )
                )
            if ok:
                st.success(f"✅ Arquivo '{uploaded_file.name}' enviado! ({resp})")
            else:
                st.error(f"❌ Falha: {resp}")
