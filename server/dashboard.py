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

col_urg, col_ind, col_shift, col_btn = st.columns([2, 3, 2, 1])

with col_urg:
    urgency_filter = st.multiselect(
        "🚦 Urgência",
        ["red", "yellow", "green"],
        default=["red", "yellow", "green"],
    )

with col_ind:
    industries = sorted(
        set(m.get("industry", "Não informada") for m in messages if m.get("industry"))
    )
    industry_filter = st.multiselect(
        "🏭 Indústria",
        industries,
        default=industries if industries else ["Não informada"],
    )

with col_shift:
    shifts = ["🌅 Manhã", "🌇 Tarde", "🌙 Noite"]
    shift_filter = st.multiselect(
        "⏰ Turno",
        shifts,
        default=shifts,
    )

with col_btn:
    st.write("")
    st.write("")
    if st.button("🔄 Atualizar", use_container_width=True):
        st.rerun()

filtered = [
    m
    for m in messages
    if m.get("urgency") in urgency_filter
    and m.get("industry") in industry_filter
    and m.get("shift") in shift_filter
]

st.subheader(f"📋 Relatórios recebidos ({len(filtered)})")
if not filtered:
    st.info("Nenhum relatório com os filtros selecionados. Aguardando inspetores...")
else:
    icon = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
    for m in reversed(filtered):
        urg = m.get("urgency", "green")
        titulo = (
            f"{icon.get(urg, '⚪')} [{m.get('inspector_id')}] "
            f"{m.get('message', '')[:60]}  —  {m.get('timestamp', '')[:19]}"
        )
        with st.expander(titulo):
            c_a, c_b = st.columns(2)
            with c_a:
                st.write(f"**Inspetor:** {m.get('inspector_id')}")
                st.write(f"**Indústria:** {m.get('industry', 'Não informada')}")
                st.write(f"**Turno:** {m.get('shift', 'Não informado')}")
                st.write(f"**Urgência:** {urg}")
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
