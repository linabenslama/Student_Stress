#Analyse Par Chaima Bouazza & Lina Ben Slama
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# CONFIGURATION DE LA PAGE

st.set_page_config(
    page_title="Student Stress Dashboard",
    page_icon="📚",
    layout="wide"
)

# CHARGEMENT DES DONNÉES

@st.cache_data
def load_data():
    df = pd.read_csv("student_stress_dataset.csv")
    df["stress"] = df["stress_level"].map({"Low": 1, "Medium": 2, "High": 3})
    return df

df = load_data()

# BARRE DE NAVIGATION

st.sidebar.title("📚 Student Stress")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Accueil", "📊 Analyse Univariée", "🔗 Analyse Bivariée", "🎛️ Filtres Interactifs", "📝 Synthèse"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filtres globaux**")

stress_filter = st.sidebar.multiselect(
    "Niveau de stress",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("*DS2 – Étude de cas · IHEC Carthage*")

# Appliquer le filtre global
df_filtered = df[df["stress_level"].isin(stress_filter)]

# Vérification : filtre vide
if len(df_filtered) == 0:
    st.warning("⚠️ Aucun étudiant sélectionné. Veuillez choisir au moins un niveau de stress dans la barre latérale.")
    st.stop()

ORDER = ["Low", "Medium", "High"]
COLORS = ["#2ecc71", "#f39c12", "#e74c3c"]

# PAGE 1 — ACCUEIL

if page == "🏠 Accueil":

    st.title("📚 Dashboard — Student Stress & Study Behavior")
    st.markdown("Analyse des facteurs influençant le stress des étudiants")
    st.info("📌 Ce dashboard explore les relations entre les habitudes d'étude, de sommeil, l'usage des réseaux sociaux et le niveau de stress des étudiants.")
    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👥 Étudiants sélectionnés", len(df_filtered))
    with col2:
        avg_score = round(df_filtered["exam_score"].mean(), 1)
        st.metric("📝 Note moyenne", avg_score)
    with col3:
        avg_sleep = round(df_filtered["sleep_hours"].mean(), 1)
        st.metric("😴 Sommeil moyen", f"{avg_sleep}h")
    with col4:
        avg_study = round(df_filtered["study_hours"].mean(), 1)
        st.metric("📖 Étude moyenne", f"{avg_study}h")
    with col5:
        avg_social = round(df_filtered["social_media_hours"].mean(), 1)
        st.metric("📱 Réseaux sociaux", f"{avg_social}h")

    st.markdown("---")

    # Deux colonnes pour les graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Répartition du niveau de stress")
        counts = df_filtered["stress_level"].value_counts().reindex(ORDER).fillna(0)
        fig, ax = plt.subplots()
        bars = ax.bar(ORDER, counts.values, color=COLORS, edgecolor="white")
        ax.set_xlabel("Niveau de stress")
        ax.set_ylabel("Nombre d'étudiants")
        for i, v in enumerate(counts.values):
            ax.text(i, v + 0.3, str(int(v)), ha="center", fontweight="bold")
        st.pyplot(fig)
        plt.close()

    with col_right:
        st.subheader("Note moyenne par niveau de stress")
        kpi = (
            df_filtered.groupby("stress_level")["exam_score"].mean().reindex(ORDER).fillna(0).round(1))
        fig2, ax2 = plt.subplots()
        ax2.bar(ORDER, kpi.values, color=COLORS, edgecolor="white")
        ax2.set_xlabel("Niveau de stress")
        ax2.set_ylabel("Note moyenne")
        for i, v in enumerate(kpi.values):
            ax2.text(i, v + 0.5, str(v), ha="center", fontweight="bold")
        st.pyplot(fig2)
        plt.close()

    st.success("✅ Observation : les étudiants à faible stress obtiennent de meilleures notes. Le stress est un facteur clé de la réussite académique.")

    st.markdown("---")
    st.subheader("📋 Aperçu des données")
    st.dataframe(df_filtered.head(10), use_container_width=True)

# PAGE 2 — ANALYSE UNIVARIÉE

elif page == "📊 Analyse Univariée":

    st.title("📊 Analyse Univariée")
    st.markdown("Distribution de chaque variable individuellement")
    st.info("📌 Sélectionnez une variable pour visualiser sa distribution et ses statistiques principales.")
    st.markdown("---")

    variable = st.selectbox(
        "Choisissez une variable",["study_hours", "sleep_hours", "social_media_hours", "exam_score"] )

    labels = {
        "study_hours": "Heures d'étude",
        "sleep_hours": "Heures de sommeil",
        "social_media_hours": "Heures réseaux sociaux",
        "exam_score": "Score à l'examen"
    }
    colors_map = {
        "study_hours": "#3498db",
        "sleep_hours": "#2ecc71",
        "social_media_hours": "#e74c3c",
        "exam_score": "#9b59b6"
    }
    interpretations = {
        "study_hours": "Les heures d'étude varient de 1 à 7h avec une moyenne de ~3.5h. La répartition est homogène : chaque durée est presque également représentée.",
        "sleep_hours": "Les heures de sommeil varient de 4 à 8h avec une moyenne de ~6h. La majorité des étudiants dorment 6h par nuit.",
        "social_media_hours": "Les heures sur les réseaux sociaux varient de 1 à 7h avec une moyenne de ~3.8h. Une distribution assez étalée.",
        "exam_score": "Les scores varient de 40 à 95 avec une moyenne de ~64. La distribution révèle un groupe à faible score et un groupe performant."
    }

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Distribution — {labels[variable]}")
        fig, ax = plt.subplots()
        if variable == "exam_score":
            ax.hist(df_filtered[variable], bins=10, color=colors_map[variable], edgecolor="white")
        else:
            counts = df_filtered[variable].value_counts().sort_index()
            ax.bar(counts.index, counts.values, color=colors_map[variable], edgecolor="white")
        ax.set_xlabel(labels[variable])
        ax.set_ylabel("Nombre d'étudiants")
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader(f"Statistiques — {labels[variable]}")
        stats = df_filtered[variable].describe().round(2)
        st.dataframe(stats.to_frame(name="Valeur"), use_container_width=True)

        st.markdown("---")
        st.markdown(f"**Minimum :** {df_filtered[variable].min()}")
        st.markdown(f"**Maximum :** {df_filtered[variable].max()}")
        st.markdown(f"**Moyenne :** {df_filtered[variable].mean():.2f}")
        st.markdown(f"**Médiane :** {df_filtered[variable].median()}")

    st.markdown("---")
    st.success(f"✅ Interprétation : {interpretations[variable]}")

# PAGE 3 — ANALYSE BIVARIÉE

elif page == "🔗 Analyse Bivariée":

    st.title("🔗 Analyse Bivariée")
    st.markdown("Relations entre les variables")
    st.info("📌 L'analyse bivariée permet de comprendre comment deux variables évoluent ensemble et d'identifier des corrélations.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📈 Scatter Plot", "📊 Moyennes par stress", "🔥 Corrélations"])

    # TAB 1 : Scatter plot
    with tab1:
        st.subheader("Relation entre deux variables")

        col1, col2 = st.columns(2)
        with col1:
            x_var = st.selectbox("Variable X", ["study_hours", "sleep_hours", "social_media_hours"], key="x")
        with col2:
            y_var = st.selectbox("Variable Y", ["exam_score", "study_hours", "sleep_hours"], key="y")

        fig = px.scatter(
            df_filtered,
            x=x_var,
            y=y_var,
            color="stress_level",
            color_discrete_map={"Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"},
            title=f"{x_var} vs {y_var}",
            labels={x_var: x_var.replace("_", " ").title(), y_var: y_var.replace("_", " ").title()}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 Chaque point représente un étudiant. La couleur indique son niveau de stress.")

    # TAB 2 : Moyennes par stress
    with tab2:
        st.subheader("Moyennes par niveau de stress")

        kpi = (
            df_filtered.groupby("stress_level")[
                ["study_hours", "sleep_hours", "social_media_hours", "exam_score"]
            ]
            .mean()
            .round(2)
            .reindex(ORDER)
        )
        st.dataframe(kpi, use_container_width=True)
        st.markdown("---")

        var_choice = st.selectbox(
            "Variable à visualiser",
            ["study_hours", "sleep_hours", "social_media_hours", "exam_score"]
        )
        fig, ax = plt.subplots()
        ax.bar(ORDER, kpi[var_choice].values, color=COLORS, edgecolor="white")
        ax.set_xlabel("Niveau de stress")
        ax.set_ylabel(f"Moyenne {var_choice}")
        for i, v in enumerate(kpi[var_choice].values):
            ax.text(i, v + 0.2, str(round(v, 1)), ha="center", fontweight="bold")
        st.pyplot(fig)
        plt.close()

        # Interprétation automatique
        low_val = kpi[var_choice].get("Low", 0)
        high_val = kpi[var_choice].get("High", 0)
        if low_val > high_val:
            st.success(f"✅ Les étudiants à stress faible ont une moyenne plus élevée de **{var_choice}** ({low_val}) que ceux à stress élevé ({high_val}).")
        else:
            st.warning(f"⚠️ Les étudiants à stress élevé ont une moyenne plus élevée de **{var_choice}** ({high_val}) que ceux à stress faible ({low_val}).")

    # TAB 3 : Matrice de corrélation 
    with tab3:
        st.subheader("Matrice de corrélation")
        cols = ["study_hours", "sleep_hours", "social_media_hours", "exam_score", "stress"]
        corr = df_filtered[cols].corr().round(2)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(
            corr, annot=True, cmap="RdYlGn",
            linewidths=0.5, ax=ax, vmin=-1, vmax=1
        )
        ax.set_title("Matrice de corrélation")
        st.pyplot(fig)
        plt.close()

        st.markdown("---")
        st.markdown("**Interprétation :**")
        st.markdown("- 🟢 **Vert** = corrélation positive (les deux variables augmentent ensemble)")
        st.markdown("- 🔴 **Rouge** = corrélation négative (l'une augmente, l'autre diminue)")
        st.success("✅ La matrice confirme : le score est fortement lié aux heures d'étude (+) et de sommeil (+), et négativement lié aux réseaux sociaux et au stress (-).")

# PAGE 4 — FILTRES INTERACTIFS

elif page == "🎛️ Filtres Interactifs":

    st.title("🎛️ Filtres Interactifs")
    st.markdown("Explorez les données selon vos critères")
    st.info("📌 Utilisez les curseurs ci-dessous pour filtrer les étudiants selon leurs heures d'étude, de sommeil et leur score à l'examen.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        study_range = st.slider(
            "Heures d'étude",
            min_value=int(df["study_hours"].min()),
            max_value=int(df["study_hours"].max()),
            value=(int(df["study_hours"].min()), int(df["study_hours"].max()))
        )
    with col2:
        sleep_range = st.slider(
            "Heures de sommeil",
            min_value=int(df["sleep_hours"].min()),
            max_value=int(df["sleep_hours"].max()),
            value=(int(df["sleep_hours"].min()), int(df["sleep_hours"].max()))
        )
    with col3:
        score_range = st.slider(
            "Score à l'examen",
            min_value=int(df["exam_score"].min()),
            max_value=int(df["exam_score"].max()),
            value=(int(df["exam_score"].min()), int(df["exam_score"].max()))
        )

    # Appliquer les filtres
    df_custom = df_filtered[
        (df_filtered["study_hours"] >= study_range[0]) &
        (df_filtered["study_hours"] <= study_range[1]) &
        (df_filtered["sleep_hours"] >= sleep_range[0]) &
        (df_filtered["sleep_hours"] <= sleep_range[1]) &
        (df_filtered["exam_score"] >= score_range[0]) &
        (df_filtered["exam_score"] <= score_range[1])
    ]

    # Affichage du nombre de résultats
    if len(df_custom) == 0:
        st.error("❌ Aucun étudiant ne correspond à ces critères. Élargissez vos filtres.")
        st.stop()
    else:
        st.success(f"✅ **{len(df_custom)} étudiants** correspondent à vos critères.")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Résultats filtrés")
        st.dataframe(
            df_custom[["study_hours", "sleep_hours", "social_media_hours", "exam_score", "stress_level"]],
            use_container_width=True
        )

    with col_b:
        st.subheader("Répartition du stress (filtrée)")
        counts = df_custom["stress_level"].value_counts().reindex(ORDER).fillna(0)
        fig, ax = plt.subplots()
        ax.bar(ORDER, counts.values, color=COLORS, edgecolor="white")
        ax.set_xlabel("Niveau de stress")
        ax.set_ylabel("Nombre d'étudiants")
        for i, v in enumerate(counts.values):
            ax.text(i, v + 0.1, str(int(v)), ha="center", fontweight="bold")
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Statistiques des étudiants filtrés")
    st.dataframe(
        df_custom[["study_hours", "sleep_hours", "social_media_hours", "exam_score"]].describe().round(2),
        use_container_width=True )

# PAGE 5 — SYNTHÈSE

elif page == "📝 Synthèse":

    st.title("📝 Synthèse — Bilan de l'Analyse")
    st.markdown("Conclusions et recommandations issues de l'étude")
    st.info("📌 Cette page résume les principales découvertes de notre analyse du stress étudiant.")
    st.markdown("---")

    # ── KPIs de synthèse ──
    st.subheader("🔢 Chiffres clés du dataset complet")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👥 Total étudiants", len(df))
    with c2:
        st.metric("📝 Note moyenne globale", round(df["exam_score"].mean(), 1))
    with c3:
        best_group = df.groupby("stress_level")["exam_score"].mean().idxmin()
        worst_score = round(df.groupby("stress_level")["exam_score"].mean().min(), 1)
        st.metric("🔴 Note moyenne des étudiants à stress élevé", f"  {worst_score}/100")
    with c4:
        best_score = round(df.groupby("stress_level")["exam_score"].mean().max(), 1)
        st.metric("🟢 Note moyenne des étudiants à stress faible", f"  {best_score}/100")

    st.markdown("---")

    #  Conclusions principales
    st.subheader("📌 Conclusions principales")

    tab_a, tab_b, tab_c = st.tabs(["📚 Étude & Notes", "😴 Sommeil & Stress", "📱 Réseaux sociaux"])

    with tab_a:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
**✅ Étudier plus = meilleures notes**

L'analyse confirme une relation **positive et forte** entre les heures d'étude et le score à l'examen :

- 1h d'étude → moyenne de **41 points**
- 7h d'étude → moyenne de **90 points**

Les étudiants à stress **faible** étudient en moyenne **5h/jour**, contre **2h** pour les étudiants à stress élevé.
            """)
        with col2:
            grp = df.groupby("study_hours")["exam_score"].mean().round(1)
            fig, ax = plt.subplots()
            ax.plot(grp.index, grp.values, marker="o", color="#3498db", linewidth=2)
            ax.fill_between(grp.index, grp.values, alpha=0.15, color="#3498db")
            ax.set_xlabel("Heures d'étude")
            ax.set_ylabel("Note moyenne")
            ax.set_title("Note moyenne par heures d'étude")
            st.pyplot(fig)
            plt.close()

    with tab_b:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
**😴 Dormir suffisamment réduit le stress**

Le sommeil est un facteur clé de bien-être et de performance :

- Stress **faible** → moyenne de **8h** de sommeil
- Stress **élevé** → moyenne de **5h** de sommeil

Les étudiants qui dorment 8h obtiennent en moyenne **88 points**, contre **40** pour ceux qui dorment 4h.""")
        with col2:
            grp2 = df.groupby("sleep_hours")["exam_score"].mean().round(1)
            fig, ax = plt.subplots()
            ax.bar(grp2.index, grp2.values, color="#2ecc71", edgecolor="white")
            ax.set_xlabel("Heures de sommeil")
            ax.set_ylabel("Note moyenne")
            ax.set_title("Note moyenne par heures de sommeil")
            st.pyplot(fig)
            plt.close()

    with tab_c:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(""" **📱 Les réseaux sociaux nuisent aux résultats**

Une relation **négative et claire** est observée :

- 1h sur les réseaux → moyenne de **88 points**
- 7h sur les réseaux → moyenne de **41 points**

Les étudiants à stress **élevé** passent en moyenne **6h/jour** sur les réseaux sociaux, contre **1h** pour les étudiants à stress faible.""")
        with col2:
            grp3 = df.groupby("social_media_hours")["exam_score"].mean().round(1)
            fig, ax = plt.subplots()
            ax.bar(grp3.index, grp3.values, color="#e74c3c", edgecolor="white")
            ax.set_xlabel("Heures réseaux sociaux")
            ax.set_ylabel("Note moyenne")
            ax.set_title("Note moyenne par heures réseaux sociaux")
            st.pyplot(fig)
            plt.close()

    st.markdown("---")

    #  Recommandations 
    st.subheader("💡 Recommandations")
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.success("📚 **Étudier minimum 4h/jour** pour viser une note supérieure à 70/100.")
    with col_r2:
        st.success("😴 **Dormir au moins 7h par nuit** pour réduire le stress et améliorer les performances.")
    with col_r3:
        st.warning("📱 **Limiter les réseaux sociaux à 2h/jour** pour éviter un impact négatif sur les résultats.")

    st.markdown("---")

    #  Tableau récapitulatif 
    st.subheader("📊 Tableau comparatif par niveau de stress")
    recap = (
        df.groupby("stress_level")[["study_hours", "sleep_hours", "social_media_hours", "exam_score"]].mean().round(2).reindex(["Low", "Medium", "High"])
        .rename(columns={
            "study_hours": "Heures d'étude",
            "sleep_hours": "Heures de sommeil",
            "social_media_hours": "Réseaux sociaux",
            "exam_score": "Note moyenne" }) )
    st.dataframe(recap, use_container_width=True)
