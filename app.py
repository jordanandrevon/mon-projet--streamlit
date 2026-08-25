import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


# ==========================================
# 1. INITIALISATION DE LA SESSION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""


# ==========================================
# 2. CHARGEMENT DES COMPTES
# ==========================================

@st.cache_data
def load_accounts():
    return pd.read_csv("accounts.csv")


# ==========================================
# 3. AUTHENTIFICATION
# ==========================================

def authenticate(username_input, password_input):

    accounts_df = load_accounts()

    user_match = accounts_df[
        (accounts_df["name"] == username_input) &
        (accounts_df["password"] == password_input)
    ]

    return not user_match.empty


# ==========================================
# 4. PAGE DE CONNEXION
# ==========================================

if not st.session_state["logged_in"]:

    st.title("🔐 Connexion à l'application")

    st.subheader("Veuillez vous identifier pour accéder au contenu")

    username_input = st.text_input("Nom d'utilisateur")

    password_input = st.text_input(
        "Mot de passe",
        type="password"
    )

    if st.button("Se connecter"):

        if authenticate(username_input, password_input):

            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input

            st.success(
                f"Bienvenue {username_input} !"
            )

            st.rerun()

        else:

            st.error(
                "Nom d'utilisateur ou mot de passe incorrect."
            )


# ==========================================
# 5. APPLICATION SÉCURISÉE
# ==========================================

else:

    # --------------------------------------
    # BARRE LATÉRALE
    # --------------------------------------

    with st.sidebar:

        st.write(
            f"👋 Bienvenue, **{st.session_state['username']}** !"
        )

        if st.button("Se déconnecter"):

            st.session_state["logged_in"] = False
            st.session_state["username"] = ""

            st.rerun()

        st.divider()

        # Menu de navigation
        selected_page = option_menu(
            menu_title="Menu principal",
            options=[
                "Accueil",
                "Galerie Photos"
            ],
            icons=[
                "house",
                "images"
            ],
            default_index=0
        )


    # ======================================
    # PAGE ACCUEIL
    # ======================================

    if selected_page == "Accueil":

        st.title("🏠 Page d'Accueil")

        st.write(
            f"Bienvenue **{st.session_state['username']}** !"
        )

        st.info(
            "Cette page est uniquement accessible "
            "aux utilisateurs authentifiés."
        )

        st.subheader("Application Streamlit sécurisée")

        st.write(
            "Vous êtes actuellement connecté à l'application."
        )


    # ======================================
    # PAGE GALERIE
    # ======================================

    elif selected_page == "Galerie Photos":

        st.title("🐱 Galerie Photos")

        st.write(
            "Voici une galerie de photos de chats."
        )

        # Création de 3 colonnes
        cols = st.columns(3)

        images = [
            "https://static.streamlit.io/examples/cat.jpg",
            "https://static.streamlit.io/examples/dog.jpg",
            "https://static.streamlit.io/examples/owl.jpg"
        ]

        # Affichage des images
        for index, image in enumerate(images):

            with cols[index % 3]:

                st.image(
                    image,
                    caption=f"Animal {index + 1}",
                    use_container_width=True
                )
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