import streamlit as st
from datetime import date
import re
import requests
import base64

# Configuração da Página
st.set_page_config(page_title="Cadastro Definitivo VKL", page_icon="⚽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO ---
def get_base64_img(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except: return None

url_fundo = "https://www.vklassociacao.com.br/images/site/vkl.png"
bin_str = get_base64_img(url_fundo)

# --- FUNÇÕES DE VALIDAÇÃO ---
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', str(cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]): return False
    return True

def validar_tel(tel):
    numeros = re.sub(r'\D', '', str(tel))
    return 10 <= len(numeros) <= 11

def calcular_categoria(nascimento):
    idade = date.today().year - nascimento.year
    if idade <= 7: return "Sub-7"
    elif idade <= 9: return "Sub-9"
    elif idade <= 11: return "Sub-11"
    elif idade <= 13: return "Sub-13"
    elif idade <= 15: return "Sub-15"
    else: return "Sub-17 / Adulto"

# --- ESTILIZAÇÃO CSS (PADRÃO VKL) ---
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), url("data:image/png;base64,{bin_str if bin_str else ''}"); background-attachment: fixed; }}
    .section-header {{ background-color: #003366; color: #ffffff; padding: 10px 15px; border-radius: 8px; font-weight: bold; margin-top: 25px; border-left: 6px solid #FFD700; }}
    .cat-box {{ background-color: #FFD700; color: #003366; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 22px; border: 2px solid #003366; margin: 15px 0; }}
    label {{ color: #003366 !important; font-weight: bold !important; }}
    .stTextArea textarea {{ height: 100px !important; }}
    div[data-testid="stFormSubmitButton"] > button {{ width: 100%; background: linear-gradient(135deg, #003366 0%, #004a99 100%); color: #FFD700; height: 60px; font-size: 20px; font-weight: bold; border-radius: 12px; border: 2px solid #FFD700; }}
    .btn-home {{ display: block; width: 100%; text-align: center; background-color: #f0f2f6; color: #003366; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; border: 1px solid #003366; }}
    </style>
    """, unsafe_allow_html=True)

# --- TOPO ---
st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=250)
st.markdown("<h1 style='text-align: center; color: #003366;'>Ficha de Inscrição Oficial VKL</h1>", unsafe_allow_html=True)

# --- CAMPOS REATIVOS (LOGIN, SENHA E CATEGORIA) ---
st.markdown('<div class="section-header">🔐 ACESSO E TURMA</div>', unsafe_allow_html=True)
col_l, col_s = st.columns(2)
with col_l: login_user = st.text_input("Login (Escolha um exclusivo para o atleta)*")
with col_s: senha_user = st.text_input("Senha*", type="password")

nasc_aluno = st.date_input("Data de Nascimento do Aluno*", value=date(2015, 1, 1), format="DD/MM/YYYY")
turma_sugerida = calcular_categoria(nasc_aluno)
st.markdown(f'<div class="cat-box">TURMA SUGERIDA: {turma_sugerida}</div>', unsafe_allow_html=True)

# --- INÍCIO DO FORMULÁRIO ---
with st.form("form_vkl_definitivo"):
    
    # DADOS DO ALUNO
    st.markdown('<div class="section-header">🏃 DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    col_a1, col_a2 = st.columns(2)
    with col_a1: cpf_aluno = st.text_input("CPF do Aluno (ou do Responsável)*")
    with col_a2: cel_aluno = st.text_input("Celular do Aluno (Opcional)")
    sexo_aluno = st.selectbox("Sexo Biológico*", ["Masculino", "Feminino"])

    # TÉCNICO E HORÁRIO
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1: posicao = st.selectbox("Posição*", ["Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante", "A definir"])
    with col_t2: lateralidade = st.selectbox("Lateralidade*", ["Destro", "Canhoto", "Ambidestro"])
    with col_t3: horario = st.selectbox("Melhor Horário*", ["Manhã", "Tarde", "Noite"])

    # ENDEREÇO
    st.markdown('<div class="section-header">🏠 ENDEREÇO RESIDENCIAL</div>', unsafe_allow_html=True)
    rua = st.text_input("Rua/Av*")
    col_e1, col_e2 = st.columns([1, 2])
    with col_e1: numero = st.text_input("Número*")
    with col_e2: complemento = st.text_input("Complemento")
    
    col_e3, col_e4 = st.columns(2)
    with col_e3: bairro = st.text_input("Bairro*")
    with col_e4: cep = st.text_input("CEP*")
    
    col_e5, col_e6 = st.columns(2)
    with col_e5: cidade = st.selectbox("Cidade*", ["Guaratuba", "Garuva", "Itapoá", "Outra"])
    with col_e6: estado = st.selectbox("Estado*", ["PR", "SC", "Outro"])

    # FILIAÇÃO (OPCIONAL)
    st.markdown('<div class="section-header">👪 FILIAÇÃO (OPCIONAL)</div>', unsafe_allow_html=True)
    c_p1, c_p2 = st.columns([2, 1])
    with c_p1: nome_pai = st.text_input("Nome do Pai")
    with c_p2: tel_pai = st.text_input("Celular do Pai")
    
    c_m1, c_m2 = st.columns([2, 1])
    with c_m1: nome_mae = st.text_input("Nome da Mãe")
    with c_m2: tel_mae = st.text_input("Celular da Mãe")

    # RESPONSÁVEL FINANCEIRO
    st.markdown('<div class="section-header">💰 RESPONSÁVEL FINANCEIRO (OBRIGATÓRIO)</div>', unsafe_allow_html=True)
    res_nome = st.text_input("Nome Completo do Responsável Financeiro*")
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1: res_cpf = st.text_input("CPF Responsável*")
    with col_r2: res_cel = st.text_input("Celular Responsável*")
    with col_r3: res_par = st.selectbox("Parentesco*", ["Pai/Mãe", "Avô/Avó", "Tio/Tia", "Outro"])

    # OBSERVAÇÕES E ARQUIVOS
    st.markdown('<div class="section-header">📝 OBSERVAÇÕES MÉDICAS / GERAIS</div>', unsafe_allow_html=True)
    obs = st.text_area("Máximo 1000 caracteres", placeholder="Alergias, problemas de saúde, etc.", max_chars=1000)
    
    st.markdown('<div class="section-header">📷 DOCUMENTAÇÃO (OPCIONAL)</div>', unsafe_allow_html=True)
    foto = st.file_uploader("Enviar Foto do Atleta e Documento (RG/CPF)", accept_multiple_files=True)

    # TERMOS
    st.markdown("---")
    termo_saude = st.checkbox("Declaro que o aluno está em boas condições de saúde para prática esportiva.*")
    termo_imagem = st.checkbox("Autorizo o uso de imagem do aluno para fins de divulgação da VKL.*")

    btn_enviar = st.form_submit_button("ENVIAR CADASTRO")

    if btn_enviar:
        if not (login_user and senha_user and nome_aluno and cpf_aluno and rua and numero and bairro and cep and res_nome and res_cpf and res_cel and termo_saude and termo_imagem):
            st.error("❌ Por favor, preencha todos os campos obrigatórios e aceite os termos.")
        elif not validar_cpf(res_cpf):
            st.error("❌ CPF do Responsável inválido.")
        elif not validar_tel(res_cel):
            st.error("❌ Celular do Responsável inválido.")
        else:
            # Lógica de Sucesso
            st.success(f"✅ Bem-vindos à Família VKL! Matrícula de **{nome_aluno}** realizada com sucesso para a turma **{turma_sugerida}**.")
            st.balloons()
            st.markdown(f"<a href='https://www.vklassociacao.com.br' class='btn-home'>🏠 Voltar para a Home VKL</a>", unsafe_allow_html=True)
