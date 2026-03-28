import streamlit as st
import pandas as pd
import os

arquivo = "gastos.csv"

# ⚙️ Configuração
st.set_page_config(page_title="Controle de Gastos", layout="centered")

st.title("💰 Controle de Gastos")

# 🔄 Inicializar estado
if "valor" not in st.session_state:
    st.session_state.valor = 0.0
if "descricao" not in st.session_state:
    st.session_state.descricao = ""
if "forma" not in st.session_state:
    st.session_state.forma = "Pix"
if "categoria" not in st.session_state:
    st.session_state.categoria = "Alimentação"

# 📥 FORMULÁRIO
st.subheader("Adicionar movimentação")


valor = st.number_input("Valor", min_value=0.0, key="valor")

forma = st.selectbox(
    "Forma de pagamento",
    ["Pix", "Débito", "Crédito", "Dinheiro"],
    key="forma"
)

categoria = st.selectbox(
    "Categoria",
    ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"],
    key="categoria"
)

descricao = st.text_input("Descrição", key="descricao")

# 💾 SALVAR
if st.button("Salvar"):
    if valor == 0:
        st.warning("Digite um valor maior que zero!")
    else:
        novo = pd.DataFrame(
            [[tipo, valor, forma, categoria, descricao]],
            columns=["Tipo", "Valor", "Forma", "Categoria", "Descrição"]
        )

        if os.path.exists(arquivo):
            df = pd.read_csv(arquivo)
            df = pd.concat([df, novo], ignore_index=True)
        else:
            df = novo

        df.to_csv(arquivo, index=False)

        st.success("Salvo com sucesso!")

        # 🧹 LIMPAR CAMPOS
        st.session_state.valor = 0.0
        st.session_state.descricao = ""
        st.session_state.tipo = "Saída"
        st.session_state.forma = "Pix"
        st.session_state.categoria = "Alimentação"

# 📊 CARREGAR DADOS
if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)

    st.subheader("📋 Movimentações")
    st.dataframe(df)

    # 💰 SALDO
    saldo = 0
    for _, row in df.iterrows():
        if row["Tipo"] == "Entrada":
            saldo += row["Valor"]
        else:
            saldo -= row["Valor"]

    st.subheader("💰 Saldo Atual")
    st.metric("", f"R$ {saldo:.2f}")

    # 📊 GRÁFICO
    st.subheader("📊 Gastos por Categoria")

    gastos = df[df["Tipo"] == "Saída"]

    if not gastos.empty:
        grafico = gastos.groupby("Categoria")["Valor"].sum()
        st.bar_chart(grafico)

    # 📥 BOTÃO PRA BAIXAR (tipo backup)
    st.download_button(
        "📥 Baixar planilha",
        df.to_csv(index=False),
        "gastos.csv"
    )
