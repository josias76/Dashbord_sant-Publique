import streamlit as st
import pandas as pd
import plotly.express as px

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

# ---------- Affichage de l'image PNG ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("animations/healthcare_animation.png", use_container_width=True)  # Remplace par le bon chemin d'image

# ---------- Section d'import de fichiers ----------
st.markdown("""
### \U0001F4E5 Importer vos fichiers CSV de données de santé
Pour commencer, chargez un ou plusieurs fichiers CSV contenant les informations suivantes :
- `Date`, `Région`, `Maladie`, `Sexe`, `Tranche_d_âge`, `Nombre_de_cas`
""")

with st.container():
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Sélectionnez vos fichiers CSV", type=["csv"], accept_multiple_files=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Traitement des fichiers ----------
if uploaded_files:
    dfs = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(dfs, ignore_index=True)
    st.subheader("🎛️ Filtres interactifs")

    # --- Création des filtres dynamiques ---


    # Convertir la colonne Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Création des filtres
    with st.expander("🔍 Affiner les données"):
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_regions = st.multiselect("Région", options=sorted(df["Région"].unique()), default=sorted(df["Région"].unique()))
        with col2:
            selected_maladies = st.multiselect("Maladie", options=sorted(df["Maladie"].unique()), default=sorted(df["Maladie"].unique()))
        with col3:
            selected_sexes = st.multiselect("Sexe", options=sorted(df["Sexe"].unique()), default=sorted(df["Sexe"].unique()))

        col4, col5 = st.columns(2)
        with col4:
            selected_ages = st.multiselect("Tranche d'âge", options=sorted(df["Tranche_d_âge"].unique()), default=sorted(df["Tranche_d_âge"].unique()))
        with col5:
            min_date = df["Date"].min()
            max_date = df["Date"].max()
            date_range = st.date_input("Période", value=[min_date, max_date], min_value=min_date, max_value=max_date)

    # Application des filtres
    df_filtered = df[
        (df["Région"].isin(selected_regions)) &
        (df["Maladie"].isin(selected_maladies)) &
        (df["Sexe"].isin(selected_sexes)) &
        (df["Tranche_d_âge"].isin(selected_ages)) &
        (df["Date"] >= pd.to_datetime(date_range[0])) &
        (df["Date"] <= pd.to_datetime(date_range[1]))
    ]

    st.success(f"{len(df_filtered)} lignes sélectionnées après filtrage.")
    st.dataframe(df_filtered.head(20))

    # 🎨 Visualisations améliorées

    st.subheader("📊 Nombre total de cas par maladie")
    fig1 = px.bar(
        df_filtered.groupby("Maladie")["Nombre_de_cas"].sum().reset_index(),
        x="Maladie", y="Nombre_de_cas", color="Maladie",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="🦠 Nombre total de cas par maladie"
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(size=14, color="black"),
        title_font=dict(size=20, color="#2E8B57"),
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📍 Répartition des cas par région")
    fig2 = px.pie(
        df_filtered, values="Nombre_de_cas", names="Région",
        title="📍 Répartition des cas par région",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(title_font=dict(size=20, color="#6A1B9A"))
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("👥 Répartition des cas par sexe")
    fig3 = px.histogram(
        df_filtered, x="Sexe", y="Nombre_de_cas",
        color="Sexe", barmode="group", histfunc="sum",
        text_auto=True,
        color_discrete_map={"Masculin": "#2196F3", "Féminin": "#E91E63"},
        title="👤 Répartition des cas par sexe"
    )
    fig3.update_layout(
        title_font=dict(size=20, color="#F57C00"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0)'
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📅 Évolution des cas dans le temps")
    fig4 = px.line(
        df_filtered.groupby("Date")["Nombre_de_cas"].sum().reset_index(),
        x="Date", y="Nombre_de_cas", markers=True,
        title="📅 Évolution des cas dans le temps"
    )
    fig4.update_traces(line=dict(color="#4CAF50", width=3))
    fig4.update_layout(
        title_font=dict(size=20, color="#4CAF50"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        hovermode="x unified"
    )
    st.plotly_chart(fig4, use_container_width=True)




    # Ici tu peux continuer avec ton code de visualisation
else:
    st.info("Veuillez importer au moins un fichier CSV pour afficher le tableau de bord.")


# ---------- Bandeau de bas de page ----------
st.markdown("""
    <hr style="border-top: 1px solid #4CAF50; margin-top: 50px;"/>
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        &copy; 2025 <strong>Josias Nteme</strong> - Tous droits réservés.
    </div>
""", unsafe_allow_html=True)


