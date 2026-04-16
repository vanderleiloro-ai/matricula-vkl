import streamlit as st
from datetime import date

# Configuração da Página
st.set_page_config(page_title="Matrícula VKL", page_icon="⚽", layout="centered")

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS AVANÇADO) ---
st.markdown(f"""
    <style>
    /* Fundo da página com degradê suave e marca d'água */
    .stApp {{
        background-color: #ffffff;
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
    }}
    
    /* Títulos das Seções com Caixa Azul VKL */
    .section-header {{
        background-color: #003366;
        color: #FFD700;
        padding: 10px 15px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 5px solid #FFD700;
        font-size: 20px;
    }}

    /* Estilização das caixas de entrada e seleção */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: #fdfaf0 !important; /* Fundo levemente dourado */
        border: 1px solid #FFD700 !important;
        border-radius: 8px !important;
    }}

    /* Botão de Envio Estilizado */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #003366 0%, #004a99 100%);
        color: #FFD700 !important;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #FFD700;
        border-radius: 10px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: #FFD700 !important;
        color: #003366 !important;
        transform: scale(1.02);
    }}

    /* Ajuste de labels */
    label {{ color: #003366 !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

def calcular_categoria(nascimento):
    ano_atual = date.today().year
    idade = ano_atual - nascimento.year
    if idade <= 7: return "Sub-7"
    elif idade <= 9: return "Sub-9"
    elif idade <= 11: return "Sub-11"
    elif idade <= 13: return "Sub-13"
    elif idade <= 15: return "Sub-15"
    else: return "Sub-17 / Adulto"

# --- TOPO DO FORMULÁRIO ---
# DICA: Se a imagem não abrir, você pode hospedar ela no seu próprio site e colar o link aqui.
st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=200)
st.title("⚽ Formulário de Cadastro para Matrícula")
st.markdown("<p style='color: #666;'>Associação VKL - Escola de Futebol</p>", unsafe_allow_html=True)

with st.form("form_vkl_v3"):
    
    # SEÇÃO 1
    st.markdown('<div class="section-header">📍 1. UNIDADE E ORIGEM</div>', unsafe_allow_html=True)
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    with col_u2:
        origem = st.selectbox("Como conheceu a nossa escola?", 
                             ["Indicação", "Facebook", "Instagram", "Pesquisa na Web", "Outros"])

    # SEÇÃO 2
    st.markdown('<div class="section-header">🏃 2. DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        nasc_aluno = st.date_input("Data de Nascimento*", format="DD/MM/YYYY", min_value=date(2005, 1, 1))
    with c2:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    with c3:
        posicao = st.selectbox("Posição", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])
    
    cat = calcular_categoria(nasc_aluno)
    st.markdown(f"<div style='background-color: #FFD700; color: #003366; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;'>CATEGORIA ESTIMADA: {cat}</div>", unsafe_allow_html=True)

    # SEÇÃO 3
    st.markdown('<div class="section-header">👨‍👩‍👦 3. DADOS DOS PAIS</div>', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nome_pai = st.text_input("Nome do Pai")
        tel_pai = st.text_input("Telefone/WhatsApp do Pai")
    with col_p2:
        nome_mae = st.text_input("Nome da Mãe")
        tel_mae = st.text_input("Telefone/WhatsApp da Mãe")

    # SEÇÃO 4
    st.markdown('<div class="section-header">💰 4. RESPONSÁVEL FINANCEIRO</div>', unsafe_allow_html=True)
    res_fin_nome = st.text_input("Nome Completo do Responsável Financeiro*")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        res_fin_cpf = st.text_input("CPF do Responsável*")
    with col_f2:
        res_fin_tel = st.text_input("Telefone do Responsável*")
    with col_f3:
        parentesco = st.selectbox("Grau de Parentesco*", ["Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Outro"])

    # SEÇÃO 5
    st.markdown('<div class="section-header">📋 5. SAÚDE E TERMOS</div>', unsafe_allow_html=True)
    saude_obs = st.text_area("O aluno possui alguma alergia ou restrição médica? (Opcional)")
    
    aceite_imagem = st.checkbox("Autorizo o uso de imagem do aluno para fins de divulgação da VKL.*")
    aceite_saude = st.checkbox("Declaro que o aluno está apto para a prática de esportes.*")

    # BOTÃO FINAL
    st.markdown("<br>", unsafe_allow_html=True)
    enviar = st.form_submit_button("ENVIAR MATRÍCULA AGORA")

    if enviar:
        if not nome_aluno or not res_fin_nome or not res_fin_cpf or not res_fin_tel or not aceite_imagem or not aceite_saude:
            st.error("❌ Por favor, preencha todos os campos obrigatórios e aceite os termos.")
        else:
            st.success(f"✅ Inscrição enviada! Seja bem-vindo à Família VKL.")
            st.balloons()
