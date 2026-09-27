import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# ====================== SEUS DADOS ======================
DONO_NOME = "Gilmar Gnann Guimarães"
DONO_PIX = "nenegnann@gmail.com"
SENHA_DONO = "2026"

# ====================== CONFIGURAÇÃO ======================
st.set_page_config(
    page_title="Lumina IA — Crie Grátis",
    page_icon="🌟",
    layout="wide",
    menu_items={"About": f"© 2026 — {DONO_NOME}"}
)

# ====================== ESTILO ======================
estilo = """
<style>
.stApp {
    background: linear-gradient(180deg, #e6f3ff, #f0f9ff);
    color: #1e293b;
    font-family: 'Segoe UI', sans-serif;
}
.caixa {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}
.nivel-bronze { border-left: 4px solid #cd7f32; padding-left: 1rem; }
.nivel-prata { border-left: 4px solid #c0c0c0; padding-left: 1rem; }
.nivel-ouro { border-left: 4px solid #ffd700; padding-left: 1rem; }
</style>
"""
st.markdown(estilo, unsafe_allow_html=True)

# ====================== INICIALIZAÇÃO ======================
if "logado_dono" not in st.session_state:
    st.session_state.logado_dono = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "conversa" not in st.session_state:
    st.session_state.conversa = []
if "chave_gemini" not in st.session_state:
    st.session_state.chave_gemini = ""
if "dados_proj" not in st.session_state:
    st.session_state.dados_proj = {
        "texto": "Barraca de Coco",
        "tipo": "Fachada",
        "cor_fundo": "#22c55e",
        "cor_letra": "#000000",
        "tam_letra": 48,
        "sombra": True,
        "cena": ""
    }
if "img_criada" not in st.session_state:
    st.session_state.img_criada = None
if "img_envio" not in st.session_state:
    st.session_state.img_envio = None

medidas_padrao = {
    "Fachada": (1200, 600),
    "Placa": (900, 600),
    "Banner": (1200, 450),
    "Cartão de Visita": (450, 270),
    "Adesivo": (600, 600)
}

# ====================== NÍVEIS DE ACESSO ======================
def nivel_usuario():
    if not st.session_state.usuario:
        return "Visitante", "bronze", "Baixa resolução (800×400)"
    cad = st.session_state.usuario
    if cad.get("nivel", "bronze") == "ouro":
        return "✨ Ouro", "ouro", "Máxima qualidade (1920×960)"
    elif cad.get("nivel", "prata") == "prata":
        return "⭐ Prata", "prata", "Alta qualidade (1400×700)"
    else:
        return "🟢 Cadastrado", "bronze", "Qualidade melhorada (1200×600)"

def obter_resolucao():
    _, nivel, _ = nivel_usuario()
    if nivel == "ouro":
        return {"Fachada": (1920, 960), "Placa": (1400, 930), "Banner": (1920, 720), "Cartão de Visita": (720, 432), "Adesivo": (960, 960)}
    elif nivel == "prata":
        return {"Fachada": (1400, 700), "Placa": (1050, 700), "Banner": (1400, 525), "Cartão de Visita": (525, 315), "Adesivo": (700, 700)}
    elif nivel == "bronze" and st.session_state.usuario:
        return medidas_padrao
    else:
        return {"Fachada": (800, 400), "Placa": (600, 400), "Banner": (800, 300), "Cartão de Visita": (300, 180), "Adesivo": (400, 400)}

# ====================== ÁREA DO DONO ======================
with st.expander("🔒 Área do Criador"):
    if not st.session_state.logado_dono:
        senha = st.text_input("Senha do Criador", type="password")
        if st.button("🔑 Entrar"):
            if senha == SENHA_DONO:
                st.session_state.logado_dono = True
                st.rerun()
            else:
                st.error("❌ Sem permissão")
    else:
        st.success(f"✅ {DONO_NOME}")
        st.info(f"PIX: `{DONO_PIX}`")
        st.divider()
        st.session_state.chave_gemini = st.text_input("Chave Gemini", type="password", value=st.session_state.chave_gemini)
        st.caption("Grátis: makersuite.google.com → Get API key")
        st.divider()
        if st.button("🚪 Sair"):
            st.session_state.logado_dono = False
            st.rerun()

