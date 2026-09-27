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
        st.info(f"PIX: {DONO_PIX}")
        st.session_state.chave_gemini = st.text_input("Chave Gemini", type="password", value=st.session_state.chave_gemini)
        st.caption("Sua chave já está configurada!")
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
    st.markdown(f"👋 Olá, {st.session_state.usuario['nome']}!")
    if st.button("🔄 Sair"):
        st.session_state.usuario = None
        st.rerun()

st.divider()

def responder_ia(mensagem):
    chave = st.session_state.chave_gemini.strip()
    if not chave:
        return "⚠️ Coloque sua chave na Área do Criador acima."
    
    # Detecta tipo de chave e usa endereço certo
    if chave.startswith("AQ."):
        # Chave nova (Google Cloud) → usa Vertex AI
        url = "https://aiplatform.googleapis.com/v1/projects/default/locations/us-central1/publishers/google/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": chave}
        dados = {
            "contents": [{
                "role": "user",
                "parts": [{"text": f"Responda em português do Brasil de forma simples e amigável: {mensagem}"}]
            }]
        }
    else:
        # Chave tradicional (AIza...) → usa endereço antigo
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={chave}"
        headers = {"Content-Type": "application/json"}
        dados = {
            "contents": [{
                "parts": [{"text": f"Responda em português do Brasil de forma simples e amigável: {mensagem}"}]
            }]
        }
    
    try:
        r = requests.post(url, json=dados, headers=headers, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            return resp["candidates"][0]["content"]["parts"][0]["text"]
        return f"⚠️ Erro {r.status_code}. Verifique se a chave está ativa."
    except Exception as e:
        return f"⚠️ Sem conexão ou formato incompatível: {str(e)}"

aba1, aba2 = st.tabs(["💬 Conversar", "🎨 Criar Projeto"])

with aba1:
    st.subheader("Fale com a Lumina")
    for msg in st.session_state.conversa:
        with st.chat_message(msg["quem"]):
            st.write(msg["texto"])
    pergunta = st.chat_input("Escreva aqui...")
    if pergunta:
        st.session_state.conversa.append({"quem": "você", "texto": pergunta})
        with st.chat_message("você"):
            st.write(pergunta)
        with st.chat_message("Lumina"), st.spinner("Pensando..."):
            resposta = responder_ia(pergunta)
            st.write(resposta)
        st.session_state.conversa.append({"quem": "Lumina", "texto": resposta})

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
            larg, alt = medidas
