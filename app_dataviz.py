import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Chargement du dataset
df = pd.read_csv("flights.csv")

# Titre
st.title("Analyse du trafic aérien")

# Sélection de la période
annees = st.slider(
    "Sélectionnez une période :",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(int(df["year"].min()), int(df["year"].max()))
)

# Sélection du mois
mois = ["Tous les mois"] + list(df["month"].unique())

mois_selectionne = st.selectbox(
    "Sélectionnez un mois :",
    mois
)

# Filtre sur les années
df_filtre = df[
    (df["year"] >= annees[0]) &
    (df["year"] <= annees[1])
]

# Filtre sur le mois
if mois_selectionne != "Tous les mois":
    df_filtre = df_filtre[
        df_filtre["month"] == mois_selectionne
    ]

# Nombre total de passagers
total_passagers = df_filtre["passengers"].sum()

st.metric(
    "Nombre total de passagers",
    total_passagers
)

# Graphique d'évolution
st.subheader("Évolution du nombre de passagers")

df_graphique = df_filtre.copy()

df_graphique["date"] = pd.to_datetime(
    df_graphique["year"].astype(str) + "-" +
    df_graphique["month"] + "-01"
)

df_graphique = df_graphique.sort_values("date")

st.line_chart(
    df_graphique.set_index("date")["passengers"]
)

# Case à cocher pour afficher la Heatmap
afficher_heatmap = st.checkbox(
    "Afficher la Heatmap"
)

if afficher_heatmap:

    st.subheader("Répartition des passagers par année et par mois")

    pivot = df_filtre.pivot(
        index="month",
        columns="year",
        values="passengers"
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.heatmap(
        pivot,
        annot=True,
        fmt="g",
        cmap="YlGnBu",
        ax=ax
    )

    ax.set_xlabel("Année")
    ax.set_ylabel("Mois")

    st.pyplot(fig)