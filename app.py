import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

DONO_NOME = "Gilmar Gnann Guimarães"
DONO_PIX = "nenegnann@gmail.com"
SENHA_DONO = "2026"

st.set_page_config(page_title="Lumina IA", page_icon="🌟", layout="wide")

if "logado_dono" not in st.session_state:
    st.session_state.logado_dono = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "conversa" not in st.session_state:
    st.session_state.conversa = []
if "chave_gemini" not in st.session_state:
    st.session_state.chave_gemini = ""

medidas = {
    "Fachada": (1200, 600),
    "Placa": (900, 600),
    "Banner": (1200, 450),
    "Cartão de Visita": (450, 270),
    "Adesivo": (600, 600)
}

with st.expander("🔒 Área do Criador"):
    if not st.session_state.logado_dono:
        senha = st.text_input("Senha", type="password")
        if st.button("🔑 Entrar"):
            if senha == SENHA_DONO:
                st.session_state.logado_dono = True
                st.rerun()
            else:
                st.error("❌ Errada")
    else:
        st.success(f"✅ {DONO_NOME}")
        st.info(f"PIX: `{DONO_PIX}`")
        st.session_state.chave_gemini = st.text_input("Chave Gemini", type="password", value=st.session_state.chave_gemini)
        st.caption("Grátis: makersuite.google.com")
        if st.button("🚪 Sair"):
            st.session_state.logado_dono = False
            st.rerun()

st.title("🌟 Lumina IA")

if not st.session_state.usuario:
    st.subheader("📝 Cadastre-se grátis")
    with st.form("cad"):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        if st.form_submit_button("✅ Cadastrar") and nome and email:
            st.session_state.usuario = {"nome": nome, "email": email, "usos": 0}
            st.success(f"Bem-vindo, {nome}!")
            st.rerun()
else:
    st.markdown(f"👋 Olá, **{st.session_state.usuario['nome']}**!")
    if st.button("🔄 Sair"):
        st.session_state.usuario = None
        st.rerun()

st.divider()

def responder(mensagem):
    if not st.session_state.chave_gemini:
        return "⚠️ Configure a chave na Área do Criador."
    hist = ""
    for m in st.session_state.conversa[-4:]:
        hist += f"{m['q']}: {m['t']}\n"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={st.session_state.chave_gemini}"
        r = requests.post(url, json={"contents": [{"parts": [{"text": f"Fale simples em português.\n{hist}\nPergunta: {mensagem}\nResposta:"}]}]}, timeout=30)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return "⚠️ Verifique a chave"
    except:
        return "⚠️ Sem conexão"

aba1, aba2 = st.tabs(["💬 Conversar", "🎨 Criar Projeto"])

with aba1:
    st.subheader("Fale com a Lumina")
    for m in st.session_state.conversa:
        with st.chat_message(m["q"]):
            st.write(m["t"])
    pergunta = st.chat_input("Sua pergunta...")
    if pergunta:
        st.session_state.conversa.append({"q": "você", "t": pergunta})
        with st.chat_message("você"):
            st.write(pergunta)
        with st.chat_message("Lumina"), st.spinner("Pensando..."):
            res = responder(pergunta)
            st.write(res)
        st.session_state.conversa.append({"q": "Lumina", "t": res})

with aba2:
    st.subheader("Monte sua peça")
    texto = st.text_input("Texto principal", "Barraca de Coco")
    tipo = st.selectbox("Tipo", list(medidas.keys()))
    cor_fundo = st.color_picker("Cor de fundo", "#22c55e")
    cor_letra = st.color_picker("Cor da letra", "#000000")
    tamanho = st.slider("Tamanho da letra", 24, 80, 48)
    sombra = st.checkbox("Sombra", True)
    descricao = st.text_area("Descreva o cenário (opcional)", "", placeholder="Ex: praia, sol, areia...")
    arquivo = st.file_uploader("Ou envie sua imagem", type=["jpg", "jpeg", "png"])
    st.divider()
    
    if st.button("✨ Criar", type="primary", use_container_width=True):
        if not texto:
            st.warning("Digite um texto!")
        else:
            larg, alt = medidas[tipo]
            if descricao:
                with st.spinner("Desenhando..."):
                    try:
                        url_img = f"https://image.pollinations.ai/prompt/{descricao.replace(' ', '%20')}?width={larg}&height={alt}&nologo=true"
                        r_img = requests.get(url_img, timeout=120)
                        img = Image.open(io.BytesIO(r_img.content)).resize((larg, alt)) if r_img.status_code == 200 else Image.new("RGB", (larg, alt), cor_fundo)
                    except:
                        img = Image.new("RGB", (larg, alt), cor_fundo)
            elif arquivo:
                img = Image.open(arquivo).convert("RGB").resize((larg, alt))
            else:
                img = Image.new("RGB", (larg, alt), cor_fundo)
            
            desenho = ImageDraw.Draw(img)
            try:
                fonte = ImageFont.truetype("arial.ttf", tamanho)
            except:
                fonte = ImageFont.load_default()
            bbox = desenho.textbbox((0, 0), texto, font=fonte)
            lar_t, alt_t = bbox[2]-bbox[0], bbox[3]-bbox[1]
            x, y = (larg-lar_t)//2, (alt-alt_t)//2
            if sombra:
                desenho.text((x+3, y+3), texto, fill="#000000", font=fonte)
            desenho.text((x, y), texto, fill=cor_letra, font=fonte)
            
            saida = io.BytesIO()
            img.save(saida, format="PNG")
            saida.seek(0)
            st.image(saida, caption=f"{tipo} — {texto}", use_column_width=True)
            with st.expander("🔍 Ampliar"):
                saida.seek(0)
                st.image(saida, caption="Ampliada")
            saida.seek(0)
            st.download_button("📥 Baixar", saida, f"{tipo}.png", "image/png", type="primary", use_container_width=True)
            if st.session_state.usuario:
                st.session_state.usuario["usos"] += 1

st.caption(f"© 2026 — {DONO_NOME}")
