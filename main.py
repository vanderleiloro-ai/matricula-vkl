import streamlit as st
from datetime import date

# Configuração da Página e Cores VKL
st.set_page_config(page_title="Inscrição Escola VKL", page_icon="⚽", layout="centered")

# CSS para usar o padrão de cores da página (Azul e Dourado)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background-color: #003366; 
        color: white; 
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton>button:hover { background-color: #004a99; border: 1px solid #ffcc00; }
    h1, h2, h3 { color: #003366; }
    .stCheckbox { color: #333; }
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

# LOGO (Puxando do seu site oficial)
st.image("https://www.vklassociacao.com.br/images/logo.png", width=180)
st.title("Formulário Oficial de Matrícula")
st.write("Preencha os dados com atenção para efetivar a pré-inscrição do atleta.")

with st.form("form_vkl_completo"):
    
    # 1. LOCALIZAÇÃO E ORIGEM
    st.subheader("📍 Unidade e Origem")
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        unidade = st.selectbox("Selecione a Unidade (Polo)*", ["Guaratuba", "Garuva", "Itapoá"])
    with col_u2:
        origem = st.selectbox("Como conheceu a nossa escola?", 
                             ["Indicação", "Facebook", "Instagram", "Pesquisa na Web", "Outros"])

    st.divider()

    # 2. DADOS DO ALUNO
    st.subheader("🏃 Dados do Atleta")
    nome_aluno = st.text_input("Nome Completo do Aluno*")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        # O Streamlit já exibe a data no formato do sistema (DD/MM/AAAA se o navegador estiver em PT-BR)
        nasc_aluno = st.date_input("Data de Nascimento*", format="DD/MM/YYYY", min_value=date(2005, 1, 1))
    with c2:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    with c3:
        posicao = st.selectbox("Posição", ["A definir", "Goleiro", "Fixo/Zagueiro", "Ala", "Pivô/Atacante"])
    
    st.info(f"Categoria Automática: **{calcular_categoria(nasc_aluno)}**")

    st.divider()

    # 3. FILIAÇÃO (PAIS)
    st.subheader("👨‍👩‍👦 Dados da Filiação")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nome_pai = st.text_input("Nome do Pai")
        tel_pai = st.text_input("Telefone/WhatsApp do Pai")
    with col_p2:
        nome_mae = st.text_input("Nome da Mãe")
        tel_mae = st.text_input("Telefone/WhatsApp da Mãe")

    st.divider()

    # 4. RESPONSÁVEL FINANCEIRO
    st.subheader("💰 Responsável Financeiro")
    res_fin_nome = st.text_input("Nome Completo do Responsável Financeiro*")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        res_fin_cpf = st.text_input("CPF do Responsável*")
    with col_f2:
        res_fin_tel = st.text_input("Telefone do Responsável*")
    with col_f3:
        parentesco = st.selectbox("Grau de Parentesco*", ["Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Outro"])

    st.divider()

    # 5. SAÚDE E OBRIGATORIEDADES
    st.subheader("📋 Saúde e Autorizações")
    saude_obs = st.text_area("O aluno possui alguma alergia ou restrição médica? (Opcional)")
    
    st.warning("Para prosseguir, é necessário aceitar os termos abaixo:")
    aceite_imagem = st.checkbox("Autorizo obrigatoriamente o uso de imagem do aluno para fins de divulgação da VKL.*")
    aceite_saude = st.checkbox("Declaro obrigatoriamente que o aluno está apto para a prática de esportes.*")

    # BOTÃO FINAL
    enviar = st.form_submit_button("ENVIAR CADASTRO PARA ANÁLISE")

    if enviar:
        # Validação de obrigatoriedade
        if not nome_aluno or not res_fin_nome or not res_fin_cpf or not res_fin_tel:
            st.error("❌ Por favor, preencha todos os campos obrigatórios marcados com (*).")
        elif not aceite_imagem or not aceite_saude:
            st.error("❌ Você precisa aceitar o Uso de Imagem e a Declaração de Saúde para continuar.")
        else:
            st.success(f"✅ Inscrição de {nome_aluno} enviada com sucesso! Analisaremos os dados e entraremos em contato.")
            st.balloons()
