import streamlit as st
from datetime import date
import re
import requests
import base64

# Configuração da Página
st.set_page_config(page_title="Matrícula VKL", page_icon="⚽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO (LOGO VKL) ---
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

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
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
        background-color: #003366; color: #ffffff; padding: 12px 15px;
        border-radius: 8px; font-weight: bold; margin-top: 20px;
        margin-bottom: 10px; border-left: 6px solid #FFD700; font-size: 18px;
    }}
    .cat-box {{
        background-color: #FFD700; color: #003366; padding: 15px;
        border-radius: 10px; text-align: center; font-weight: bold;
        font-size: 22px; border: 2px solid #003366;
    }}
    /* Estilo dos Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {{
        background-color: #fff9e6 !important; color: #003366 !important;
        border: 1px solid #FFD700 !important;
    }}
    /* Botão Enviar */
    div[data-testid="stFormSubmitButton"] > button {{
        width: 100% !important; background: linear-gradient(135deg, #003366 0%, #004a99 100%) !important;
        color: #FFD700 !important; height: 55px !important; font-size: 22px !important;
        font-weight: bold !important; border: 2px solid #FFD700 !important;
        border-radius: 12px !important; transition: 0.3s ease !important;
    }}
    div[data-testid="stFormSubmitButton"] > button:hover {{
        background: #FFD700 !important; color: #003366 !important;
        border: 2px solid #003366 !important;
    }}
    label {{ color: #003366 !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
c_logo1, c_logo2, c_logo3 = st.columns([1.5, 2, 1.5])
with c_logo2:
    st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=300)

st.markdown("<h1 style='text-align: center; color: #003366;'>⚽ Matrícula Escola de Futebol VKL</h1>", unsafe_allow_html=True)

# --- INÍCIO DO FORMULÁRIO ---
with st.form("form_vkl_completo"):
    
    # --- 1. ACESSO INDIVIDUAL ---
    st.markdown('<div class="section-header">🔑 1. ACESSO DO ALUNO (LOGIN ÚNICO)</div>', unsafe_allow_html=True)
    st.info("Utilize um Login exclusivo para cada filho matriculado.")
    
    col_l, col_s = st.columns(2)
    with col_l:
        login_usuario = st.text_input("Nome de Usuário (Login)*", placeholder="ex: pedro.silva")
    with col_s:
        senha_usuario = st.text_input("Criar Senha*", type="password")

    # --- 2. DADOS DO ALUNO E CATEGORIA ---
    st.markdown('<div class="section-header">📅 2. DADOS DO ALUNO E NASCIMENTO</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    
    col_n, col_g = st.columns(2)
    with col_n:
        nasc_aluno = st.date_input("Data de Nascimento*", value=date(2015, 1, 1), format="DD/MM/YYYY")
    with col_g:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    
    categoria_atual = calcular_categoria(nasc_aluno)
    st.markdown(f'<div class="cat-box">CATEGORIA SUGERIDA: {categoria_atual}</div>', unsafe_allow_html=True)

    # --- 3. UNIDADE E POSIÇÃO ---
    st.markdown('<div class="section-header">📍 3. UNIDADE E CAMPO</div>', unsafe_allow_html=True)
    col_u, col_p = st.columns(2)
    with col_u:
        unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    with col_p:
        posicao = st.selectbox("Posição de Preferência", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])

    # --- 4. RESPONSÁVEL FINANCEIRO ---
    st.markdown('<div class="section-header">💰 4. RESPONSÁVEL FINANCEIRO</div>', unsafe_allow_html=True)
    res_nome = st.text_input("Nome Completo do Responsável*")
    
    col_c, col_w = st.columns(2)
    with col_c:
        res_cpf = st.text_input("CPF do Responsável*")
    with col_w:
        res_tel = st.text_input("WhatsApp (DDD + Número)*")

    # --- BOTÃO DE ENVIO ---
    enviar = st.form_submit_button("CONCLUIR MATRÍCULA")

    if enviar:
        if not login_usuario or not senha_usuario or not nome_aluno or not res_nome or not res_cpf or not res_tel:
            st.error("❌ Preencha todos os campos obrigatórios (*).")
        elif not validar_cpf(res_cpf):
            st.error("❌ O CPF informado é inválido.")
        else:
            # URL do seu Google Forms (ajustar conforme novos campos forem adicionados)
            url_forms = "https://docs.google.com/forms/d/e/1FAIpQLSdyEy4VB4jQTzYdovJkXJUa_b4Y8rjlvbn5a1GthNmOzKYLRg/formResponse"
            
            # ATENÇÃO: Os 'entry.XXXX' abaixo precisam ser atualizados com o seu novo link preenchido
            dados_matricula = {
                "entry.666952651": nome_aluno,       # Nome do Aluno
                "entry.1010511222": unidade,         # Unidade
                "entry.1377162592": categoria_atual, # Categoria
                "entry.162643904": genero,           # Gênero
                # Adicione aqui os novos códigos para Login e Senha quando gerar o link
            }

            try:
                requests.post(url_forms, data=dados_matricula)
                st.success(f"✅ Matrícula de {nome_aluno} realizada com sucesso!")
                st.balloons()
            except:
                st.error("Erro técnico ao salvar. Tente novamente em instantes.")
