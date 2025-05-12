import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json

# ---------- Chargement des animations ----------
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_accueil = load_lottiefile("animations/healthcare_animation.json")  # À placer dans un dossier animations

# ---------- Page d'accueil attrayante ----------
st.set_page_config(page_title="Dashboard Santé Publique", page_icon="🩺", layout="wide")

st.markdown("""
    <style>
    .main-header {
        font-size:3em;
        font-weight:bold;
        color:#4CAF50;
        text-align:center;
        margin-bottom:0;
    }
    .sub-header {
        font-size:1.2em;
        color:#555;
        text-align:center;
        margin-top:0;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        padding: 30px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>Tableau de bord des Campagnes de Santé Publique</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Analyse visuelle et interactive des données sanitaires en RDC</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st_lottie(lottie_accueil, height=250, key="accueil")

st.markdown("""
### \U0001F4E5 Importer vos fichiers CSV de données de santé
Pour commencer, chargez un ou plusieurs fichiers CSV contenant les informations suivantes :
- `Date`, `Région`, `Maladie`, `Sexe`, `Tranche_d_âge`, `Nombre_de_cas`
""")

with st.container():
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Sélectionnez vos fichiers CSV", type=["csv"], accept_multiple_files=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Vous pouvez maintenant continuer à utiliser uploaded_files pour l'analyse comme avant...

# Exemple de traitement plus bas dans ton app :
if uploaded_files:
    dfs = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(dfs, ignore_index=True)

    # Code de nettoyage ou visualisation...
else:
    st.info("Veuillez importer au moins un fichier CSV pour afficher le tableau de bord.")
