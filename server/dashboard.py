"""Painel de controle da Secretaria - lê os dados persistidos pelo servidor."""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(page_title="SANEANET - Secretaria", page_icon="🏛️", layout="wide")
st.title("🏛️ SANEANET — Painel da Secretaria de Meio Ambiente")
st.caption("Monitoramento em tempo real do Rio Tietê")

DATA_DIR = Path(__file__).parent / "data"
MSGS_FILE = DATA_DIR / "messages.json"
FILES_DIR = DATA_DIR / "files"


def load_messages() -> list:
    if not MSGS_FILE.exists():
        return []
    try:
        return json.loads(MSGS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


messages = load_messages()

# --- Métricas ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("📨 Total de relatórios", len(messages))
c2.metric(
    "🚨 Críticos (vermelho)", sum(1 for m in messages if m.get("urgency") == "red")
)
c3.metric(
    "⚠️ Advertências (amarelo)", sum(1 for m in messages if m.get("urgency") == "yellow")
)
c4.metric("📎 Arquivos recebidos", sum(1 for m in messages if m.get("type") == "file"))

st.divider()

# --- Filtros ---
col_a, col_b = st.columns([2, 1])
with col_a:
    urgency_filter = st.multiselect(
        "Filtrar por urgência",
        ["red", "yellow", "green"],
        default=["red", "yellow", "green"],
    )
with col_b:
    st.write("")
    st.write("")
    if st.button("🔄 Atualizar agora"):
        st.rerun()

filtered = [m for m in messages if m.get("urgency") in urgency_filter]

# --- Lista de relatórios ---
st.subheader("📋 Relatórios recebidos")
if not filtered:
    st.info("Nenhum relatório ainda. Aguardando inspetores...")
else:
    icon = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
    for m in reversed(filtered):
        urg = m.get("urgency", "green")
        titulo = (
            f"{icon.get(urg, '⚪')} [{m.get('inspector_id')}] "
            f"{m.get('message', '')[:70]}  —  {m.get('timestamp', '')[:19]}"
        )
        with st.expander(titulo):
            c_a, c_b = st.columns(2)
            with c_a:
                st.write(f"**Inspetor:** {m.get('inspector_id')}")
                st.write(f"**Urgência:** {urg}")
                loc = m.get("location", {})
                st.write(f"**Local:** lat {loc.get('lat')}, lng {loc.get('lng')}")
                st.write(f"**Mensagem:** {m.get('message')}")
            with c_b:
                st.json(m)
                if m.get("type") == "file" and m.get("stored_as"):
                    fpath = FILES_DIR / m["stored_as"]
                    if fpath.exists():
                        with open(fpath, "rb") as f:
                            st.download_button(
                                "⬇️ Baixar evidência",
                                f,
                                file_name=m.get("filename", "arquivo"),
                                key=f"dl_{m.get('timestamp')}",
                            )
