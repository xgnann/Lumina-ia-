import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Lumina IA", page_icon="✨", layout="wide")

NOME = "Gilmar Gnann Guimarães"
PIX = "nenegnann@gmail.com"

st.title("✨ Lumina IA — Comunicação Visual")
st.subheader("100% Gratuita 💜")

aba1, aba2, aba3 = st.tabs(["Criar", "Acabamentos", "Sobre"])

with aba1:
    tipo = st.selectbox("Tipo", ["Fachada", "Placa", "Banner", "Cartão"])
    texto = st.text_input("Texto")
    cor_fundo = st.color_picker("Cor de fundo", "#2E86AB")
    cor_texto = st.color_picker("Cor do texto", "#FFFFFF")

    if st.button("✨ Gerar"):
        st.success("Pronto! ✅")
        
        img = Image.new("RGB", (800, 400), cor_fundo)
        desenho = ImageDraw.Draw(img)
        
        try:
            fonte = ImageFont.truetype("arial.ttf", 50)
        except:
            fonte = ImageFont.load_default()
        
        bbox = desenho.textbbox((0,0), texto, font=fonte)
        lar = bbox[2] - bbox[0]
        alt = bbox[3] - bbox[1]
        x = (800 - lar) // 2
        y = (400 - alt) // 2
        desenho.text((x, y), texto, fill=cor_texto, font=fonte)
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        
        # ✅ AQUI ESTÁ A MUDANÇA IMPORTANTE
        st.image(buf.getvalue(), caption="Sua arte ✨", use_column_width=True)
        
        buf.seek(0)
        st.download_button("📥 Baixar", buf, f"{tipo}.png", "image/png")

with aba2:
    for item in ["Adesivo", "Lona", "ACM", "Letra Caixa"]:
        st.checkbox(item)

with aba3:
    st.write(f"**Nome:** {NOME}")
    st.write(f"**PIX:** {PIX}")
    st.caption("© 2026 — Todos os direitos reservados")
