import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder

# --- Configuration de la page ---
st.set_page_config(page_title="Formulaire de prédiction", page_icon="📋", layout="centered")

# --- Design sombre personnalisé ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h2, h3, label { color: #00C3FF; }
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

# --- Chargement du modèle et des données ---
model = joblib.load("model/best_randomforest_model.joblib")
df = pd.read_csv("data/Financial_inclusion_dataset.csv")
df = df.drop(columns=['year', 'uniqueid'])

# --- Préparation du preprocessing ---
high_card_cols = ['country', 'relationship_with_head', 'marital_status', 'education_level', 'job_type']
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

# --- Titre et instructions ---
st.markdown("<h2>📋 Formulaire de prédiction</h2>", unsafe_allow_html=True)
st.markdown("Remplissez les informations ci-dessous pour savoir si une personne est susceptible d’avoir un compte bancaire 💳.")

# --- Formulaire utilisateur ---
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        age_of_respondent = st.slider("🎂 Âge de la personne", 16, 100, 30, help="Âge de la personne interrogée.")
        household_size = st.slider("👨‍👩‍👧 Taille du foyer", 1, 20, 5, help="Nombre de personnes dans le foyer.")
        cellphone_access = st.radio("📱 Accès à un téléphone portable", ["Yes", "No"], help="Possède-t-elle un téléphone portable ?")
        gender_of_respondent = st.radio("👤 Sexe", ["Male", "Female"], help="Genre de la personne.")
        location_type = st.radio("📍 Lieu de résidence", ["Urban", "Rural"], help="Habite-t-elle en ville ou en zone rurale ?")

    with col2:
        country = st.selectbox("🌍 Pays", ["Kenya", "Rwanda", "Tanzania", "Uganda"])
        education_level = st.selectbox("🎓 Niveau d'éducation", [
            "No formal education", "Primary education", "Secondary education",
            "Tertiary education", "Vocational training", "Other"
        ])
        marital_status = st.selectbox("💍 Statut marital", [
            "Married/Living together", "Divorced/Seperated", "Widowed",
            "Single/Never Married", "Dont know"
        ])
        relationship_with_head = st.selectbox("👪 Lien avec le chef de ménage", [
            "Head of Household", "Spouse", "Child", "Parent", "Other relative", "Other non-relatives", "Dont know"
        ])
        job_type = st.selectbox("💼 Type d'emploi", [
            "Self employed", "Government Dependent", "Formally employed Private",
            "Informally employed", "Formally employed Government", "Farming and Fishing", 
            "Remittance Dependent", "Other Income", "No Income"
        ])

    submit = st.form_submit_button("🔍 Prédire")

# --- Prédiction si soumission ---
if submit:
    user_input = {
        "age_of_respondent": age_of_respondent,
        "household_size": household_size,
        "cellphone_access": cellphone_access,
        "country": country,
        "gender_of_respondent": gender_of_respondent,
        "location_type": location_type,
        "education_level": education_level,
        "marital_status": marital_status,
        "relationship_with_head": relationship_with_head,
        "job_type": job_type
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

    # --- Message personnalisé selon le résultat ---
    if prediction[0] == 1:
        st.success("✅ Cette personne possède probablement un compte bancaire.")
        st.markdown("💡 **Astuce** : Avoir un compte bancaire facilite l'accès à des services essentiels comme les prêts, les économies et les paiements numériques. Continuez à l'utiliser régulièrement pour de meilleures opportunités financières !")
    else:
        st.error("❌ Cette personne ne possède probablement pas de compte bancaire.")
        st.markdown("📢 **Sensibilisation** : Encouragez cette personne à ouvrir un compte bancaire pour sécuriser son argent, recevoir des aides, ou encore développer une activité. L'inclusion financière est une étape clé vers l'autonomie économique.")

