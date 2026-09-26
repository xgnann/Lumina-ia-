import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ==================================================
# ✨ LUMINA IA — VERSÃO BRASIL INTEIRO
# Proprietário: Gilmar Gnann Guimarães
# 📧 contato: nenegnann@gmail.com
# 💳 PIX: nenegnann@gmail.com
# 🇧🇷 DIVERSIDADE • INCLUSÃO • TODOS
# 🔒 Marca em registro INPI | Todos os direitos reservados
# ==================================================

st.set_page_config(
    page_title="Lumina IA — Comunicação Visual",
    page_icon="✨",
    layout="wide"
)

SEU_NOME = "Gilmar Gnann Guimarães"
SEU_CPF = "03072871906"  # substitua pelo seu CPF
CHAVE_PIX = "nenegnann@gmail.com"
CONTA_BANCARIA = "Banco: Nu Pagamentos | Agência: 0001 | Conta: 56071828-9"

st.title("✨ Lumina IA — Projetos de Comunicação Visual")
st.subheader("100% Gratuita para você! 💜")

aba1, aba2, aba3, aba4 = st.tabs([
    "🎨 Criar Projeto",
    "📐 Acabamentos",
    "💰 Sobre & Renda",
    "👤 Sobre o Criador"
])

with aba1:
    st.header("Crie sua Arte")
    tipo = st.selectbox("Tipo de projeto", [
        "Fachada", "Placa", "Banner", "Cartão", "Logotipo", "Outro"
    ])
    texto = st.text_input("Texto principal")
    cor_principal = st.color_picker("Cor principal", "#2E86AB")
    cor_texto = st.color_picker("Cor do texto", "#FFFFFF")
    estilo = st.selectbox("Estilo", ["Moderno", "Clássico", "Econômico", "Chamativo"])

    if st.button("✨ Gerar Prévia"):
        st.success(f"✅ Projeto de {tipo} criado com sucesso!")
        st.info(f"Estilo: {estilo} | Texto: {texto}")
        st.balloons()

        largura, altura = 800, 400
        img = Image.new('RGB', (largura, altura), color=cor_principal)
        desenho = ImageDraw.Draw(img)

        try:
            fonte = ImageFont.truetype("arial.ttf", 50)
        except:
            fonte = ImageFont.load_default()

        bbox = desenho.textbbox((0, 0), texto, font=fonte)
        lar_texto = bbox[2] - bbox[0]
        alt_texto = bbox[3] - bbox[1]
        pos_x = (largura - lar_texto) // 2
        pos_y = (altura - alt_texto) // 2
        desenho.text((pos_x, pos_y), texto, font=fonte, fill=cor_texto)

        st.image(img, caption=f"Prévia — {tipo}", use_column_width=True)

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        st.download_button(
            "📥 Baixar Imagem",
            data=buffer.getvalue(),
            file_name=f"Lumina_{tipo}.png",
            mime="image/png"
        )

with aba2:
    st.header("📐 Materiais e Acabamentos")
    st.write("Recomendações para execução:")
    for ac in ["Adesivo", "Letra Caixa", "Lona", "ACM", "Iluminação LED", "Impressão UV"]:
        st.checkbox(ac)
    st.info("🔜 Em breve: indicação de gráficas parceiras!")

with aba3:
    st.header("💰 Como funciona a renda")
    st.markdown("""
    A **Lumina IA** é **gratuita** para todos! 💙
    A renda vem de:
    - 📺 YouTube, Instagram e TikTok — tutoriais e demonstrações
    - 👁️ Quanto mais acessada, mais visualizações = mais ganhos
    - 🤝 Parcerias com gráficas e fornecedores
    - 💸 Doações voluntárias via PIX
    """)
    st.info(f"💳 PIX para doações: **{CHAVE_PIX}**")

with aba4:
    st.header("👤 Dados do Criador")
    st.write(f"**Nome:** {SEU_NOME}")
    st.write(f"**CPF:** {SEU_CPF}")
    st.write(f"**Chave PIX:** {CHAVE_PIX}")
    st.write(f"**Conta Bancária:** {CONTA_BANCARIA}")
    st.caption("© 2026 Lumina IA — Todos os direitos reservados")

st.divider()
st.markdown("<center>✨ Lumina IA — Diversidade • Inclusão • Brasil Inteiro ✨</center>", unsafe_allow_html=True)