# ====================== CABEÇALHO ======================
st.title("🌟 Lumina IA — Crie sua Arte Visual")
rotulo_nivel, cor_nivel, qualidade = nivel_usuario()
st.markdown(f"""
<div class="caixa nivel-{cor_nivel}">
    <strong>Seu nível:</strong> {rotulo_nivel}<br>
    <small>Qualidade da imagem: {qualidade}</small>
</div>
""", unsafe_allow_html=True)

# CADASTRO
if not st.session_state.usuario:
    st.markdown("### 📝 Cadastre-se para qualidade melhor!")
    with st.form("cadastro"):
        nome = st.text_input("Seu nome")
        email = st.text_input("Seu e-mail")
        enviado = st.form_submit_button("✅ Cadastrar Grátis", type="primary")
        if enviado and nome and email:
            st.session_state.usuario = {"nome": nome, "email": email, "nivel": "bronze", "usos": 0}
            st.success(f"🎉 Bem-vindo, {nome}! Qualidade melhorada liberada!")
            st.rerun()
else:
    st.markdown(f"👋 Olá, **{st.session_state.usuario['nome']}**!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Sair da conta"):
            st.session_state.usuario = None
            st.session_state.conversa = []
            st.rerun()
    with col2:
        usos = st.session_state.usuario["usos"]
        if usos >= 5 and st.session_state.usuario["nivel"] == "bronze":
            st.session_state.usuario["nivel"] = "prata"
            st.success("🎉 Subiu para ⭐ Prata!")
        if usos >= 15 and st.session_state.usuario["nivel"] == "prata":
            st.session_state.usuario["nivel"] = "ouro"
            st.success("🏆 Subiu para ✨ Ouro!")

st.divider()

# ====================== FUNÇÃO DA IA ======================
def responder(mensagem):
    if not st.session_state.chave_gemini:
        return "⚠️ Configure a chave do Gemini na Área do Criador."
    hist = ""
    for m in st.session_state.conversa[-5:]:
        hist += f"{m['quem']}: {m['texto']}\n"
    prompt = f"Você é Lumina IA, amigável e prática. Responda em português do Brasil.\n{hist}\nPergunta: {mensagem}\nResposta:"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={st.session_state.chave_gemini}"
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return "⚠️ Verifique a chave"
    except:
        return "⚠️ Sem conexão"

# ====================== ABAS ======================
aba_conversa, aba_projeto = st.tabs(["💬 Conversar", "🎨 Criar Projeto"])

# ABA 1 — CONVERSA
with aba_conversa:
    st.subheader("💬 Fale com a Lumina")
    for msg in st.session_state.conversa:
        with st.chat_message(msg["quem"]):
            st.write(msg["texto"])
    pergunta = st.chat_input("Pergunte algo...")
    if pergunta:
        st.session_state.conversa.append({"quem": "você", "texto": pergunta})
        with st.chat_message("você"):
            st.write(pergunta)
        with st.chat_message("Lumina"), st.spinner("Pensando..."):
            resp = responder(pergunta)
            st.write(resp)
        st.session_state.conversa.append({"quem": "Lumina", "texto": resp})

