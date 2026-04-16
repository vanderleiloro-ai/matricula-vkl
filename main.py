import streamlit as st
from datetime import date
import re
import requests
import base64

# Configuração da Página
st.set_page_config(page_title="Matrícula VKL", page_icon="⚽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO (BASE64) ---
def get_base64_img(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except:
        return None

url_fundo = "https://www.vklassociacao.com.br/images/site/vkl.png"
bin_str = get_base64_img(url_fundo)

# --- FUNÇÕES DE VALIDAÇÃO ---
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

# --- ESTILIZAÇÃO ---
if bin_str:
    bg_style = f"""
        background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), 
                    url("data:image/png;base64,{bin_str}");
        background-repeat: repeat !important;
        background-size: 100px !important; 
        background-attachment: fixed;
    """
else:
    bg_style = "background-color: #ffffff;"

st.markdown(f"""
    <style>
    .stApp {{ {bg_style} }}
    
    .section-header {{
        background-color: #003366;
        color: #ffffff;
        padding: 12px 15px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 6px solid #FFD700;
        font-size: 18px;
    }}

    .cat-box {{
        background-color: #FFD700;
        color: #003366;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        border: 2px solid #003366;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {{
        background-color: #fff9e6 !important;
        color: #003366 !important;
        border: 1px solid #FFD700 !important;
    }}

    div.stButton > button {{
        width: 100% !important;
        background: linear-gradient(135deg, #003366 0%, #004a99 100%) !important;
        color: #FFD700 !important;
        height: 55px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 2px solid #FFD700 !important;
        border-radius: 12px !important;
        transition: 0.3s !important;
    }}

    div.stButton > button:hover {{
        background: #FFD700 !important;
        color: #003366 !important;
        border: 2px solid #003366 !important;
    }}

    /* Estilo para o link de voltar que parece um botão */
    .btn-voltar {{
        display: inline-block;
        padding: 10px 20px;
        background-color: #003366;
        color: #FFD700 !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-top: 15px;
        border: 1px solid #FFD700;
    }}
    .btn-voltar:hover {{
        background-color: #FFD700;
        color: #003366 !important;
    }}

    label {{ color: #003366 !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
c_logo1, c_logo2, c_logo3 = st.columns([1.5, 2, 1.5])
with c_logo2:
    st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=300)

st.markdown("<h1 style='text-align: center; color: #003366;'>⚽ Cadastro para Matrícula</h1>", unsafe_allow_html=True)

# --- DATA E CATEGORIA ---
st.markdown('<div class="section-header">📅 1. INFORME A DATA DE NASCIMENTO</div>', unsafe_allow_html=True)
nasc_aluno = st.date_input("Data de Nascimento do Aluno*", 
                           value=date(2015, 1, 1),
                           format="DD/MM/YYYY", 
                           min_value=date(2005, 1, 1))

categoria_atual = calcular_categoria(nasc_aluno)
st.markdown(f'<div class="cat-box">CATEGORIA SUGERIDA: {categoria_atual}</div>', unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vkl_final"):
    st.markdown('<div class="section-header">📍 2. UNIDADE E ORIGEM</div>', unsafe_allow_html=True)
    unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    origem = st.selectbox("Como conheceu a nossa escola?", ["Indicação", "Facebook", "Instagram", "Pesquisa na Web", "Outros"])

    st.markdown('<div class="section-header">🏃 3. DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    col_at1, col_at2 = st.columns(2)
    with col_at1:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    with col_at2:
        posicao = st.selectbox("Posição", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])

    st.markdown('<div class="section-header">👨‍👩‍👦 4. DADOS DOS PAIS</div>', unsafe_allow_html=True)
    nome_pai = st.text_input("Nome do Pai")
    tel_pai = st.text_input("Telefone do Pai")
    nome_mae = st.text_input("Nome da Mãe")
    tel_mae = st.text_input("Telefone da Mãe")

    st.markdown('<div class="section-header">💰 5. RESPONSÁVEL FINANCEIRO</div>', unsafe_allow_html=True)
    res_fin_nome = st.text_input("Nome Completo do Responsável*")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        res_fin_cpf = st.text_input("CPF do Responsável*")
    with col_f2:
        res_fin_tel = st.text_input("WhatsApp do Responsável*")
    parentesco = st.selectbox("Parentesco*", ["Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Outro"])

    st.markdown('<div class="section-header">📋 6. SAÚDE E TERMOS</div>', unsafe_allow_html=True)
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
        
        if erros:
            for e in erros: st.error(f"❌ {e}")
        else:
            st.success(f"✅ Sucesso! Inscrição de {nome_aluno} enviada. Bem-vindos à família VKL!")
            st.balloons()
            
            # BOTÃO DE RETORNO APÓS O SUCESSO
            st.markdown("""
                <div style='text-align: center;'>
                    <a href='https://www.vklassociacao.com.br' class='btn-voltar'>
                        🏠 Voltar para a Página Principal da VKL
                    </a>
                </div>
            """, unsafe_allow_html=True)
