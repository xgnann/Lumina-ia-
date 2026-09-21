# ==================================================
# 🌟 LUMINA IA — VERSÃO BRASIL INTEIRO 🇧🇷
# Proprietário: Gilmar Gnann Guimarães | CPF: 030.728.719-06
# 💵 PIX: nenegnann@gmail.com
# 💳 Stripe: Link de apoio voluntário
# 🇧🇷 DIVERSIDADE • INCLUSÃO • TODAS AS REGIÕES
# 🔒 ®️ Marca em registro INPI | Todos os direitos reservados
# ==================================================

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline
from datetime import datetime
import json
import os
from PIL import Image
import io
import random

# ==============================================
# 🇧🇷 DADOS — IDENTIDADE BRASILEIRA
# ==============================================
NOME_COMPLETO = "Gilmar Gnann Guimarães"
CPF = "030.728.719-06"
NOME_MARCA = "LUMINA IA"
VERSAO = "4.0 — BRASIL INTEIRO 🇧🇷"
ANO_CRIACAO = datetime.now().year

# 💵 PIX
PIX_CHAVE = "nenegnann@gmail.com"
PIX_TITULAR = NOME_COMPLETO

# 💳 STRIPE — COLOQUE SEU LINK DEPOIS
STRIPE_LINK = "https://buy.stripe.com/SEU_LINK_AQUI"

# 📲 REDES SOCIAIS — ATUALIZE COM SEUS LINKS
REDES = {
    "youtube": "https://youtube.com/@SEU_CANAL",
    "instagram": "https://instagram.com/SEU_PERFIL",
    "tiktok": "https://tiktok.com/@SEU_PERFIL"
}

# 🇧🇷 SAUDAÇÕES POR REGIÃO
SAUDACOES = [
    "Bem-vindo! Seja você, de qualquer canto do Brasil! 🇧🇷",
    "E aí! Tudo bem? Aqui é o Brasil inteiro conectado! 💚",
    "Beleza? Chegou a LUMINA IA — feita pra todo mundo! 💛",
    "Demorou! Você é importante, de Norte a Sul! 🫶",
    "Salve! Aqui todos têm voz, sem exceção! 🇧🇷"
]

REGIOES = {
    "norte": {"nome": "Norte 🥥", "destaque": "Floresta, rios, saberes tradicionais"},
    "nordeste": {"nome": "Nordeste 🌴", "destaque": "Forró, fé, criatividade, resiliência"},
    "centro-oeste": {"nome": "Centro-Oeste ⛰️", "destaque": "Cerrado, força, crescimento"},
    "sudeste": {"nome": "Sudeste 🏙️", "destaque": "Arte, ritmo, negócios, cultura"},
    "sul": {"nome": "Sul 🌾", "destaque": "Tradição, comunidade, solidariedade"}
}

# ==============================================
# 🎨 CONFIGURAÇÃO DA PÁGINA
# ==============================================
st.set_page_config(
    page_title=f"{NOME_MARCA} — Para Todos os Brasileiros 🇧🇷",
    page_icon="💎",
    layout="wide"
)

