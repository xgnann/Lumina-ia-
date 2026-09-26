import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

st.set_page_config(page_title="Lumina IA — Gerador de Projetos", page_icon="✨", layout="wide")

DONO_NOME = "Gilmar Gnann Guimarães"
DONO_PIX = "nenegnann@gmail.com"
SENHA = "2026"

if "logado" not in st.session_state:
    st.session_state.logado = False

st.title("✨ Lumina IA — Do Desenho à Fachada")
st.caption(f"Propriedade: {DONO_NOME} | Versão 2.0")
st.divider()

aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "✏️ Descrever",
    "🖼️ Gerar Imagem",
    "📷 Sua Foto",
    "👁️ Resultado",
    "👑 Painel do Dono"
])

dimensoes = {
    "Fachada": (800, 400),
    "Placa": (600, 400),
    "Banner": (900, 300),
    "Cartão": (350, 200),
    "Adesivo": (400, 400)
}

# Variáveis globais
texto_principal = ""
cor_fundo = "#22DD55"
cor_texto = "#000000"
tipo_peca = "Fachada"
imagem_gerada = None
arquivo_foto = None

with aba1:
    st.subheader("📝 Descreva seu Projeto")
    tipo_peca = st.selectbox("Tipo de Peça", list(dimensoes.keys()))
    
    st.info("💬 Descreva o cenário, cores, estilo...")
    descricao = st.text_area("O que você quer ver?", 
        placeholder="Ex: Barraca de coco na praia, sol brilhando, pessoas bebendo água de coco, cores quentes, estilo convidativo...")
    
    texto_principal = st.text_input("Texto Principal", value="Barraca de Coco")
    
    col1, col2 = st.columns(2)
    with col1:
        cor_fundo = st.color_picker("Cor de Fundo", "#22DD55")
    with col2:
        cor_texto = st.color_picker("Cor do Texto", "#000000")

with aba2:
    st.subheader("🖼️ Gerar Imagem com IA")
    
    if st.button("🎨 Criar Imagem", type="primary"):
        if descricao:
            with st.spinner("🔄 A IA está criando... Aguarde!"):
                try:
                    # Usando API gratuita de geração de imagem
                    prompt_completo = f"{descricao}, {tipo_peca}, sinalização profissional, alta qualidade"
                    
                    # Chamada à API
                    resposta = requests.get(
                        "https://image.pollinations.ai/prompt/" + prompt_completo.replace(" ", "%20"),
                        params={"width": dimensoes[tipo_peca][0], "height": dimensoes[tipo_peca][1]},
                        timeout=60
                    )
                    
                    if resposta.status_code == 200:
                        imagem_gerada = Image.open(io.BytesIO(resposta.content))
                        st.success("✅ Imagem criada com sucesso!")
                        st.image(imagem_gerada, caption="Imagem gerada pela IA")
                        st.session_state.imagem_gerada = imagem_gerada
                    else:
                        st.warning("⚠️ Serviço temporariamente indisponível — use sua foto na aba ao lado")
                        
                except Exception as e:
                    st.warning("⚠️ Conexão lenta — envie sua própria foto na aba 'Sua Foto'")
    
    if "imagem_gerada" in st.session_state and st.session_state.imagem_gerada:
        st.info("✅ Imagem pronta! Vá para a aba 'Resultado'")

with aba3:
    st.subheader("📷 Ou envie sua própria imagem")
    arquivo_foto = st.file_uploader("Escolha foto/logo", type=["jpg", "jpeg", "png"])
    if arquivo_foto:
        st.success("✅ Imagem carregada!")
        st.image(arquivo_foto, width=300)

with aba4:
    st.subheader("👁️ Projeto Final")
    
    if not texto_principal:
        st.info("✏️ Digite um texto na aba 'Descrever'")
    else:
        larg, alt = dimensoes[tipo_peca]
        
        # Escolhe qual imagem usar
        if "imagem_gerada" in st.session_state and st.session_state.imagem_gerada:
            img = st.session_state.imagem_gerada.resize((larg, alt))
            st.info("🖼️ Usando imagem gerada pela IA")
        elif arquivo_foto:
            img = Image.open(arquivo_foto).convert("RGB").resize((larg, alt))
            st.info("📷 Usando sua imagem")
        else:
            img = Image.new("RGB", (larg, alt), cor_fundo)
            st.info("🎨 Usando cor de fundo")
        
        # Desenha texto
        desenho = ImageDraw.Draw(img)
        fonte = ImageFont.load_default()
        bbox = desenho.textbbox((0, 0), texto_principal, font=fonte)
        lar_texto = bbox[2] - bbox[0]
        alt_texto = bbox[3] - bbox[1]
        
        x = (larg - lar_texto) // 2
        y = (alt - alt_texto) // 2
        
        # Sombra para destacar texto
        desenho.text((x+2, y+2), texto_principal, fill="#000000", font=fonte)
        desenho.text((x, y), texto_principal, fill=cor_texto, font=fonte)
        
        st.image(img, caption=f"{tipo_peca} — {texto_principal}")
        
        # Baixar
        saida = io.BytesIO()
        img.save(saida, "PNG")
        saida.seek(0)
        st.download_button("📥 Baixar Projeto Final", saida, f"{tipo_peca}.png", "image/png")

with aba5:
    if not st.session_state.logado:
        st.subheader("🔐 Área Reservada")
        senha = st.text_input("Senha do Dono", type="password")
        if st.button("🔑 Entrar"):
            if senha == SENHA:
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta")
    else:
        st.subheader("👑 Painel de Controle")
        st.success(f"✅ Bem-vindo, {DONO_NOME}!")
        st.divider()
        st.write("### 👤 Seus Dados")
        st.write(f"**Nome:** {DONO_NOME}")
        st.info(f"**PIX para orçamento:** `{DONO_PIX}`")
        st.divider()
        st.write("### 📝 Comandos")
        comando = st.text_area("Diga o que melhorar:", 
            placeholder="Ex: deixar a fonte maior | adicionar tipo | cores mais brilhantes...")
        if st.button("📤 Enviar Comando") and comando:
            st.code(f"COMANDO: {comando}", language="markdown")
            st.info("✅ Recebido! Me fale e eu atualizo!")
        st.divider()
        if st.button("🚪 Sair"):
            st.session_state.logado = False
            st.rerun()
