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
    if not nascimento:
        return "Aguardando data..."
    ano_atual = date.today().year
    idade_referencia = ano_atual - nascimento.year
    
    if idade_referencia <= 7: return "Sub-7"
    elif idade_referencia <= 9: return "Sub-9"
    elif idade_referencia <= 11: return "Sub-11"
    elif idade_referencia <= 13: return "Sub-13"
    elif idade_referencia <= 15: return "Sub-15"
    else: return "Sub-17 / Adulto"

# --- ESTILIZAÇÃO CUSTOMIZADA COM MARCA D'ÁGUA ---
# Nota: A imagem 'logo_fundo.png' deve estar na mesma pasta do código no GitHub
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #ffffff;
        background-image: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), url("https://www.vklassociacao.com.br/images/logo.png");
        background-repeat: repeat;
        background-size: 150px; /* Tamanho da logo no fundo */
        background-attachment: fixed;
    }}
    
    .section-header {{
        background-color: #003366;
        color: #ffffff;
        padding: 10px 15px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 5px solid #FFD700;
        font-size: 20px;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: rgba(253, 250, 240, 0.9) !important;
        border: 1px solid #FFD700 !important;
        border-radius: 8px !important;
    }}

    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #003366 0%, #004a99 100%) !important;
        color: #FFD700 !important;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #FFD700 !important;
        border-radius: 10px;
    }}
    
    .stButton>button:hover {{
        background: #FFD700 !important;
        color: #003366 !important;
        border: 2px solid #003366 !important;
    }}

    label {{ color: #003366 !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", use_column_width=True)

st.title("⚽ Formulário de Cadastro para Matrícula")
st.markdown("<p style='text-align: center; color: #666;'>Associação VKL - Escola de Futebol</p>", unsafe_allow_html=True)

with st.form("form_vkl_v3_4"):
    
    st.markdown('<div class="section-header">📍 1. UNIDADE E ORIGEM</div>', unsafe_allow_html=True)
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    with col_u2:
        origem = st.selectbox("Como conheceu a nossa escola?", 
                             ["Indicação", "Facebook", "Instagram", "Pesquisa na Web", "Outros"])

    st.markdown('<div class="section-header">🏃 2. DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        # Definindo um valor padrão mais antigo para forçar o recálculo
        nasc_aluno = st.date_input("Data de Nascimento*", 
                                   value=date(2015, 1, 1),
                                   format="DD/MM/YYYY", 
                                   min_value=date(2005, 1, 1))
    with c2:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    with c3:
        posicao = st.selectbox("Posição", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])
    
    # Cálculo em tempo real dentro do formulário
    categoria_texto = calcular_categoria(nasc_aluno)
    st.markdown(f"<div style='background-color: #FFD700; color: #003366; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;'>CATEGORIA SUGERIDA: {categoria_texto}</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-header">👨‍👩‍👦 3. DADOS DOS PAIS</div>', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nome_pai = st.text_input("Nome do Pai")
        tel_pai = st.text_input("Telefone/WhatsApp do Pai", placeholder="(00) 00000-0000")
    with col_p2:
        nome_mae = st.text_input("Nome da Mãe")
        tel_mae = st.text_input("Telefone/WhatsApp da Mãe", placeholder="(00) 00000-0000")

    st.markdown('<div class="section-header">💰 4. RESPONSÁVEL FINANCEIRO</div>', unsafe_allow_html=True)
    res_fin_nome = st.text_input("Nome Completo do Responsável Financeiro*")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        res_fin_cpf = st.text_input("CPF do Responsável*", placeholder="000.000.000-00")
    with col_f2:
        res_fin_tel = st.text_input("Telefone do Responsável*", placeholder="(00) 00000-0000")
    with col_f3:
        parentesco = st.selectbox("Grau de Parentesco*", ["Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Outro"])

    st.markdown('<div class="section-header">📋 5. SAÚDE E TERMOS</div>', unsafe_allow_html=True)
    saude_obs = st.text_area("O aluno possui alguma alergia ou restrição médica? (Opcional)")
    aceite_imagem = st.checkbox("Autorizo o uso de imagem do aluno para fins de divulgação da VKL.*")
    aceite_saude = st.checkbox("Declaro que o aluno está apto para a prática de esportes.*")

    st.markdown("<br>", unsafe_allow_html=True)
    enviar = st.form_submit_button("ENVIAR MATRÍCULA AGORA")

    if enviar:
        erros = []
        if not nome_aluno or not res_fin_nome or not res_fin_cpf or not res_fin_tel:
            erros.append("Preencha todos os campos obrigatórios (*).")
        if res_fin_cpf and not validar_cpf(res_fin_cpf):
            erros.append("O CPF informado é inválido.")
        if not validar_telefone(res_fin_tel):
            erros.append("O telefone do Responsável Financeiro é inválido.")
        if not aceite_imagem or not aceite_saude:
            erros.append("Você precisa aceitar os termos de imagem e saúde.")

        if erros:
            for erro in erros:
                st.error(f"❌ {erro}")
        else:
            st.success(f"✅ Inscrição enviada! Bem-vindos à família VKL.")
            st.balloons()