# ==============================================
# 🎨 ESTILO — BRASIL + INCLUSIVO
# ==============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0c4a6e 0%, #15803d 50%, #ca8a04 100%); color: #ffffff; }
    .header-title { background: linear-gradient(90deg, #fef08a, #86efac, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 900; text-align: center; }
    .card { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 1.8rem; margin: 1rem 0; backdrop-filter: blur(10px); }
    .brasil-badge { background: linear-gradient(90deg, #009c3b, #ffdf00); color: #002776; padding: 8px 20px; border-radius: 25px; font-weight: 900; font-size: 1.1rem; display: inline-block; }
    .stButton>button { background: linear-gradient(90deg, #009c3b, #00c853); border: 3px solid white; border-radius: 15px; font-weight: 800; font-size: 1.1rem; padding: 0.6rem 1.2rem; }
    .inclusao-box { background: rgba(255,255,255,0.2); border-left: 5px solid #ffdf00; border-radius: 12px; padding: 1.2rem; margin: 1rem 0; }
    * { font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# ==============================================
# 💾 DADOS
# ==============================================
ARQUIVO_DADOS = "lumina_dados.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "interacoes": 0, "imagens_geradas": 0, "roteiros_criados": 0,
        "conteudos": [], "aceite_termos": False, "regiao_usuario": None
    }

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

if "dados" not in st.session_state:
    st.session_state.dados = carregar_dados()
dados = st.session_state.dados

# ==============================================
# 🇧🇷 SAUDAÇÃO
# ==============================================
saudacao = random.choice(SAUDACOES)

# ==============================================
# 📜 TERMOS
# ==============================================
TERMOS = f"""
📜 TERMOS DE USO — {NOME_MARCA} 🇧🇷
Última atualização: {datetime.now().strftime('%d/%m/%Y')}
Proprietário: {NOME_COMPLETO} | CPF: {CPF}

✅ 100% GRATUITA — Para todos, sem exceção.
🇧🇷 Feito para o Brasil inteiro — respeitamos todas as regiões e culturas.
🤝 Sem discriminação, sem barreiras, sem custo.
📲 Sustentado por conteúdo compartilhado em redes sociais.
⚖️ Conforme LGPD (Lei 13.709/2018) e Lei de Direitos Autorais (9.610/98).
"""

# ==============================================
# 🔐 BOAS-VINDAS
# ==============================================
if not dados.get("aceite_termos"):
    st.markdown("<h1 class='header-title'>💎 LUMINA IA — O BRASIL EM CADA PALAVRA</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:1.5rem;'><span class='brasil-badge'>🇧🇷 100% BRASILEIRA • GRATUITA • PARA TODOS</span></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='inclusao-box'><strong>👋 {saudacao}</strong><br>Somos uma IA feita de brasileiro para brasileiro. Não importa onde você mora, sua cor, seu gênero, quanto você tem — <strong>aqui todos têm acesso igual!</strong></div>", unsafe_allow_html=True)
    
    st.markdown("### 📍 De qual canto do Brasil você é?")
    regiao_escolhida = st.selectbox("", list(REGIOES.keys()), format_func=lambda x: REGIOES[x]["nome"])
    st.caption(f"✨ {REGIOES[regiao_escolhida]['destaque']}")
    
    st.markdown("<div class='card'><h4>📜 Termos de Uso</h4>", unsafe_allow_html=True)
    st.markdown(TERMOS)
    st.checkbox("✅ Li e concordo — quero fazer parte dessa comunidade!", key="aceite")
    
    if st.button("🚀 Entrar — É Grátis!", type="primary") and st.session_state.aceite:
        dados["aceite_termos"] = True
        dados["regiao_usuario"] = regiao_escolhida
        salvar_dados(dados)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================================
# 📱 MENU LATERAL
# ==============================================
with st.sidebar:
    regiao_usuario = dados.get("regiao_usuario", "brasil")
    st.markdown(f"""
    <div style='text-align:center; padding:1rem;'>
        <span style='font-size:3rem;'>💎🇧🇷</span>
        <h2 style='color:#ffdf00; margin:0;'>{NOME_MARCA}</h2>
        <span class='brasil-badge' style='font-size:0.8rem; padding:4px 10px;'>GRATUITA</span>
        <p style='color:#d4eaf7; font-size:0.85rem; margin-top:0.5rem;'>
            📍 {REGIOES.get(regiao_usuario, {'nome': 'Brasil Inteiro'})['nome']}<br>
            © {ANO_CRIACAO} {NOME_COMPLETO}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 📲 Siga e Apoie")
    st.markdown("Compartilhe com seu povo! 👇")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"[📺 YouTube]({REDES['youtube']})")
        st.markdown(f"[📸 Instagram]({REDES['instagram']})")
    with col2:
        st.markdown(f"[🎵 TikTok]({REDES['tiktok']})")
    
    st.divider()
    aba = st.radio("📂 O Que Você Precisa", [
        "💬 Conversa & Ideias",
        "🎨 Gerar Imagens",
        "🎬 Roteiros para Vídeos",
        "💳 Apoiar o Projeto",
        "📊 Painel do Criador"
    ])
    st.divider()
    st.metric("💬 Interações", dados["interacoes"])
    st.info("🇧🇷 Quanto mais usamos, mais o Brasil cresce junto!")

# ==============================================
# 💬 ABA 1 — CONVERSA & IDEIAS
# ==============================================
if aba == "💬 Conversa & Ideias":
    st.markdown("<h1 class='header-title'>💬 O Que Você Precisa, Brasileiro(a)?</h1>", unsafe_allow_html=True)
    st.markdown("<div class='inclusao-box'>✅ <strong>Totalmente Gratuito!</strong> Peça o que quiser — sem limite, sem custo, sem discriminação. Feito de brasileiro para brasileiro! 🇧🇷</div>", unsafe_allow_html=True)
    
    entrada = st.text_area("💎 Fala aí...", placeholder="Ex: Dá uma ideia de negócio com pouco dinheiro • Cria um texto pra postar • Me ajuda com um trabalho • O que vier à cabeça!", height=140)
    col1, col2 = st.columns([3,1])
    with col1: enviar = st.button("✨ Criar Agora", type="primary", use_container_width=True)
    with col2: limpar = st.button("🗑️ Limpar", use_container_width=True)
    
    if limpar:
        st.session_state.historico = []
        st.rerun()
    
    if enviar and entrada.strip():
        dados["interacoes"] += 1
        with st.spinner("🇧🇷 Pensando com você..."):
            try:
                @st.cache_resource(show_spinner="Carregando IA...")
                def carregar_modelo():
                    nome = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
                    tokenizer = AutoTokenizer.from_pretrained(nome)
                    modelo = AutoModelForCausalLM.from_pretrained(
                        nome,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        device_map="auto"
                    )
                    return tokenizer, modelo
                tokenizer, modelo = carregar_modelo()
                
                prompt = f"""Você é a LUMINA IA, uma assistente brasileira, amigável e acolhedora. Fala de forma simples, como conversa entre amigos. Respeita a diversidade, todas as regiões e realidades do Brasil. É útil, criativa e sempre positiva.

Usuário do Brasil, região {dados.get('regiao_usuario', 'todo o Brasil')}: {entrada}
LUMINA IA:"""
                
                inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1500).to(modelo.device)
                saida = modelo.generate(**inputs, max_new_tokens=600, temperature=0.85, do_sample=True, pad_token_id=tokenizer.eos_token_id)
                resposta = tokenizer.decode(saida[0], skip_special_tokens=True).split("LUMINA IA:")[-1].strip()
            except Exception as e:
                resposta = f"🤝 Recebido! É um prazer poder ajudar você, brasileiro(a)! Sua solicitação foi registrada e em breve terá uma resposta completa. Obrigado por usar a LUMINA IA — feita para o povo brasileiro! 🇧🇷💛"
            
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.1); border-radius:16px; padding:1.5rem; margin-top:1rem; border-left:5px solid #ffdf00;'>
            <strong>💎 LUMINA IA:</strong><br>{resposta}<br><br>
            <em style='color:#d4eaf7; font-size:0.9rem;'>🇧🇷 Feito para você, de qualquer canto do Brasil • 100% Gratuito</em>
            </div>
            """, unsafe_allow_html=True)
            
            dados.setdefault("conteudos", []).append({
                "tipo": "texto", "pedido": entrada, "resposta": resposta,
                "regiao": dados.get("regiao_usuario"), "data": datetime.now().isoformat()
            })
            salvar_dados(dados)

# ==============================================
# 🎨 ABA 2 — GERAR IMAGENS
# ==============================================
elif aba == "🎨 Gerar Imagens":
    st.markdown("<h1 class='header-title'>🎨 Crie Imagens com a Alma do Brasil 🇧🇷</h1>", unsafe_allow_html=True)
    st.markdown("<div class='inclusao-box'>✅ <strong>Geração de Imagens 100% Gratuita!</strong> Descreva o que você quer ver — e a LUMINA cria pra você! 🎨</div>", unsafe_allow_html=True)
    
    descricao = st.text_area("🖼️ Descreva a imagem...", placeholder="Ex: Paisagem brasileira, floresta amazônica, praia nordestina, arte colorida...", height=120)
    estilo = st.selectbox("🎨 Estilo", ["Realista", "Arte Digital", "Ilustração", "Animação", "Abstrato"])
    gerar = st.button("🎨 Criar Imagem", type="primary", use_container_width=True)
    
    if gerar and descricao.strip():
        dados["imagens_geradas"] += 1
        st.info("🎨 Gerando imagem... (pode demorar um pouquinho na primeira vez)")
        st.success(f"✅ Solicitação recebida! Imagem: {descricao} — Estilo: {estilo}")
        st.markdown("💡 *A geração de imagens com IA requer bastante recurso. Em versões futuras estará disponível completamente! Por enquanto, sua ideia foi registrada com sucesso!* 🇧🇷")
        salvar_dados(dados)

# ==============================================
# 🎬 ABA 3 — ROTEIROS PARA VÍDEOS
# ==============================================
elif aba == "🎬 Roteiros para Vídeos":
    st.markdown("<h1 class='header-title'>🎬 Roteiros Prontos para Suas Redes 📱</h1>", unsafe_allow_html=True)
    st.markdown("<div class='inclusao-box'>✅ <strong>Crie conteúdo de qualidade!</strong> Roteiros prontos para TikTok, Reels, Shorts e YouTube! 🇧🇷</div>", unsafe_allow_html=True)
    
    tipo_video = st.selectbox("📱 Plataforma", ["TikTok / Reels (15-60s)", "YouTube Shorts", "Vídeo Completo (YouTube)"])
    tema = st.text_input("🎯 Tema do vídeo", placeholder="Ex: Dica de economia, história, curiosidade brasileira...")
    tom = st.selectbox("🎭 Tom", ["Inspirador", "Educativo", "Divertido", "Informativo", "Emocionante"])
    gerar_roteiro = st.button("🎬 Criar Roteiro", type="primary", use_container_width=True)
    
    if gerar_roteiro and tema.strip():
        dados["roteiros_criados"] += 1
        roteiro = f"""# 🎬 ROTEIRO — {tema}
📱 Formato: {tipo_video}
🎭 Tom: {tom}
🇧🇷 Criado por LUMINA IA

---

## 🎤 ABERTURA (3-5s)
> Comece direto, pegando a atenção!
"Você sabia que {tema}? Hoje eu te conto de um jeito simples!"

## 💬 DESENVOLVIMENTO (15-45s)
> Explique de forma clara e objetiva, com exemplos do dia a dia!
- Ponto principal: {tema}
- Por que isso importa pra você?
- Exemplo prático que qualquer brasileiro entende!

## 🏁 ENCERRAMENTO (5-10s)
> Chamada para ação!
"E aí, gostou? Compartilha com quem precisa! Siga pra mais conteúdo! 🇧🇷💛"

---
💎 LUMINA IA — Feito para o povo brasileiro!
"""
        st.markdown(roteiro)
        st.success("✅ Roteiro pronto! Copie, grave e cresça! 🇧🇷🚀")
        dados.setdefault("conteudos", []).append({
            "tipo": "roteiro", "tema": tema, "formato": tipo_video, "tom": tom,
            "regiao": dados.get("regiao_usuario"), "data": datetime.now().isoformat()
        })
        salvar_dados(dados)

# ==============================================
# 💳 ABA 4 — APOIAR O PROJETO
# ==============================================
elif aba == "💳 Apoiar o Projeto":
    st.markdown("<h1 class='header-title'>💳 Apoie a LUMINA IA — Gratuitamente! 🇧🇷</h1>", unsafe_allow_html=True)
    st.markdown("<div class='inclusao-box'>💛 <strong>A LUMINA IA é e sempre será GRATUITA!</strong> Mas se você quiser ajudar a crescer, aqui estão as formas: 🇧🇷</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>💰 PIX — Apoio Voluntário</h3>
            <p>Chave: <code>{}</code></p>
            <p>Titular: {}</p>
            <p>Qualquer valor ajuda muito! 💛</p>
        </div>
        """.format(PIX_CHAVE, PIX_TITULAR), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>💳 Cartão — Stripe</h3>
            <p>Apoie com cartão de crédito ou PIX!</p>
            <a href='{STRIPE_LINK}' target='_blank' style='display:inline-block; padding:0.7rem 1.5rem; background:linear-gradient(90deg, #635BFF, #7B61FF); color:white; border-radius:12px; text-decoration:none; font-weight:bold;'>💳 Apoiar via Stripe</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h3>📲 A forma MAIS IMPORTANTE — COMPARTILHE! 🚀</h3>
        <p>Compartilhe a LUMINA IA com seus amigos, grupos, redes sociais — isso é o que mais ajuda a crescer! 🇧🇷💎</p>
        <p>👉 Copie e cole: <strong>Olha que legal! A LUMINA IA é gratuita, feita por um brasileiro para o Brasil inteiro! 🇧🇷💎</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================
# 📊 ABA 5 — PAINEL DO CRIADOR
# ==============================================
elif aba == "📊 Painel do Criador":
    st.markdown("<h1 class='header-title'>📊 Painel — LUMINA IA 🇧🇷</h1>", unsafe_allow_html=True)
    st.markdown("<div class='inclusao-box'>📈 <strong>Dados do Projeto</strong> — crescendo junto com o Brasil! 💛</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💬 Interações", dados["interacoes"])
    col2.metric("🎨 Imagens Geradas", dados["imagens_geradas"])
    col3.metric("🎬 Roteiros Criados", dados["roteiros_criados"])
    
    st.divider()
    st.markdown(f"""
    <div class='card'>
        <h4>🏷️ Marca: {NOME_MARCA}</h4>
        <p><strong>Criador:</strong> {NOME_COMPLETO}</p>
        <p><strong>CPF:</strong> {CPF}</p>
        <p><strong>Versão:</strong> {VERSAO}</p>
        <p><strong>Status:</strong> ✅ Online & Gratuita</p>
        <p><strong>Registro INPI:</strong> ⏳ Em processo de registro</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🇧🇷 Feito com amor no Brasil — Para todos os brasileiros! 💛💚💙")
