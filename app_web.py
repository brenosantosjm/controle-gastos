import streamlit as st
import pandas as pd
import os

arquivo = "gastos.csv"

st.set_page_config(page_title="Controle de Gastos", layout="centered")

st.title("💰 Controle de Gastos")

# FORMULÁRIO
st.subheader("Adicionar movimentação")

tipo = st.selectbox("Tipo", ["Saída", "Entrada"])

valor = st.number_input("Valor", min_value=0.0)

forma = st.selectbox("Forma de pagamento", ["Pix", "Débito", "Crédito", "Dinheiro"])

categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"])

descricao = st.text_input("Descrição")

if st.button("Salvar"):
    novo = pd.DataFrame([[tipo, valor, forma, categoria, descricao]],
                        columns=["Tipo", "Valor", "Forma", "Categoria", "Descrição"])

    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
        df = pd.concat([df, novo], ignore_index=True)
    else:
        df = novo

    df.to_csv(arquivo, index=False)
    st.success("Movimentação salva!")

# MOSTRAR DADOS
if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)

    st.subheader("📋 Movimentações")

    saldo = 0
    for _, row in df.iterrows():
        if row["Tipo"] == "Entrada":
            saldo += row["Valor"]
        else:
            saldo -= row["Valor"]

    st.metric("💰 Saldo atual", f"R$ {saldo:.2f}")

    st.dataframe(df)

    # 📊 GRÁFICO
    st.subheader("📊 Gastos por Categoria")

    gastos = df[df["Tipo"] == "Saída"]

    if not gastos.empty:
        grafico = gastos.groupby("Categoria")["Valor"].sum()
        st.bar_chart(grafico)