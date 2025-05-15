import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder

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
# Titre et instructions
st.markdown("<h2 style='text-align: center;'>📋 Formulaire de prédiction</h2>", unsafe_allow_html=True)
st.markdown("Remplissez le formulaire ci-dessous pour savoir si une personne a un compte bancaire 💳")
st.markdown("---")

# Personnalisation bouton
st.markdown("""
    <style>
    .stButton>button {
        background-color: #00C3FF;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0099cc;
    }
    </style>
""", unsafe_allow_html=True)

# Chargement du modèle et des données
model = joblib.load("C:/Users/USERNAME/Desktop/app/financial_inclusion_app/model/best_randomforest_model (1).joblib")
df = pd.read_csv("C:/Users/USERNAME/Desktop/app/financial_inclusion_app/data/Financial_inclusion_dataset.csv")
df = df.drop(columns=['year', 'uniqueid'])

# Colonnes à forte cardinalité
high_card_cols = ['country', 'relationship_with_head', 'marital_status', 'education_level', 'job_type']

# Récupération des valeurs uniques AVANT suppression
education_values = df['education_level'].unique()
marital_values = df['marital_status'].unique()
relationship_values = df['relationship_with_head'].unique()
job_values = df['job_type'].unique()
country_values = df['country'].unique()

# Prétraitement du dataset
freq_maps = {col: df[col].value_counts() for col in high_card_cols}
for col in high_card_cols:
    df[col + '_freq'] = df[col].map(freq_maps[col])
scaler = MinMaxScaler()
freq_cols = [col + '_freq' for col in high_card_cols]
df[freq_cols] = scaler.fit_transform(df[freq_cols])
df = df.drop(columns=high_card_cols)

le = LabelEncoder()
df['bank_account'] = le.fit_transform(df['bank_account'])

cat_cols = ['location_type', 'cellphone_access', 'gender_of_respondent']
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoder.fit(df[cat_cols])
encoded_array = encoder.transform(df[cat_cols])
encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(cat_cols), dtype=int)
df = df.drop(columns=cat_cols).reset_index(drop=True)
df_final = pd.concat([df.drop(columns=['bank_account']), encoded_df], axis=1)
full_columns = df_final.columns

# Formulaire
with st.form("formulaire"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("🎂 Âge", 16, 100, 30)
        household = st.slider("👨‍👩‍👧 Taille du foyer", 1, 20, 5)
        cellphone = st.radio("📱 Accès au téléphone portable", ["Yes", "No"])
        gender = st.radio("👤 Sexe", ["Male", "Female"])
        location = st.radio("📍 Type de lieu", ["Urban", "Rural"])
    with col2:
        country = st.selectbox("🌍 Pays", country_values)
        education = st.selectbox("🎓 Niveau d'éducation", education_values)
        marital = st.selectbox("💍 Statut marital", marital_values)
        relationship = st.selectbox("👪 Relation au chef de famille", relationship_values)
        job = st.selectbox("💼 Type d'emploi", job_values)

    submit = st.form_submit_button("🔍 Prédire")

# Prédiction après soumission
if submit:
    user_input = {
        "age_of_respondent": age,
        "household_size": household,
        "cellphone_access": cellphone,
        "country": country,
        "gender_of_respondent": gender,
        "location_type": location,
        "education_level": education,
        "marital_status": marital,
        "relationship_with_head": relationship,
        "job_type": job
    }

    df_user = pd.DataFrame([user_input])

    for col in high_card_cols:
        df_user[col + '_freq'] = df_user[col].map(freq_maps[col]).fillna(0)
    df_user[freq_cols] = scaler.transform(df_user[freq_cols])
    df_user = df_user.drop(columns=high_card_cols)

    encoded_user = encoder.transform(df_user[cat_cols])
    encoded_user_df = pd.DataFrame(encoded_user, columns=encoder.get_feature_names_out(cat_cols), dtype=int)
    df_user = df_user.drop(columns=cat_cols).reset_index(drop=True)
    encoded_user_df = encoded_user_df.reset_index(drop=True)
    df_user_final = pd.concat([df_user, encoded_user_df], axis=1)

    for col in full_columns:
        if col not in df_user_final.columns:
            df_user_final[col] = 0
    df_user_final = df_user_final[full_columns]

    prediction = model.predict(df_user_final)

    st.markdown("---")
    if prediction[0] == 1:
        st.success("✅ Cette personne possède un compte bancaire.")
        st.info("💡 **Conseil** : Continuez à utiliser votre compte régulièrement. Cela facilite les services financiers comme les prêts, l’épargne ou les assurances.")
    else:
        st.error("❌ Cette personne **ne possède pas** de compte bancaire.")
        st.warning("🔔 **Sensibilisation** : Avoir un compte bancaire vous permet de sécuriser votre argent, de recevoir des paiements, et d'accéder à plus de services financiers.")

