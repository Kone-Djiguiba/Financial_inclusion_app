import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
st.set_page_config(page_title="Visualisation des Données", page_icon="📊")

st.markdown("<h2 style='text-align: center;'>📊 Visualisation des Données</h2>", unsafe_allow_html=True)
st.markdown("Explorez les données d’inclusion financière : âge, genre, accès téléphonique, etc.")
st.markdown("---")

df = pd.read_csv("C:/Users/USERNAME/Desktop/app/financial_inclusion_app/data/Financial_inclusion_dataset.csv")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Répartition du genre")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x="gender_of_respondent", palette="Set2", ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Accès au téléphone 📱")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x="cellphone_access", palette="Set3", ax=ax2)
    st.pyplot(fig2)

st.subheader("📈 Âge selon possession de compte")
fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x="bank_account", y="age_of_respondent", palette="coolwarm", ax=ax3)
ax3.set_xticklabels(["Pas de compte", "Compte"])
st.pyplot(fig3)
