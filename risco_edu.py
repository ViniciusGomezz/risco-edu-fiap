import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib


st.set_page_config(
    page_title="Passos Mágicos - Risco Educacional",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>

/* ÁREA GERAL */
.stApp {
    background-color: #F4F6F9;
    color: #1E1E1E;
}

/* CONTAINER PRINCIPAL MAIS LARGO */
.block-container {
    max-width: 95% !important;
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* TEXTOS */
h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #1E1E1E !important;
}

h1, h2, h3 {
    color: #0F4C8A !important;
}

/* SUBTÍTULO */
[data-testid="stMarkdownContainer"] p {
    color: #1E1E1E !important;
    font-size: 16px;
}

/* CARDS */
.card, .metric-card {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
    margin-bottom: 18px;
}

/* KPI */
.metric-title {
    color: #5F6B7A !important;
    font-size: 15px;
}

.metric-value {
    color: #0F4C8A !important;
    font-size: 30px;
    font-weight: 700;
}

/* SELECTBOX */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1E1E1E !important;
    border: 1px solid #D0D7DE !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: #1E1E1E !important;
}

/* MENU ABERTO DO SELECTBOX */
div[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
}

div[data-baseweb="popover"] * {
    background-color: #FFFFFF !important;
    color: #1E1E1E !important;
}

div[role="listbox"] {
    background-color: #FFFFFF !important;
}

div[role="option"] {
    background-color: #FFFFFF !important;
    color: #1E1E1E !important;
}

div[role="option"]:hover {
    background-color: #EAF2FB !important;
    color: #1E1E1E !important;
}

li[role="option"] {
    background-color: #FFFFFF !important;
    color: #1E1E1E !important;
}

li[role="option"]:hover {
    background-color: #EAF2FB !important;
    color: #1E1E1E !important;
}

/* SETA DO SELECTBOX */
.stSelectbox svg {
    fill: #1E1E1E !important;
    color: #1E1E1E !important;
}

/* SLIDERS */
.stSlider label, .stSlider span, .stSlider div {
    color: #1E1E1E !important;
}

/* BOTÃO */
.stButton>button {
    background-color: #1F5FA8 !important;
    color: white !important;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #2E74C9 !important;
    color: white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] * {
    color: #1E1E1E !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


@st.cache_resource
def carregar_modelo():
    modelo = joblib.load("modelo_risco_educacional.pkl")
    features_modelo = joblib.load("features_modelo.pkl")
    return modelo, features_modelo


modelo, features_modelo = carregar_modelo()


def criar_gauge(probabilidade):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probabilidade * 100,
            number={
                "suffix": "%",
                "font": {"size": 52, "color": "#0F4C8A"}
            },
            title={
                "text": "Probabilidade de risco",
                "font": {"size": 20, "color": "#1E1E1E"}
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#1E1E1E",
                    "tickfont": {"color": "#1E1E1E"}
                },
                "bar": {"color": "#1F5FA8"},
                "bgcolor": "#FFFFFF",
                "borderwidth": 1,
                "bordercolor": "#D0D7DE",
                "steps": [
                    {"range": [0, 40], "color": "#DFF3E3"},
                    {"range": [40, 70], "color": "#FFE8B5"},
                    {"range": [70, 100], "color": "#F7C7C7"}
                ],
                "threshold": {
                    "line": {"color": "#C0392B", "width": 4},
                    "thickness": 0.75,
                    "value": 70
                }
            }
        )
    )

    fig.update_layout(
        height=330,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"color": "#1E1E1E"},
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


def criar_radar(iaa, ips, ipp):
    categorias = [
        "Autoavaliação",
        "Psicossocial",
        "Psicopedagógico"
    ]

    valores = [iaa, ips, ipp]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=valores + [valores[0]],
            theta=categorias + [categorias[0]],
            fill="toself",
            name="Indicadores",
            line={"color": "#1F5FA8", "width": 3},
            fillcolor="rgba(31, 95, 168, 0.25)"
        )
    )

    fig.update_layout(
        height=330,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"color": "#1E1E1E"},
        polar=dict(
            bgcolor="#FFFFFF",
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont={"color": "#1E1E1E"},
                gridcolor="#D0D7DE",
                linecolor="#D0D7DE"
            ),
            angularaxis=dict(
                tickfont={"color": "#1E1E1E"},
                gridcolor="#D0D7DE",
                linecolor="#D0D7DE"
            )
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig


st.title("🎓 Previsão de Risco Educacional")

