import streamlit as st
from datetime import date
import re
import requests
import base64

# Configuração da Página
st.set_page_config(page_title="Matrícula VKL", page_icon="⚽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO ---
def get_base64_img(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except:
        return None

url_fundo = "https://www.vklassociacao.com.br/images/site/vkl.png"
bin_str = get_base64_img(url_fundo)

# --- FUNÇÕES DE APOIO ---
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]): return False
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

# --- ESTILIZAÇÃO CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), url("data:image/png;base64,{bin_str if bin_str else ''}"); background-attachment: fixed; }}
    .section-header {{ background-color: #003366; color: #ffffff; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 20px; border-left: 6px solid #FFD700; }}
    .cat-box {{ background-color: #FFD700; color: #003366; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 22px; border: 2px solid #003366; margin: 10px 0; }}
    div[data-testid="stFormSubmitButton"] > button {{ width: 100%; background: linear-gradient(135deg, #003366 0%, #004a99 100%); color: #FFD700; height: 55px; font-size: 22px; font-weight: bold; border-radius: 12px; }}
    label {{ color: #003366 !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.image("https://www.vklassociacao.com.br/images/EscolaDeFutebol/Escola_de_Futebol.jpeg", width=300)
st.markdown("<h1 style='text-align: center; color: #003366;'>⚽ Matrícula VKL</h1>", unsafe_allow_html=True)

# --- CAMPOS FORA DO FORMULÁRIO (PARA CÁLCULO EM TEMPO REAL) ---
st.markdown('<div class="section-header">🔑 1. ACESSO E NASCIMENTO</div>', unsafe_allow_html=True)

col_l, col_s = st.columns(2)
with col_l:
    login_usuario = st.text_input("Nome de Usuário (Login)*", placeholder="ex: pedro.silva")
with col_s:
    senha_usuario = st.text_input("Criar Senha*", type="password")

nasc_aluno = st.date_input("Data de Nascimento do Aluno*", value=date(2015, 1, 1), format="DD/MM/YYYY")
categoria_atual = calcular_categoria(nasc_aluno)
st.markdown(f'<div class="cat-box">CATEGORIA: {categoria_atual}</div>', unsafe_allow_html=True)

# --- INÍCIO DO FORMULÁRIO (DEMAIS DADOS) ---
with st.form("form_vkl_final"):
    st.markdown('<div class="section-header">🏃 2. DADOS DO ATLETA</div>', unsafe_allow_html=True)
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    
    col_at1, col_at2 = st.columns(2)
    with col_at1: genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    with col_at2: posicao = st.selectbox("Posição", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])

    st.markdown('<div class="section-header">📍 3. UNIDADE E ORIGEM</div>', unsafe_allow_html=True)
    unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    origem = st.selectbox("Como conheceu a nossa escola?", ["Indicação", "Facebook", "Instagram", "Pesquisa na Web", "Outros"])

    st.markdown('<div class="section-header">💰 4. RESPONSÁVEL FINANCEIRO</div>', unsafe_allow_html=True)
    res_nome = st.text_input("Nome Completo do Responsável*")
    col_f1, col_f2 = st.columns(2)
    with col_f1: res_cpf = st.text_input("CPF do Responsável*")
    with col_f2: res_tel = st.text_input("WhatsApp do Responsável*")

    enviar = st.form_submit_button("CONCLUIR MATRÍCULA")

    if enviar:
        if not login_usuario or not nome_aluno or not res_cpf:
            st.error("❌ Preencha os campos obrigatórios.")
        elif not validar_cpf(res_cpf):
            st.error("❌ CPF inválido.")
        else:
            # Envio para o Google (Ajustar entries conforme seu novo link depois)
            url_forms = "https://docs.google.com/forms/d/e/1FAIpQLSdyEy4VB4jQTzYdovJkXJUa_b4Y8rjlvbn5a1GthNmOzKYLRg/formResponse"
            dados = {
                "entry.666952651": nome_aluno,
                "entry.1010511222": unidade,
                "entry.1377162592": categoria_atual,
                "entry.162643904": genero,
                "entry.632921519": origem,
                # Aqui você adicionará o entry do Login e Senha depois
            }
            try:
                requests.post(url_forms, data=dados)
                st.success("✅ Matrícula enviada!")
                st.balloons()
            except:
                st.error("Erro ao salvar dados.")
