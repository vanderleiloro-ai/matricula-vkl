import streamlit as st
from datetime import date
import re

# Configuração da Página
st.set_page_config(page_title="Matrícula VKL", page_icon="⚽", layout="centered")

# --- FUNÇÕES DE VALIDAÇÃO E LÓGICA ---

def validar_telefone(telefone):
    numeros = re.sub(r'\D', '', telefone)
    return len(numeros) >= 10 and len(numeros) <= 11

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def calcular_categoria(nascimento):
    ano_atual = date.today().year
    idade_referencia = ano_atual - nascimento.year
    if idade_referencia <= 7: return "Sub-7"
    elif idade_referencia <= 9: return "Sub-9"
    elif idade_referencia <= 11: return "Sub-11"
    elif idade_referencia <= 13: return "Sub-13"
    elif idade_referencia <= 15: return "Sub-15"
    else: return "Sub-17 / Adulto"

# --- ESTILIZAÇÃO CUSTOMIZADA (MARCA D'ÁGUA VKL) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #ffffff;
        /* A logo se repete e a opacidade é controlada pelo linear-gradient branco por cima */
        background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                          url("https://www.vklassociacao.com.br/images/logo.png");
        background-repeat: repeat;
        background-size: 200px; 
        background-attachment: fixed;
    }}
    
    .section-header {{
        background-color: #003366;
        color: #ffffff;
        padding: 10px 15px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 5px solid #FFD700;
        font-size: 18px;
    }}

    /* Estilo para destacar a Categoria Sugerida fora do form */
    .cat-box {{
        background-color: #FFD700;
        color: #003366;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        border: 2px solid #003366;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", use_column_width=True)

st.title("⚽ Cadastro para Matrícula")

# --- ÁREA DE CÁLCULO DINÂMICO (FORA DO FORMULÁRIO PARA ATUALIZAR NA HORA) ---
st.markdown('<div class="section-header">📅 DEFINA A IDADE PARA VER A CATEGORIA</div>', unsafe_allow_html=True)
nasc_aluno = st.date_input("Data de Nascimento do Aluno*", 
                           value=date(2015, 1, 1),
                           format="DD/MM/YYYY", 
                           min_value=date(2005, 1, 1))

categoria_atual = calcular_categoria(nasc_aluno)
st.markdown(f'<div class="cat-box">CATEGORIA SUGERIDA: {categoria_atual}</div>', unsafe_allow_html=True)

# --- INÍCIO DO FORMULÁRIO ---
with st.form("form_vkl_final"):
    
    st.markdown('<div class="section-header">📍 1. UNIDADE E ORIGEM</div>', unsafe_allow_html=True)
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    with col_u2:
        origem = st.selectbox("Como conheceu a nossa escola?", 
                             ["Indicação", "Facebook", "Instagram", "Pesquisa na Web", "Outros"])

    st.markdown('<div class="section-header">🏃 2. DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    col_at1, col_at2 = st.columns(2)
    with col_at1:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    with col_at2:
        posicao = st.selectbox("Posição", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])

    st.markdown('<div class="section-header">👨‍👩‍👦 3. DADOS DOS PAIS</div>', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nome_pai = st.text_input("Nome do Pai")
        tel_pai = st.text_input("Telefone do Pai")
    with col_p2:
        nome_mae = st.text_input("Nome da Mãe")
        tel_mae = st.text_input("Telefone da Mãe")

    st.markdown('<div class="section-header">💰 4. RESPONSÁVEL FINANCEIRO</div>', unsafe_allow_html=True)
    res_fin_nome = st.text_input("Nome Completo do Responsável*")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        res_fin_cpf = st.text_input("CPF do Responsável*")
    with col_f2:
        res_fin_tel = st.text_input("WhatsApp do Responsável*")
    with col_f3:
        parentesco = st.selectbox("Parentesco*", ["Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Outro"])

    st.markdown('<div class="section-header">📋 5. SAÚDE E TERMOS</div>', unsafe_allow_html=True)
    saude_obs = st.text_area("Restrições médicas/Alergias (Opcional)")
    aceite_imagem = st.checkbox("Autorizo o uso de imagem do aluno para divulgação VKL.*")
    aceite_saude = st.checkbox("Declaro que o aluno está apto para esportes.*")

    enviar = st.form_submit_button("ENVIAR MATRÍCULA AGORA")

    if enviar:
        erros = []
        if not nome_aluno or not res_fin_nome or not res_fin_cpf or not res_fin_tel:
            erros.append("Preencha todos os campos obrigatórios (*).")
        if not validar_cpf(res_fin_cpf):
            erros.append("O CPF informado é inválido.")
        if not validar_telefone(res_fin_tel):
            erros.append("O telefone do Responsável é inválido.")
        if not aceite_imagem or not aceite_saude:
            erros.append("Você precisa aceitar os termos obrigatórios.")

        if erros:
            for e in erros: st.error(f"❌ {e}")
        else:
            st.success(f"✅ Sucesso! {nome_aluno} foi pré-inscrito na categoria {categoria_atual}.")
            st.balloons()