# ABA 2 — PROJETO
with aba_projeto:
    st.subheader("🎨 Monte seu Projeto")
    cfg = st.session_state.dados_proj
    res = obter_resolucao()
    
    col1, col2 = st.columns(2)
    with col1:
        cfg["texto"] = st.text_input("✍ Texto", value=cfg["texto"])
        cfg["tipo"] = st.selectbox("📐 Tipo", list(res.keys()), index=list(res.keys()).index(cfg["tipo"]))
        cfg["tam_letra"] = st.slider("🔤 Tamanho da Letra", 24, 80, cfg["tam_letra"])
    with col2:
        cfg["cor_fundo"] = st.color_picker("🎨 Cor de Fundo", cfg["cor_fundo"])
        cfg["cor_letra"] = st.color_picker("✏️ Cor da Letra", cfg["cor_letra"])
        cfg["sombra"] = st.checkbox("💫 Sombra", value=cfg["sombra"])
    
    st.divider()
    cfg["cena"] = st.text_area("🖼️ Descreva a imagem:", value=cfg["cena"], placeholder="Ex: Barraca de coco na praia...", height=100)
    
    if st.button("✨ Gerar Imagem", type="primary", use_container_width=True):
        if cfg["cena"]:
            with st.spinner("Desenhando..."):
                try:
                    larg, alt = res[cfg["tipo"]]
                    prompt_img = f"{cfg['cena']}, sinalização comercial, cores vivas, alta definição, sem texto"
                    url_img = f"https://image.pollinations.ai/prompt/{prompt_img.replace(' ', '%20')}?width={larg}&height={alt}&nologo=true&quality=2"
                    resp_img = requests.get(url_img, timeout=120)
                    if resp_img.status_code == 200:
                        st.session_state.img_criada = Image.open(io.BytesIO(resp_img.content))
                        if st.session_state.usuario:
                            st.session_state.usuario["usos"] += 1
                        st.success(f"✅ Pronto! Resolução: {larg}×{alt}")
                    else:
                        st.warning("⚠️ Envie sua foto abaixo")
                except:
                    st.error("❌ Sem conexão — envie sua imagem")
        else:
            st.warning("⚠️ Descreva a imagem primeiro!")
    
    st.divider()
    st.subheader("📷 Ou use sua imagem")
    st.info("Busque grátis: Pexels · Unsplash · Pixabay")
    envio = st.file_uploader("Envie a imagem", type=["jpg", "jpeg", "png"])
    if envio:
        st.session_state.img_envio = envio
        st.success("✅ Recebida!")
    
    st.divider()
    
    # RESULTADO — CORRIGIDO DE VEZ ✅
    st.subheader("👁️ Resultado Final")
    
    if not cfg["texto"]:
        st.info("✍️ Digite um texto acima")
    else:
        larg, alt = res[cfg["tipo"]]
        
        # Cria imagem base
        if st.session_state.img_criada:
            img = st.session_state.img_criada.resize((larg, alt))
            st.info(f"🖼️ Imagem criada — {larg}×{alt}")
        elif st.session_state.img_envio:
            img = Image.open(st.session_state.img_envio).convert("RGB").resize((larg, alt))
            st.info(f"📷 Sua imagem — {larg}×{alt}")
        else:
            img = Image.new("RGB", (larg, alt), cfg["cor_fundo"])
            st.info(f"🎨 Cor de fundo — {larg}×{alt}")
        
        # Desenha texto
        desenho = ImageDraw.Draw(img)
        try:
            fonte = ImageFont.truetype("arial.ttf", cfg["tam_letra"])
        except:
            fonte = ImageFont.load_default()
        
        bbox = desenho.textbbox((0, 0), cfg["texto"], font=fonte)
        lar_t = bbox[2] - bbox[0]
        alt_t = bbox[3] - bbox[1]
        x = (larg - lar_t) // 2
        y = (alt - alt_t) // 2
        
        if cfg["sombra"]:
            desenho.text((x+3, y+3), cfg["texto"], fill="#000000", font=fonte)
        desenho.text((x, y), cfg["texto"], fill=cfg["cor_letra"], font=fonte)
        
        # Converte para bytes e exibe — GARANTIDO FUNCIONAR ✅
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        legenda = f"{cfg['tipo']} — {cfg['texto']}"
        st.image(buffer, caption=legenda, use_column_width=True)
        
        # Zoom
        with st.expander("🔍 Ampliar imagem"):
            buffer.seek(0)
            st.image(buffer, caption="Visualização ampliada", width=larg)
        
        # Download
        buffer.seek(0)
        nome_arquivo = f"{cfg['tipo']}_{cfg['texto'].replace(' ', '_')}.png"
        st.download_button("📥 BAIXAR EM ALTA", buffer, nome_arquivo, "image/png", type="primary", use_container_width=True)

st.caption("© 2026 — Lumina IA | Propriedade Exclusiva")
