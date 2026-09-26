import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Lumina IA", page_icon="✨", layout="wide")

DONO_NOME = "Gilmar Gnann Guimarães"
DONO_PIX = "nenegnann@gmail.com"
SENHA_OPERADOR = "2026"

config = {
    "nome_projeto": "Lumina IA",
    "cor_fundo_padrao": "#22DD55",
    "cor_texto_padrao": "#000000",
    "versao": "1.1"
}

if "logado" not in st.session_state:
    st.session_state.logado = False

st.title("✨ Lumina IA — Comunicação Visual")
st.caption(f"Versão {config['versao']} | Propriedade: {DONO_NOME}")
st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "🎨 Produção",
    "📷 Sua Imagem",
    "👁️ Prévia",
    "👑 Painel do Dono"
])

dimensoes = {
    "Fachada": (800, 400),
    "Placa": (600, 400),
    "Banner": (900, 300),
    "Cartão de Visita": (350, 200),
    "Adesivo": (400, 400)
}

with aba1:
    st.subheader("📐 Dados do Projeto")
    col1, col2 = st.columns(2)
    with col1:
        tipo = st.selectbox("Tipo de Peça", list(dimensoes.keys()))
        texto = st.text_input("Texto Principal", value="Seu Texto Aqui")
    with col2:
        cor_fundo = st.color_picker("Cor de Fundo", config["cor_fundo_padrao"])
        cor_texto = st.color_picker("Cor do Texto", config["cor_texto_padrao"])

with aba2:
    st.subheader("📷 Envie Sua Imagem / Logo")
    arquivo_envio = st.file_uploader("Imagem", type=["jpg", "jpeg", "png", "webp"])
    if arquivo_envio:
        st.success("✅ Imagem recebida!")
        st.image(arquivo_envio, width=200)

with aba3:
    st.subheader("👁️ Prévia em Tempo Real")
    if texto:
        larg, alt = dimensoes[tipo]
        img = Image.new("RGB", (larg, alt), cor_fundo)
        
        if arquivo_envio:
            foto = Image.open(arquivo_envio).convert("RGBA")
            foto.thumbnail((int(larg*0.35), int(alt*0.7)))
            fx = 20
            fy = (alt - foto.height) // 2
            img.paste(foto, (fx, fy), foto if foto.mode=="RGBA" else None)
            margem_texto = fx + foto.width + 30
        else:
            margem_texto = 20
        
        desenho = ImageDraw.Draw(img)
        fonte = ImageFont.load_default()
        caixa = desenho.textbbox((0, 0), texto, font=fonte)
        l_texto = caixa[2] - caixa[0]
        a_texto = caixa[3] - caixa[1]
        x_texto = margem_texto + ((larg - margem_texto - 20) - l_texto) // 2
        y_texto = (alt - a_texto) // 2
        desenho.text((x_texto, y_texto), texto, fill=cor_texto, font=fonte)
        
        st.image(img, caption=f"Prévia — {tipo}")
        saida = io.BytesIO()
        img.save(saida, "PNG")
        saida.seek(0)
        st.download_button("📥 Baixar Projeto", saida, f"{tipo}.png", "image/png")
    else:
        st.info("✏️ Digite um texto na aba Produção")

with aba4:
    if not st.session_state.logado:
        st.subheader("🔐 Área do Dono")
        senha = st.text_input("Senha", type="password")
        if st.button("🔑 Entrar"):
            if senha == SENHA_OPERADOR:
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("❌ Senha errada")
    else:
        st.subheader("👑 Painel de Controle")
        st.success(f"✅ Bem-vindo, {DONO_NOME}!")
        st.divider()
        st.write("### ⚙️ Configurações")
        config["nome_projeto"] = st.text_input("Nome da IA", config["nome_projeto"])
        config["cor_fundo_padrao"] = st.color_picker("Fundo Padrão", config["cor_fundo_padrao"])
        config["cor_texto_padrao"] = st.color_picker("Texto Padrão", config["cor_texto_padrao"])
        st.divider()
        st.write("### 📝 Comandos")
        comando = st.text_area("Diga o que mudar:", placeholder="Ex: adicionar tipo...")
        if st.button("📤 Enviar Comando") and comando:
            st.code(f"Comando: {comando}", language="markdown")
            st.info("✅ Recebido! Me fale e eu te ajudo!")
        st.divider()
        st.write("### 👤 Seus Dados")
        st.write(f"**Nome:** {DONO_NOME}")
        st.info(f"**PIX:** `{DONO_PIX}`")
        st.divider()
        if st.button("🚪 Sair"):
            st.session_state.logado = False
            st.rerun()
