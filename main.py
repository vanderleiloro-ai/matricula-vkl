import streamlit as st
from datetime import date
import re
import requests
import base64

# Configuração da Página
st.set_page_config(page_title="Cadastro Oficial VKL", page_icon="⚽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO ---
def get_base64_img(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except: return None

url_fundo = "https://www.vklassociacao.com.br/images/site/vkl.png"
bin_str = get_base64_img(url_fundo)

# --- FUNÇÕES DE APOIO ---
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', str(cpf))
    return len(cpf) == 11

def calcular_categoria(nascimento):
    idade = date.today().year - nascimento.year
    if idade <= 7: return "Sub-7"
    elif idade <= 9: return "Sub-9"
    elif idade <= 11: return "Sub-11"
    elif idade <= 13: return "Sub-13"
    elif idade <= 15: return "Sub-15"
    else: return "Sub-17 / Adulto"

# --- ESTILIZAÇÃO CSS REFINADA ---
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)), url("data:image/png;base64,{bin_str if bin_str else ''}"); background-attachment: fixed; }}
    .section-header {{ background-color: #003366; color: #ffffff; padding: 5px 12px; border-radius: 5px; font-weight: bold; margin-top: 15px; border-left: 5px solid #FFD700; font-size: 15px; }}
    
    /* Caixa de Turma Compacta */
    .cat-box {{ 
        background-color: #FFD700; color: #003366; padding: 5px; border-radius: 8px; 
        text-align: center; border: 1.5px solid #003366; margin: 5px 0; 
    }}
    .cat-text {{ font-size: 11px; display: block; margin-bottom: -5px; font-weight: normal; }}
    .cat-val {{ font-size: 18px; font-weight: bold; }}
    
    label {{ color: #003366 !important; font-weight: bold !important; font-size: 13px !important; }}
    
    /* Botões com Efeito Hover */
    div[data-testid="stFormSubmitButton"] > button {{ 
        width: 100%; background: #003366 !important; color: #FFD700 !important; 
        height: 40px; font-size: 16px; font-weight: bold; border-radius: 8px; 
        border: 2px solid #FFD700 !important; transition: 0.3s;
    }}
    div[data-testid="stFormSubmitButton"] > button:hover {{ 
        background: #FFD700 !important; color: #003366 !important; 
        border: 2px solid #003366 !important;
    }}

    .btn-home {{ 
        display: block; width: 100%; text-align: center; background-color: #ffffff; 
        color: #003366; padding: 10px; border-radius: 8px; text-decoration: none; 
        font-weight: bold; border: 2px solid #003366; transition: 0.3s; margin-top: 10px;
    }}
    .btn-home:hover {{ background-color: #003366; color: #FFD700; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo, col_titulo = st.columns([1, 3])
with col_logo: st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=100)
with col_titulo: st.markdown("<h3 style='color: #003366; margin-top: 15px;'>Ficha de Inscrição Oficial VKL</h3>", unsafe_allow_html=True)

# --- ACESSO E TURMA ---
st.markdown('<div class="section-header">🔐 IDENTIFICAÇÃO E UNIDADE</div>', unsafe_allow_html=True)
col_l, col_s, col_u = st.columns(3)
with col_l: login_user = st.text_input("Login (Único)*")
with col_s: senha_user = st.text_input("Senha*", type="password")
with col_u: unidade_vkl = st.selectbox("Unidade*", ["--- Selecione ---", "Guaratuba", "Garuva", "Itapoá"])

col_n, col_c = st.columns([2, 1])
with col_n: nasc_aluno = st.date_input("Nascimento do Aluno*", value=date(2015, 1, 1), format="DD/MM/YYYY")
with col_c: 
    turma_sugerida = calcular_categoria(nasc_aluno)
    st.markdown(f'<div class="cat-box"><span class="cat-text">Turma sugerida</span><span class="cat-val">{turma_sugerida}</span></div>', unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vkl_final_v7"):
    st.markdown('<div class="section-header">🏃 DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    
    col_a1, col_a2, col_a3 = st.columns([1.5, 1.5, 1])
    with col_a1: cpf_aluno = st.text_input("CPF (Aluno ou Resp.)*")
    with col_a2: cel_aluno = st.text_input("Celular Aluno")
    with col_a3: sexo_aluno = st.selectbox("Sexo*", ["--- Selecione ---", "Masculino", "Feminino"])

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1: posicao = st.selectbox("Posição*", ["--- Selecione ---", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô", "A definir"])
    with col_t2: lateral = st.selectbox("Lateralidade*", ["--- Selecione ---", "Destro", "Canhoto", "Ambidestro"])
    with col_t3: horario = st.selectbox("Horário*", ["--- Selecione ---", "Manhã", "Tarde", "Noite"])

    st.markdown('<div class="section-header">🏠 ENDEREÇO</div>', unsafe_allow_html=True)
    col_end1, col_end2 = st.columns([3, 1])
    with col_end1: rua = st.text_input("Rua/Av*")
    with col_end2: numero = st.text_input("Nº*")
    
    col_end3, col_end4, col_end5 = st.columns([1.5, 1.5, 1.5])
    with col_end3: bairro = st.text_input("Bairro*")
    with col_end4: cep = st.text_input("CEP*")
    with col_end5: comp = st.text_input("Compl.")
    
    col_end6, col_end7 = st.columns(2)
    with col_end6: est_res = st.selectbox("Estado*", ["--- Selecione ---", "PR", "SC", "Outro"])
    with col_end7: cid_res = st.text_input("Cidade*")

    st.markdown('<div class="section-header">👪 FILIAÇÃO E FINANCEIRO</div>', unsafe_allow_html=True)
    col_p, col_m = st.columns(2)
    with col_p: nome_pai = st.text_input("Nome do Pai"); tel_pai = st.text_input("Cel. Pai")
    with col_m: nome_mae = st.text_input("Nome da Mãe");
