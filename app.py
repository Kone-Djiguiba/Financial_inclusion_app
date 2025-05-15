import streamlit as st

# ⚠️ Ce bloc DOIT être en tout premier
st.set_page_config(
    page_title="Inclusion Financière",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Design sombre ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    h1, h2, h3 {
        color: #00C3FF;
        text-align: center;
    }
    .block-container {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Titre principal ---
st.markdown("<h1>📊 Prédiction d'Inclusion Financière</h1>", unsafe_allow_html=True)

# --- Message de bienvenue ---
st.markdown("""
Bienvenue dans cette application dédiée à **l'inclusion financière en Afrique**.  
Grâce à un modèle d'intelligence artificielle, vous pouvez ici :
- 📋 **Remplir un formulaire** avec les caractéristiques d'une personne,
- 🧠 **Prédire si cette personne possède un compte bancaire ou non**,
- 📈 **Explorer les données** utilisées pour construire le modèle.

""")

# --- Comment utiliser l'app ---
st.markdown("---")
st.subheader("🧭 Comment utiliser cette application ?")

st.markdown("""
1. **Allez dans le menu à gauche.**
2. Cliquez sur la page **📋 Formulaire de prédiction**.
3. Remplissez les informations demandées (âge, pays, emploi...).
4. Cliquez sur le bouton **Prédire**.
5. L'application vous dira si, selon le modèle, la personne a un compte bancaire ou non.

Vous pouvez aussi visiter la page **📊 Visualisation des données** pour mieux comprendre le contexte.
""")

# --- Info supplémentaire ---
st.info("Cette application a été conçue pour sensibiliser à l'importance de l'inclusion financière en Afrique.")

