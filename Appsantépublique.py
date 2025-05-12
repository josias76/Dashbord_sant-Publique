import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# --- Configuration de la page ---
st.set_page_config(
    page_title="Tableau de bord - Santé publique",
    layout="wide",
    page_icon="💉"
)

# --- Fonction pour charger une animation Lottie ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Animation d'en-tête
lottie_animation = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_w51pcehl.json")

# --- Chargement des données ---
uploaded_file = st.file_uploader("\U0001F4C2 Importez un fichier CSV de données de santé publique", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    st.title("\U0001F489 Tableau de Bord des Campagnes de Santé Publique")

    with st.container():
        st_lottie(lottie_animation, height=200, key="header")

    # --- Filtres ---
    with st.sidebar:
        st.header("\U0001F50D Filtres")
        maladies = st.multiselect("Choisissez les maladies", options=df["Maladie"].unique(), default=df["Maladie"].unique())
        regions = st.multiselect("Choisissez les régions", options=df["Région"].unique(), default=df["Région"].unique())
        sexes = st.multiselect("Sexe", options=df["Sexe"].unique(), default=df["Sexe"].unique())
        ages = st.multiselect("Tranche d'âge", options=df["Tranche_d_âge"].unique(), default=df["Tranche_d_âge"].unique())

    # --- Application des filtres ---
    df_filtré = df[
        df["Maladie"].isin(maladies) &
        df["Région"].isin(regions) &
        df["Sexe"].isin(sexes) &
        df["Tranche_d_âge"].isin(ages)
    ]

    # --- Statistiques globales ---
    total_cas = int(df_filtré["Nombre_de_cas"].sum())
    nb_enregistrements = df_filtré.shape[0]

    col1, col2 = st.columns(2)
    col1.metric("\U0001F4CA Nombre total de cas", f"{total_cas:,}")
    col2.metric("\U0001F5C2\ufe0f Enregistrements", nb_enregistrements)

    # --- Graphiques ---
    col3, col4 = st.columns(2)

    with col3:
        cas_par_maladie = df_filtré.groupby("Maladie")["Nombre_de_cas"].sum().reset_index()
        fig1 = px.bar(cas_par_maladie, x="Maladie", y="Nombre_de_cas", color="Maladie",
                      title="\U0001F489 Cas par maladie", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col4:
        cas_par_region = df_filtré.groupby("Région")["Nombre_de_cas"].sum().reset_index()
        fig2 = px.pie(cas_par_region, names="Région", values="Nombre_de_cas", title="\U0001F30F Répartition régionale")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    cas_temps = df_filtré.groupby("Date")["Nombre_de_cas"].sum().reset_index()
    fig3 = px.line(cas_temps, x="Date", y="Nombre_de_cas", title="\U0001F4C5 Évolution des cas dans le temps")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("\u26A0\ufe0f Veuillez importer un fichier CSV pour visualiser les données.")
