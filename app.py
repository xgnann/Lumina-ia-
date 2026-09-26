import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
st.set_page_config(page_title="Lumina IA", page_icon="✨")
NOME = "Gilmar Gnann Guimarães"
PIX = "nenegnann@gmail.com"
st.title("✨ Lumina IA")
aba1, aba2, aba3 = st.tabs(["Criar", "Acabamentos", "Sobre"])
with aba1:
     tipo = st.selectbox("Tipo", ["Fachada", "Placa", "Banner", "Cartão"])
     texto = st.text_input("Texto")
     cf = st.color_picker("Fundo", "#2E86AB")
     ct = st.color_picker("Texto", "#FFFFFF")
     if st.button("✨ Gerar"):
         img = Image.new("RGB", (800, 400), cf)
         d = ImageDraw.Draw(img)
         f = ImageFont.load_default()
         b = d.textbbox((0, 0), texto, font=f)
         l = b[2] - b[0]
         a = b[3] - b[1]
         x = (800 - l) // 2
         y = (400 - a) // 2
         d.text((x, y), texto, fill=ct, font=f)
         
         arq = io.BytesIO()
         img.save(arq, "PNG")
         arq.seek(0)
         st.image(arq)
         
         arq.seek(0)
         st.download_button("Baixar", arq, f"{tipo}.png")
with aba2:
     st.checkbox("Adesivo")
     st.checkbox("Lona")
     st.checkbox("ACM")
     st.checkbox("Letra Caixa")
with aba3:
     st.write(f"Nome: {NOME}")
     st.write(f"PIX: {PIX}")
     st.caption("© 2026")
