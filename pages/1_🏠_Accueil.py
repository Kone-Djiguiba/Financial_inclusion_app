import streamlit as st

# ⚠️ Doit être le tout premier appel Streamlit
st.set_page_config(
    page_title="Inclusion Financière",
    page_icon="🏦",
)

# --- Interface thème ---
st.sidebar.markdown("## 🎨 Thème de l'application")
theme_choice = st.sidebar.radio("Choisir un thème :", ["🌑 Sombre", "☀️ Clair"], index=0)

# --- Appliquer le style selon le thème ---
if theme_choice == "🌑 Sombre":
    st.markdown("""
        <style>
            body {
                background-color: #0e1117;
                color: #ffffff;
            }
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
            .css-18e3th9 {
                background-color: #0e1117;
            }
            .css-1d391kg {
                background-color: #0e1117;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f5;
                color: #000000;
            }
            .stApp {
                background-color: #f5f5f5;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Contenu principal de la page ---
st.title("🏦 Bienvenue dans l'application d'Inclusion Financière")
st.markdown("Cette application vous permet de prédire si une personne possède un compte bancaire, à partir de ses informations socio-économiques.")

st.markdown("---")

st.subheader("📊 Fonctionnalités disponibles :")
st.markdown("""
- 🧮 Formulaire de prédiction
- 📈 Visualisation des données
- ⚙️ Interface personnalisée
""")

st.success("Utilisez le menu à gauche pour naviguer entre les pages.")

