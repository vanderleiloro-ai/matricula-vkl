import streamlit as st
from datetime import date
import re
import requests
import base64

# Configuração da Página
st.set_page_config(page_title="Cadastro de Aluno VKL", page_icon="⚽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO ---
def get_base64_img(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except: return None

url_fundo = "https://www.vklassociacao.com.br/images/site/vkl.png"
bin_str = get_base64_img(url_fundo)

# --- ESTILIZAÇÃO CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.94), rgba(255, 255, 255, 0.94)), url("data:image/png;base64,{bin_str if bin_str else ''}"); background-attachment: fixed; }}
    
    /* Layout do Cabeçalho: Imagem fora, Título no Retângulo */
    .header-row {{
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 25px;
    }}
    .title-box {{
        background-color: #FFFFFF;
        padding: 15px 25px;
        border-radius: 8px;
        border-bottom: 4px solid #FFD700;
        flex-grow: 1;
    }}
    .header-title {{
        color: #FFD700;
        font-family: 'Arial Black', sans-serif;
        font-size: 24px;
        margin: 0;
        text-transform: uppercase;
        text-align: center;
    }}

    .section-header {{ background-color: #003366; color: #ffffff; padding: 5px 12px; border-radius: 5px; font-weight: bold; margin-top: 15px; border-left: 5px solid #FFD700; font-size: 14px; }}
    
    /* Turma Sugerida */
    .cat-box {{ background-color: #FFD700; color: #003366; padding: 8px; border-radius: 8px; text-align: center; border: 2px solid #003366; margin-top: 5px; }}
    .cat-text {{ font-size: 13px; font-weight: bold; display: block; }}
    .cat-val {{ font-size: 20px; font-weight: bold; display: block; line-height: 1.1; }}
    
    label {{ color: #003366 !important; font-weight: bold !important; font-size: 13px !important; }}
    
    /* Botões */
    div[data-testid="stFormSubmitButton"] > button {{ 
        width: 100%; background: #003366 !important; color: #FFD700 !important; 
        height: 50px; font-size: 18px; font-weight: bold; border-radius: 8px; 
        border: 2px solid #FFD700 !important; transition: 0.4s;
    }}
    div[data-testid="stFormSubmitButton"] > button:hover {{ 
        background: #FFD700 !important; color: #003366 !important; border: 2px solid #003366 !important;
    }}

    .btn-home {{ 
        display: block; width: 100%; text-align: center; background-color: #ffffff; 
        color: #003366; padding: 12px; border-radius: 8px; text-decoration: none; 
        font-weight: bold; border: 2px solid #003366; transition: 0.3s; margin-top: 15px;
    }}
    .btn-home:hover {{ background-color: #003366; color: #FFD700; }}

    /* Animação das Bolas */
    @keyframes dropBall {{
        0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 1; }}
        30% {{ transform: translateY(0) rotate(180deg); }}
        45% {{ transform: translateY(-120px) rotate(270deg); }}
        60% {{ transform: translateY(0) rotate(360deg); }}
        100% {{ transform: translateY(100vh) translateX(150px) rotate(720deg); opacity: 0; }}
    }}
    .soccer-ball {{ position: fixed; top: -50px; font-size: 35px; z-index: 9999; animation: dropBall 2.5s ease-in forwards; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="header-row">
        <img src="https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg" width="110">
        <div class="title-box">
            <h1 class="header-title">Cadastro de Aluno VKL</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ACESSO E TURMA ---
st.markdown('<div class="section-header">🔐 IDENTIFICAÇÃO E UNIDADE</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: login_user = st.text_input("Login (Único)*")
with c2: senha_user = st.text_input("Senha*", type="password")
with c3: unidade_vkl = st.selectbox("Unidade*", ["--- Selecione ---", "Guaratuba", "Garuva", "Itapoá"])

c4, c5 = st.columns([2, 1])
with c4: 
    # Data de nascimento com limite mínimo em 1960
    nasc_aluno = st.date_input("Data de Nascimento*", 
                               value=date(2015, 1, 1), 
                               min_value=date(1960, 1, 1), 
                               format="DD/MM/YYYY")
with c5: 
    def calc_cat(d):
        idade = date.today().year - d.year
        if idade <= 7: return "SUB-7"
        elif idade <= 9: return "SUB-9"
        elif idade <= 11: return "SUB-11"
        elif idade <= 13: return "SUB-13"
        elif idade <= 15: return "SUB-15"
        else: return "SUB-17/ADULTO"
    turma = calc_cat(nasc_aluno)
    st.markdown(f'<div class="cat-box"><span class="cat-text">Turma sugerida</span><span class="cat-val">{turma}</span></div>', unsafe_allow_html=True)

# --- FORMULÁRIO Master ---
with st.form("vkl_final_form"):
    st.markdown('<div class="section-header">🏃 DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    a1, a2, a3 = st.columns(3)
    with a1: cpf_aluno = st.text_input("CPF (Aluno/Resp)*")
    with a2: cel_aluno = st.text_input("Celular Aluno")
    with a3: sexo = st.selectbox("Sexo*", ["--- Selecione ---", "Masculino", "Feminino"])

    t1, t2, t3 = st.columns(3)
    with t1: pos = st.selectbox("Posição*", ["--- Selecione ---", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô", "A definir"])
    with t2: lat = st.selectbox("Lateralidade*", ["--- Selecione ---", "Destro", "Canhoto", "Ambidestro"])
    with t3: hor = st.selectbox("Horário*", ["--- Selecione ---", "Manhã", "Tarde", "Noite"])

    st.markdown('<div class="section-header">🏠 ENDEREÇO</div>', unsafe_allow_html=True)
    rua = st.text_input("Rua/Avenida*")
    e1, e2, e3 = st.columns([1, 2, 2])
    with e1: num = st.text_input("Nº*")
    with e2: bairro = st.text_input("Bairro*")
    with e3: cep = st.text_input("CEP*")
    
    e4, e5 = st.columns(2)
    with e4: est = st.selectbox("Estado*", ["--- Selecione ---", "PR", "SC", "Outro"])
    with e5: cid = st.text_input("Cidade*")

    st.markdown('<div class="section-header">👪 FILIAÇÃO E FINANCEIRO</div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1: st.text_input("Nome do Pai"); st.text_input("WhatsApp Pai")
    with f2: st.text_input("Nome da Mãe"); st.text_input("WhatsApp Mãe")
    
    res_nome = st.text_input("Nome do Responsável Financeiro*")
    r1, r2, r3 = st.columns(3)
    with r1: res_cpf = st.text_input("CPF Resp*")
    with r2: res_cel = st.text_input("Cel Resp*")
    with r3: res_par = st.selectbox("Parentesco*", ["--- Selecione ---", "Pai/Mãe", "Avô/ã", "Tio/a", "Outro"])

    st.markdown('<div class="section-header">📝 OBSERVAÇÕES E ARQUIVOS</div>', unsafe_allow_html=True)
    st.text_area("Observações Médicas/Gerais (Máx. 1000 caracteres)", height=80)
    st.file_uploader("Documentos/Foto Atleta", accept_multiple_files=True)
    
    aceite1 = st.checkbox("Declaro que o aluno goza de plena saúde física e mental para a prática de futebol.*")
    aceite2 = st.checkbox("Autorizo o uso de imagem e voz do aluno para divulgação da Escola VKL.*")

    if st.form_submit_button("CONCLUIR MATRÍCULA"):
        if "--- Selecione ---" in [unidade_vkl, sexo, pos, lat, hor, est, res_par] or not nome_aluno:
            st.error("❌ Preencha todos os campos obrigatórios e selecione as opções.")
        else:
            # ANIMAÇÃO DAS BOLAS
            for i in range(12):
                st.markdown(f'<div class="soccer-ball" style="left: {i*8}%; animation-delay: {i*0.15}s">⚽</div>', unsafe_allow_html=True)
            
            st.success(f"✅ {nome_aluno}, Bem-vindos à Família VKL! Matrícula realizada com sucesso na turma {turma}.")
            st.markdown(f'<a href="https://www.vklassociacao.com.br" target="_self" class="btn-home">RETORNAR À HOME VKL</a>', unsafe_allow_html=True)
