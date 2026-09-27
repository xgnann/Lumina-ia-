import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# ====================== DADOS EXCLUSIVOS ======================
ADM_NOME = "Gilmar Gnann Guimarães"
ADM_PIX = "nenegnann@gmail.com"
ADM_SENHA = "2026"

# ====================== CONFIGURAÇÃO DE PÁGINA ======================
st.set_page_config(
    page_title="Lumina IA — Painel Administrativo",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== ESTILO VISUAL OFICIAL ======================
estilo = """
<style>
/* Fundo geral */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
}

/* Cartões e caixas */
.caixa {
    background: rgba(30, 41, 59, 0.8);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid rgba(59, 130, 246, 0.3);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

/* Títulos */
h1, h2, h3 { color: #fbbf24; }

/* Botões */
button[kind="primary"] {
    background: linear-gradient(90deg, #f59e0b, #d97706);
    border: none;
    font-weight: bold;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(59, 130, 246, 0.2);
}
</style>
"""
st.markdown(estilo, unsafe_allow_html=True)

# ====================== CONTROLE DE ACESSO ======================
if "adm_logado" not in st.session_state:
    st.session_state.adm_logado = False

if not st.session_state.adm_logado:
    st.markdown('<div class="caixa">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://image.pollinations.ai/prompt/light%20glowing%20star%20logo%20gold%20blue%20minimalist", width=120)
        st.title("🔒 LUMINA IA")
        st.subheader("Painel de Controle — Acesso Exclusivo")
        st.divider()
        
        senha_digitada = st.text_input("Digite sua senha de Administrador", type="password", placeholder="••••••••")
        
        if st.button("🔑 ENTRAR NO SISTEMA", type="primary", use_container_width=True):
            if senha_digitada == ADM_SENHA:
                st.session_state.adm_logado = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta — acesso negado")
        
        st.caption(f"© 2026 — Propriedade Exclusiva: {ADM_NOME}\nTodos os direitos reservados")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ====================== SÓ DEPOIS DE LOGAR ======================
if "config" not in st.session_state:
    st.session_state.config = {
        "cor_fundo": "#22DD55",
        "cor_texto": "#000000",
        "tamanho_fonte": 42,
        "sombra": True,
        "texto": "Barraca de Coco",
        "tipo": "Fachada",
        "descricao_imagem": ""
    }
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "imagem_gerada" not in st.session_state:
    st.session_state.imagem_gerada = None
if "foto_usuario" not in st.session_state:
    st.session_state.foto_usuario = None

dimensoes = {
    "Fachada": (800, 450),
    "Placa": (600, 400),
    "Banner": (900, 350),
    "Cartão de Visita": (350, 200),
    "Adesivo": (400, 400)
}

# ====================== PROCESSADOR DE COMANDOS ======================
def processar_comando(msg_texto):
    msg = msg_texto.lower()
    c = st.session_state.config
    resp = []

    # Texto principal
    for alvo in ["texto é", "diz", "nome é", "colocar"]:
        if alvo in msg:
            t = msg_texto.split(alvo)[-1].strip()
            if t: c["texto"] = t; resp.append(f"✅ Texto definido: **{t}**")
            break

    # Cores de fundo
    if "fundo" in msg:
        if "azul" in msg: c["cor_fundo"] = "#3B82F6"; resp.append("✅ Fundo → Azul")
        elif "verde" in msg: c["cor_fundo"] = "#22C55E"; resp.append("✅ Fundo → Verde")
        elif "amarelo" in msg: c["cor_fundo"] = "#EAB308"; resp.append("✅ Fundo → Amarelo")
        elif "preto" in msg: c["cor_fundo"] = "#0F172A"; resp.append("✅ Fundo → Escuro")
        elif "branco" in msg: c["cor_fundo"] = "#F8FAFC"; resp.append("✅ Fundo → Branco")

    # Cores de letra
    if "letra" in msg or "cor do texto" in msg:
        if "branca" in msg: c["cor_texto"] = "#FFFFFF"; resp.append("✅ Letra → Branca")
        elif "preta" in msg: c["cor_texto"] = "#000000"; resp.append("✅ Letra → Preta")
        elif "dourada" in msg: c["cor_texto"] = "#FBBF24"; resp.append("✅ Letra → Dourada")
        elif "vermelha" in msg: c["cor_texto"] = "#EF4444"; resp.append("✅ Letra → Vermelha")

    # Tamanho
    if "maior" in msg or "aumentar" in msg:
        c["tamanho_fonte"] = min(80, c["tamanho_fonte"] + 10)
        resp.append(f"✅ Tamanho → {c['tamanho_fonte']}")
    if "menor" in msg or "diminuir" in msg:
        c["tamanho_fonte"] = max(20, c["tamanho_fonte"] - 10)
        resp.append(f"✅ Tamanho → {c['tamanho_fonte']}")

    # Tipo de peça
    if "fachada" in msg: c["tipo"] = "Fachada"; resp.append("✅ Formato → Fachada")
    if "placa" in msg: c["tipo"] = "Placa"; resp.append("✅ Formato → Placa")
    if "banner" in msg: c["tipo"] = "Banner"; resp.append("✅ Formato → Banner")
    if "cartão" in msg: c["tipo"] = "Cartão de Visita"; resp.append("✅ Formato → Cartão")
    if "adesivo" in msg: c["tipo"] = "Adesivo"; resp.append("✅ Formato → Adesivo")

    # Sombra
    if "sombra" in msg:
        if "tirar" in msg or "sem" in msg: c["sombra"] = False; resp.append("✅ Sombra desativada")
        else: c["sombra"] = True; resp.append("✅ Sombra ativada")

    # Descrição de imagem
    for alvo in ["imagem de", "cenário de", "fundo com"]:
        if alvo in msg:
            c["descricao_imagem"] = msg_texto.split(alvo)[-1].strip()
            resp.append(f"✅ Cena registrada! Agora digite: **criar imagem**")
            break

    # Gerar imagem
    if "criar imagem" in msg or "gerar imagem" in msg:
        if c["descricao_imagem"]:
            resp.append("🎨 Desenhando... aguarde!")
            try:
                larg, alt = dimensoes[c["tipo"]]
                prompt = f"{c['descricao_imagem']}, sinalização comercial, cores vivas, alta qualidade, sem texto"
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width={larg}&height={alt}&nologo=true"
                r = requests.get(url, timeout=90)
                if r.status_code == 200:
                    st.session_state.imagem_gerada = Image.open(io.BytesIO(r.content))
                    resp.append("✅ Imagem pronta! Vá em 'Resultado'")
                else:
                    resp.append("⚠️ Sem conexão — envie sua foto")
            except:
                resp.append("⚠️ Tente mais tarde ou envie sua foto")
        else:
            resp.append("⚠️ Primeiro descreva: 'imagem de praia com coqueiros'")

    if not resp:
        resp.append("💡 Exemplos: fundo azul | texto é Loja do Zé | letra dourada | imagem de praia | criar imagem")
    return resp

# ====================== BARRA LATERAL ======================
st.sidebar.markdown("## 👑 LUMINA IA")
st.sidebar.markdown(f"**Admin:** {ADM_NOME}")
st.sidebar.divider()
st.sidebar.markdown("### 💳 Recebimento")
st.sidebar.info(f"**PIX:**\n`{ADM_PIX}`")
st.sidebar.divider()
st.sidebar.markdown("### ⚙️ Atalhos")
st.sidebar.markdown("""
- `fundo azul`
- `texto é ...`
- `letra dourada`
- `aumentar letra`
- `imagem de ...`
- `criar imagem`
""")
st.sidebar.divider()
if st.sidebar.button("🚪 SAIR DO SISTEMA", use_container_width=True):
    st.session_state.adm_logado = False
    st.rerun()

# ====================== ÁREA PRINCIPAL ======================
st.header("✨ Painel de Controle")
st.markdown("---")

aba1, aba2, aba3 = st.tabs([
    "💬 Comandos",
    "📷 Usar Minha Foto",
    "👁️ Resultado e Download"
])

# ABA 1 — COMANDOS
with aba1:
    st.subheader("Fale com o sistema")
    st.info("Digite o que quer e eu faço automaticamente")
    
    # Histórico
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["funcao"]):
            st.write(msg["texto"])
    
    # Entrada
    fala = st.chat_input("O que você precisa?")
    if fala:
        st.session_state.mensagens.append({"funcao": "usuario", "texto": fala})
        for resposta in processar_comando(fala):
            st.session_state.mensagens.append({"funcao": "assistente", "texto": resposta})
        st.rerun()

# ABA 2 — FOTO
with aba2:
    st.subheader("Envie sua própria imagem")
    foto = st.file_uploader("Escolha do celular", type=["jpg", "jpeg", "png"])
    if foto:
        st.session_state.foto_usuario = foto
        st.success("✅ Imagem carregada com sucesso!")
        st.image(foto, width=400, caption="Sua imagem")

# ABA 3 — RESULTADO
with aba3:
    c = st.session_state.config
    st.subheader("Projeto Final")
    
    if not c["texto"]:
        st.info("💬 Vá em 'Comandos' e diga: **texto é Nome da Sua Loja**")
    else:
        larg, alt = dimensoes[c["tipo"]]
        
        # Escolhe base
        if st.session_state.imagem_gerada:
            img = st.session_state.imagem_gerada.resize((larg, alt))
            st.info("🖼️ Imagem criada pela IA")
        elif st.session_state.foto_usuario:
            img = Image.open(st.session_state.foto_usuario).convert("RGB").resize((larg, alt))
            st.info("📷 Usando sua imagem")
        else:
            img = Image.new("RGB", (larg, alt), c["cor_fundo"])
            st.info("🎨 Cor de fundo selecionada")
        
        # Desenha texto
        desenho = ImageDraw.Draw(img)
        try:
            fonte = ImageFont.truetype("arial.ttf", c["tamanho_fonte"])
        except:
            fonte = ImageFont.load_default()
        
        bbox = desenho.textbbox((0, 0), c["texto"], font=fonte)
        lar_texto = bbox[2] - bbox[0]
        alt_texto = bbox[3] - bbox[1]
        x = (larg - lar_texto) // 2
        y = (alt - alt_texto) // 2
        
        if c["sombra"]:
            desenho.text((x+2, y+2), c["texto"], fill="#000000", font=fonte)
        desenho.text((x, y), c["texto"], fill=c["cor_texto"], font=fonte)
        
        st.image(img, caption=f"{c['tipo']} — {c['texto']}", use_column_width=True)
        
        # Download
        saida = io.BytesIO()
        img.save(saida, "PNG")
        saida.seek(0)
        st.download_button(
            label="📥 BAIXAR PROJETO FINAL",
            data=saida,
            file_name=f"{c['tipo']}_{c['texto'].replace(' ', '_')}.png",
            mime="image/png",
            type="primary",
            use_container_width=True
        )
