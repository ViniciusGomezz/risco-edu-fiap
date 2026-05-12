import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Passos Mágicos - Risco Educacional",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stButton>button {
    background-color: #1F5FA8;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #2E74C9;
    color: white;
}
</style>
""", unsafe_allow_html=True)


modelo = joblib.load("modelo_risco_educacional.pkl")
features_modelo = joblib.load("features_modelo.pkl")


st.title("🎓 Previsão de Risco Educacional")
st.subheader("Associação Passos Mágicos")

st.write(
    """
    Esta aplicação utiliza um modelo de Machine Learning para estimar a probabilidade
    de um aluno apresentar risco educacional, apoiando ações preventivas e acompanhamento individualizado.
    """
)

st.divider()


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


st.divider()


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


if st.button(
    "🔍 Calcular risco educacional",
    use_container_width=True
):
    probabilidade = modelo.predict_proba(entrada_encoded)[0][1]

    st.subheader("Resultado da previsão")

    col_a, col_b = st.columns(2)

    with col_a:
        st.metric(
            label="Probabilidade de risco",
            value=f"{probabilidade * 100:.1f}%"
        )

    with col_b:
        if probabilidade >= 0.70:
            st.error("🔴 Alto risco educacional")
        elif probabilidade >= 0.40:
            st.warning("🟠 Risco moderado")
        else:
            st.success("🟢 Baixo risco")

    st.divider()

    st.write("### Interpretação")

    if probabilidade >= 0.70:
        st.write(
            """
            O aluno apresenta alta probabilidade de risco educacional.
            Recomenda-se acompanhamento pedagógico e psicopedagógico prioritário,
            com atenção especial ao engajamento, evolução acadêmica e contexto individual.
            """
        )

    elif probabilidade >= 0.40:
        st.write(
            """
            O aluno apresenta risco intermediário.
            Recomenda-se monitoramento contínuo e ações preventivas para evitar queda de desempenho
            ou aumento da defasagem.
            """
        )

    else:
        st.write(
            """
            O aluno apresenta baixa probabilidade de risco educacional no momento.
            Recomenda-se manter acompanhamento regular e estímulo ao engajamento.
            """
        )


st.sidebar.title("Sobre o modelo")

st.sidebar.write(
    """
    Modelo utilizado: Random Forest Classifier.

    Métricas obtidas:
    - Accuracy: 85%
    - ROC-AUC: 0.92
    - Recall da classe de risco: 89%

    O modelo foi treinado com dados históricos da PEDE 2022, 2023 e 2024.
    """
)