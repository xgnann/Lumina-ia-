import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
st.set_page_config(page_title="Lumina IA — Controle Total", page_icon="👑", layout="wide")
# ⚙️ DADOS DO DONO
DONO_NOME = "Gilmar Gnann Guimarães"
DONO_PIX = "nenegnann@gmail.com"
SENHA_OPERADOR = "2026"  # ← Você pode mudar essa senha quando quiser!
# 📦 CONFIGURAÇÕES PADRÃO (aqui você muda tudo!)
config = {
     "nome_projeto": "Lumina IA",
     "cor_fundo_padrao": "#22DD55",
     "cor_texto_padrao": "#000000",
     "largura_padrao": 800,
     "altura_padrao": 400,
     "versao": "1.1"
 }
 # 🔑 SISTEMA DE ACESSO
if "logado" not in st.session_state:
st.session_state.logado = False
st.title("✨ Lumina IA — Sistema de Produção Visual")
st.caption(f"Versão {config['versao']} | Propriedade: {DONO_NOME}")
st.divider()
aba1, aba2, aba3, aba4 = st.tabs([
     "🎨 Produção", 
     "📤 Enviar Imagem", 
     "👁️ Prévia",
     "⚙️ Painel do Dono"
 ])
 # ==========================================
 # ABA 1 — PRODUÇÃO
 # ==========================================
 with aba1:
     st.subheader("📐 Criar Projeto")
     
     col1, col2 = st.columns(2)
     with col1:
         tipo = st.selectbox("Tipo de Peça", [
             "Fachada", "Placa", "Banner", "Cartão de Visita", "Adesivo"
         ])
         texto = st.text_input("Texto Principal", value="Digite aqui...")
     
     with col2:
         cor_fundo = st.color_picker("Cor de Fundo", config["cor_fundo_padrao"])
         cor_texto = st.color_picker("Cor do Texto", config["cor_texto_padrao"])
     
     dimensoes = {
         "Fachada": (800, 400),
         "Placa": (600, 400),
         "Banner": (900, 300),
         "Cartão de Visita": (350, 200),
         "Adesivo": (400, 400)
     }
     larg, alt = dimensoes[tipo]
 # ==========================================
 # ABA 2 — ENVIAR FOTO/LOGO
 # ==========================================
 with aba2:
     st.subheader("📷 Sua Imagem / Logo / Foto")
     arquivo_envio = st.file_uploader(
         "Envie arquivo de imagem",
         type=["jpg", "jpeg", "png", "webp"]
     )
     
     if arquivo_envio:
         st.success("✅ Imagem recebida! Aparece na prévia")
         st.image(arquivo_envio, width=200)
 # ==========================================
 # ABA 3 — PRÉVIA E DOWNLOAD
 # ==========================================
 with aba3:
     st.subheader("👁️ Prévia em Tempo Real")
     
     if texto:
         img = Image.new("RGB", (larg, alt), cor_fundo)
         
         # Cola imagem enviada
         if arquivo_envio:
             foto = Image.open(arquivo_envio).convert("RGBA")
             foto.thumbnail((int(larg*0.35), int(alt*0.7)))
             fx = 20
             fy = (alt - foto.height) // 2
             img.paste(foto, (fx, fy), foto if foto.mode=="RGBA" else None)
             margem_texto = fx + foto.width + 30
         else:
             margem_texto = 20
         
         # Desenha texto
         desenho = ImageDraw.Draw(img)
         fonte = ImageFont.load_default()
         caixa = desenho.textbbox((0,0), texto, font=fonte)
         l_texto = caixa[2] - caixa[0]
         a_texto = caixa[3] - caixa[1]
         
         x_texto = margem_texto + ((larg - margem_texto - 20) - l_texto) // 2
         y_texto = (alt - a_texto) // 2
         desenho.text((x_texto, y_texto), texto, fill=cor_texto, font=fonte)
         
         st.image(img, caption=f"Prévia — {tipo}", use_column_width=True)
         
         saida = io.BytesIO()
         img.save(saida, "PNG")
         saida.seek(0)
         st.download_button("📥 Baixar Projeto", saida, f"{tipo}.png", "image/png")
     else:
         st.info("✏️ Digite um texto na aba 'Produção' para ver a prévia")
 # ==========================================
 # ABA 4 — PAINEL DO DONO (SÓ SEU!)
 # ==========================================
 with aba4:
     if not st.session_state.logado:
         st.subheader("🔐 Área Reservada")
         senha_digitada = st.text_input("Digite sua senha", type="password")
         
         if st.button("🔑 Entrar como Dono"):
             if senha_digitada == SENHA_OPERADOR:
                 st.session_state.logado = True
                 st.success("✅ Acesso concedido! Bem-vindo, Gilmar!")
                 st.rerun()
             else:
                 st.error("❌ Senha incorreta")
     else:
         st.subheader("👑 Painel de Controle — Lumina IA")
         st.success(f"✅ Conectado como: {DONO_NOME}")
         st.divider()
         
         st.write("### ⚙️ Configurações da IA")
         st.info("Altere aqui e a IA se atualiza!")
         
         config["nome_projeto"] = st.text_input("Nome da IA", value=config["nome_projeto"])
         config["cor_fundo_padrao"] = st.color_picker("Fundo Padrão", config["cor_fundo_padrao"])
         config["cor_texto_padrao"] = st.color_picker("Texto Padrão", config["cor_texto_padrao"])
         
         st.divider()
         st.write("### 📝 Comandos Diretos")
         st.info("Aqui você me diz o que mudar e eu te mostro o código!")
         
         comando = st.text_area(
             "Diga o que quer que a IA faça:",
             placeholder="Ex: Quero adicionar o tipo 'Adesivo Redondo' | Quero fonte maior | Mudar cor padrão para azul..."
         )
         
         if st.button("📤 Enviar Comando"):
             if comando:
                 st.success("✅ Comando recebido! Eu vou te ajudar a implementar isso!")
                 st.code(f"COMANDO DO DONO:\n{comando}", language="markdown")
                 st.info("Me avise e eu te passo o trecho de código pronto para colar! 💜")
         
         st.divider()
         st.write("### 👤 Seus Dados")
         st.write(f"**Nome:** {DONO_NOME}")
         st.write(f"**PIX:** `{DONO_PIX}`")
         
         st.divider()
         if st.button("🚪 Sair"):
             st.session_state.logado = False
             st.rerun()