st.write(
    """
    Aplicação preditiva para estimar a probabilidade de risco educacional
    com base em indicadores educacionais, psicossociais e psicopedagógicos.
    """
)

st.divider()

st.subheader("📋 Dados do aluno")

col1, col2, col3 = st.columns(3)

with col1:
    idade = st.selectbox(
        "Idade",
        options=list(range(6, 25)),
        index=6
    )

    ano_ingresso = st.selectbox(
        "Ano de ingresso",
        options=[2024, 2023, 2022, 2021, 2020, 2019, 2018],
        index=2
    )

    genero = st.selectbox(
        "Gênero",
        ["FEMININO", "MASCULINO"]
    )

with col2:
    pedra = st.selectbox(
        "Pedra",
        ["QUARTZO", "ÁGATA", "AMETISTA", "TOPÁZIO", "DESCONHECIDO"]
    )

    macro_fase = st.selectbox(
        "Fase",
        [
            "FASE ALFA",
            "FASE 1",
            "FASE 2",
            "FASE 3",
            "FASE 4",
            "FASE 5",
            "FASE 6",
            "FASE 7",
            "FASE 8"
        ]
    )

with col3:
    iaa = st.slider(
        "IAA - Autoavaliação",
        0.0,
        10.0,
        8.0,
        0.1
    )

    ips = st.slider(
        "IPS - Psicossocial",
        0.0,
        10.0,
        7.0,
        0.1
    )

    ipp = st.slider(
        "IPP - Psicopedagógico",
        0.0,
        10.0,
        7.5,
        0.1
    )

entrada = pd.DataFrame({
    "IAA": [iaa],
    "IPS": [ips],
    "IPP": [ipp],
    "IDADE": [idade],
    "ANO_INGRESSO": [ano_ingresso],
    "PEDRA": [pedra],
    "MACRO_FASE": [macro_fase],
    "GENERO": [genero]
})

entrada_encoded = pd.get_dummies(
    entrada,
    columns=["PEDRA", "MACRO_FASE", "GENERO"],
    drop_first=True
)

for col in features_modelo:
    if col not in entrada_encoded.columns:
        entrada_encoded[col] = 0

entrada_encoded = entrada_encoded[features_modelo]

st.write("")

if st.button(
    "🔍 Calcular risco educacional",
    use_container_width=True
):
    probabilidade = modelo.predict_proba(entrada_encoded)[0][1]

    if probabilidade >= 0.70:
        nivel = "Alto risco"
        cor_nivel = "🔴"
        recomendacao = """
        O aluno apresenta alta probabilidade de risco educacional.
        Recomenda-se acompanhamento pedagógico e psicopedagógico prioritário,
        com atenção especial ao engajamento, evolução acadêmica e contexto individual.
        """
    elif probabilidade >= 0.40:
        nivel = "Risco moderado"
        cor_nivel = "🟠"
        recomendacao = """
        O aluno apresenta risco intermediário.
        Recomenda-se monitoramento contínuo e ações preventivas para evitar queda de desempenho
        ou aumento da defasagem.
        """
    else:
        nivel = "Baixo risco"
        cor_nivel = "🟢"
        recomendacao = """
        O aluno apresenta baixa probabilidade de risco educacional no momento.
        Recomenda-se manter acompanhamento regular e estímulo ao engajamento.
        """

    st.divider()

    st.subheader("📊 Resultado da previsão")

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Probabilidade de risco</div>
                <div class="metric-value">{probabilidade * 100:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Classificação</div>
                <div class="metric-value">{cor_nivel} {nivel}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Modelo</div>
                <div class="metric-value">Random Forest</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.progress(float(probabilidade))

    col_gauge, col_radar = st.columns(2)

    with col_gauge:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(
            criar_gauge(probabilidade),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_radar:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(
            criar_radar(iaa, ips, ipp),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Interpretação")
    st.info(recomendacao)

    st.markdown("### 📌 Dados utilizados na previsão")
    st.dataframe(entrada, use_container_width=True)


st.sidebar.title("📘 Sobre o modelo")

st.sidebar.write(
    """
    **Modelo:** Random Forest Classifier

    **Métricas obtidas:**
    - Accuracy: 85%
    - ROC-AUC: 0.92
    - Recall da classe de risco: 89%

    **Base histórica:** PEDE 2022, 2023 e 2024.
    """
)

st.sidebar.divider()

st.sidebar.write(
    """
    **Interpretação do risco:**

    🟢 Baixo risco: até 40%

    🟠 Risco moderado: 40% a 70%

    🔴 Alto risco: acima de 70%
    """
)