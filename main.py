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

# --- ESTILIZAÇÃO CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)), url("data:image/png;base64,{bin_str if bin_str else ''}"); background-attachment: fixed; }}
    .section-header {{ background-color: #003366; color: #ffffff; padding: 5px 12px; border-radius: 5px; font-weight: bold; margin-top: 15px; border-left: 5px solid #FFD700; font-size: 14px; }}
    .cat-box {{ background-color: #FFD700; color: #003366; padding: 5px; border-radius: 8px; text-align: center; border: 1.5px solid #003366; margin: 5px 0; width: 150px; }}
    .cat-text {{ font-size: 10px; display: block; margin-bottom: -3px; }}
    .cat-val {{ font-size: 16px; font-weight: bold; }}
    label {{ color: #003366 !important; font-weight: bold !important; font-size: 12px !important; }}
    
    div[data-testid="stFormSubmitButton"] > button {{ 
        width: 100%; background: #003366 !important; color: #FFD700 !important; 
        height: 40px; font-size: 16px; font-weight: bold; border-radius: 8px; 
        border: 2px solid #FFD700 !important; transition: 0.3s;
    }}
    div[data-testid="stFormSubmitButton"] > button:hover {{ 
        background: #FFD700 !important; color: #003366 !important; border: 2px solid #003366 !important;
    }}
    .btn-home {{ 
        display: block; width: 100%; text-align: center; background-color: #ffffff; 
        color: #003366; padding: 10px; border-radius: 8px; text-decoration: none; 
        font-weight: bold; border: 2px solid #003366; transition: 0.3s; margin-top: 10px;
    }}
    .btn-home:hover {{ background-color: #003366; color: #FFD700; }}
    </style>
    """, unsafe_allow_html=True)

# --- CONTEÚDO ---
st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=80)
st.markdown("<h4 style='color: #003366;'>Ficha de Inscrição Oficial VKL</h4>", unsafe_allow_html=True)

st.markdown('<div class="section-header">🔐 IDENTIFICAÇÃO E UNIDADE</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: login_user = st.text_input("Login*")
with c2: senha_user = st.text_input("Senha*", type="password")
with c3: unidade_vkl = st.selectbox("Unidade*", ["--- Selecione ---", "Guaratuba", "Garuva", "Itapoá"])

c4, c5 = st.columns([2, 1])
with c4: nasc_aluno = st.date_input("Nascimento*", value=date(2015, 1, 1), format="DD/MM/YYYY")
with c5: 
    turma = calcular_categoria(nasc_aluno)
    st.markdown(f'<div class="cat-box"><span class="cat-text">Turma sugerida</span><span class="cat-val">{turma}</span></div>', unsafe_allow_html=True)

with st.form("vkl_form_v8"):
    st.markdown('<div class="section-header">🏃 ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    a1, a2, a3 = st.columns(3)
    with a1: cpf_aluno = st.text_input("CPF (Aluno/Resp)*")
    with a2: cel_aluno = st.text_input("Celular Aluno")
    with a3: sexo = st.selectbox("Sexo*", ["--- Selecione ---", "Masculino", "Feminino"])

    t1, t2, t3 = st.columns(3)
    with t1: pos = st.selectbox("Posição*", ["--- Selecione ---", "Goleiro", "Fixo", "Ala", "Pivô", "A definir"])
    with t2: lat = st.selectbox("Lateralidade*", ["--- Selecione ---", "Destro", "Canhoto", "Ambidestro"])
    with t3: hor = st.selectbox("Horário*", ["--- Selecione ---", "Manhã", "Tarde", "Noite"])

    st.markdown('<div class="section-header">🏠 ENDEREÇO</div>', unsafe_allow_html=True)
    rua = st.text_input("Rua/Av*")
    e1, e2, e3 = st.columns([1, 2, 2])
    with e1: num = st.text_input("Nº*")
    with e2: bairro = st.text_input("Bairro*")
    with e3: cep = st.text_input("CEP*")
    
    e4, e5 = st.columns(2)
    with e4: est = st.selectbox("Estado*", ["--- Selecione ---", "PR", "SC", "Outro"])
    with e5: cid = st.text_input("Cidade*")

    st.markdown('<div class="section-header">👪 FILIAÇÃO E FINANCEIRO</div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1: st.text_input("Nome Pai"); st.text_input("Cel Pai")
    with f2: st.text_input("Nome Mãe"); st.text_input("Cel Mãe")
    
    res_nome = st.text_input("Nome Resp. Financeiro*")
    r1, r2, r3 = st.columns(3)
    with r1: res_cpf = st.text_input("CPF Resp*")
    with r2: res_cel = st.text_input("Cel Resp*")
    with r3: res_par = st.selectbox("Parentesco*", ["--- Selecione ---", "Pai/Mãe", "Avô/ã", "Outro"])

    st.markdown('<div class="section-header">📝 OBSERVAÇÕES E TERMOS</div>', unsafe_allow_html=True)
    st.text_area("Observações", height=70)
    st.file_uploader("Documentos (Opcional)", accept_multiple_files=True)
    
    aceite1 = st.checkbox("Saúde em dia.*")
    aceite2 = st.checkbox("Uso de imagem.*")

    if st.form_submit_button("CONCLUIR MATRÍCULA"):
        if "--- Selecione ---" in [unidade_vkl, sexo, pos, lat, hor, est, res_par] or not nome_aluno:
            st.error("❌ Preencha todos os campos obrigatórios e selecione as opções.")
        else:
            st.success(f"⚽ Bem-vindos! Matrícula de {nome_aluno} realizada!")
            st.balloons()
            st.markdown(f'<a href="https://www.vklassociacao.com.br" target="_self" class="btn-home">VOLTAR À HOME</a>', unsafe_allow_html=True)
