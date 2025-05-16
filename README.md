
# 🌍 Financial Inclusion Prediction App

Cette application permet de prédire si une personne est financièrement incluse ou non, à partir de caractéristiques sociodémographiques issues du dataset Zindi **Financial Inclusion in Africa**.

## 📊 Fonctionnalités

- Interface web intuitive (via Streamlit)
- Prédiction en ligne du statut financier (inclus / non inclus)
- Visualisation interactive des données
- Design sombre personnalisé avec icônes

## 🚀 Lancer l'application

### Localement

```bash
git clone https://github.com/Kone-Djiguiba/Financial_inclusion_app.git
cd Financial_inclusion_app
pip install -r requirements.txt
streamlit run app.py
```

### En ligne

> 🔗 Lien vers l’app : [🌐 Streamlit App](https://<ton-lien-app>.streamlit.app)

## 📁 Structure du projet

```
📦 Financial_inclusion_app
├── app.py                  # Page principale
├── model/                  # Modèle ML .joblib
├── data/                   # Données CSV
├── pages/                  # Pages multipages Streamlit
│   ├── Accueil
│   ├── À propos
│   ├── Prédiction
│   └── Visualisations
└── requirements.txt        # Dépendances
```

## 🤖 Modèle ML

- Modèle : `RandomForestClassifier`
- Entraînement réalisé avec preprocessing (encodage, normalisation…)
- Sauvegarde avec `joblib`

## 📚 Données

- Dataset : [Zindi - Financial Inclusion in Africa](https://zindi.africa/competitions/financial-inclusion-in-africa/data)
- Variables : âge, niveau d’éducation, situation géographique, etc.

---

## 🙋‍♂️ Auteur

Développé par [Kone Djiguiba](https://github.com/Kone-Djiguiba)

> N'hésitez pas à ⭐️ le repo si vous aimez ce projet !
