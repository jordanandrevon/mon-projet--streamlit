import streamlit as st
import pandas as pd
# Titre principal de la page
st.title("Mon Premier Dashboard Streamlit")
# Texte de présentation
st.write("Bienvenue sur cette application interactive dédiée à l'analyse de données.")
import streamlit as st
import pandas as pd

# Chargement du fichier CSV
df = pd.read_csv("taxis.csv")

# Titre personnalisé
st.title("Dashboard Analyse Taxis - Jordan")

# Menu déroulant pour choisir un arrondissement
boroughs = df["pickup_borough"].dropna().unique()

borough = st.selectbox(
    "Choisissez un quartier de prise en charge :",
    boroughs
)

# Filtrer le dataframe selon l'arrondissement choisi
df_filtre = df[df["pickup_borough"] == borough]

# Afficher les 5 premières lignes
st.dataframe(df_filtre.head())

# Afficher le nombre total de courses
st.metric(
    "Nombre total de courses",
    len(df_filtre)
)