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