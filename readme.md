# Tableau de bord des campagnes de santé publique \U0001F489

Cette application Streamlit permet d'analyser les données relatives aux campagnes de santé publique en République Démocratique du Congo. Elle offre une visualisation interactive des cas de maladies enregistrés selon les régions, les tranches d'âge, le sexe et dans le temps.

## Fonctionnalités
- Téléversement de fichiers CSV de données de santé publique
- Filtres interactifs sur : maladies, régions, sexes, tranches d'âge
- Statistiques clés : total de cas, nombre d'enregistrements
- Graphiques dynamiques avec Plotly :
  - Barres des cas par maladie
  - Camembert de la répartition régionale
  - Ligne temporelle de l'évolution des cas
- Animations attrayantes via Lottie

##  Données attendues
Le fichier CSV importé doit contenir les colonnes suivantes :
- `Date` (format AAAA-MM-JJ)
- `Région`
- `Maladie`
- `Sexe`
- `Tranche_d_âge`
- `Nombre_de_cas`

##  Technologies utilisées
- [Streamlit](https://streamlit.io)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Pandas](https://pandas.pydata.org)
- [Lottie](https://lottiefiles.com) pour les animations

## Lancer l'application localement
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Auteur
**Josias Nteme**  
Statisticien, Data Analyst & Data Scientist passionné par l'impact de la donnée sur les politiques publiques.

- GitHub : [github.com/josiasnteme](https://github.com/josiasnteme)
- LinkedIn : [linkedin.com/in/josiasnteme](https://linkedin.com/in/josiasnteme)
- Email : josias76nteme@gmail.com

![Logo du projet](A_logo_for_an_e-commerce_dashboard_is_displayed_in.png)

---
> Ce projet est réalisé dans un but éducatif et peut être adapté pour tout besoin de visualisation de données en santé publique.
