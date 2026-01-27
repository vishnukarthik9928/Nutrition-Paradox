import streamlit as st
import pandas as pd
from sqlalchemy import text

from db_connect import get_engine
from queries_pandas import (
    get_obesity_data,
    get_malnutrition_data
)
# -----------------------------------
# SQL QUERY LABELS (PowerBI-style)
# -----------------------------------
QUERY_LABELS = [
    "Obesity | Top 5 regions (selected year)",
    "Obesity | Top 5 countries",
    "Obesity | India trend",
    "Obesity | Avg by gender",
    "Obesity | Country count by age & level",
    "Obesity | Least reliable countries",
    "Obesity | Avg by age group",
    "Obesity | Consistently low obesity",
    "Obesity | Female > Male gap",
    "Obesity | Global average per year",

    "Malnutrition | Avg by age group",
    "Malnutrition | Top 5 countries",
    "Malnutrition | Africa trend",
    "Malnutrition | Avg by gender",
    "Malnutrition | CI width by age group",
    "Malnutrition | Yearly change (India/Nigeria/Brazil)",
    "Malnutrition | Lowest regions",
    "Malnutrition | Increasing countries",
    "Malnutrition | Min/Max per year",
    "Malnutrition | High CI flags",

    "Combined | Obesity vs Malnutrition",
    "Combined | Gender disparity",
    "Combined | Africa vs Americas",
    "Combined | Obesity up & Malnutrition down",
    "Combined | Age-wise trend"
]

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Global Nutrition Dashboard",
    layout="wide"
)

st.title("🌍 Global Obesity & Malnutrition Dashboard")
st.caption("Streamlit • SQL • Pandas • PowerBI-aligned analytics")

# -----------------------------------
# LOAD DATA (for Pandas visuals)
# -----------------------------------
@st.cache_data
def load_data():
    engine = get_engine()
    obesity_df = get_obesity_data(engine)
    malnutrition_df = get_malnutrition_data(engine)
    return obesity_df, malnutrition_df

obesity, malnutrition = load_data()

# Hide sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fixed filters
year = int(obesity["Year"].max())
countries = ["India", "Nigeria", "Brazil", "United States", "China"]

import plotly.express as px

st.header("🧋 Obesity Analytics")
col1, col2 = st.columns(2)

# -----------------------------
# Top 5 Regions – Avg Obesity
# -----------------------------
with col1:
    st.subheader("Top 5 Regions – Avg Obesity")

    df = (
        obesity[obesity["Year"] == 2022]
        .groupby("Region", as_index=False)["Mean_Estimate"]
        .mean()
        .sort_values("Mean_Estimate", ascending=False)
        .head(5)
    )

    fig = px.bar(
        df,
        x="Region",
        y="Mean_Estimate",
        text_auto=".2f",
        labels={
            "Region": "WHO Region",
            "Mean_Estimate": "Average Obesity (%)"
        },
        title="Top 5 Regions by Average Obesity (2022)"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_tickangle=-40,
        yaxis_title="Average Obesity (%)",
        xaxis_title="Region",
        bargap=0.3
    )

    fig.update_traces(
        textposition="outside",
        selector=dict(type="bar")
    )

    st.plotly_chart(fig, use_container_width=True, key="obesity_regions")

# -----------------------------
# Top 5 Countries – Obesity
# -----------------------------
with col2:
    st.subheader("Top 5 Countries – Obesity")

    df = (
        obesity.groupby("Country", as_index=False)["Mean_Estimate"]
        .mean()
        .sort_values("Mean_Estimate", ascending=False)
        .head(5)
    )

    fig = px.bar(
        df,
        x="Country",
        y="Mean_Estimate",
        text_auto=".2f",
        labels={
            "Country": "Country",
            "Mean_Estimate": "Average Obesity (%)"
        },
        title="Top 5 Countries by Average Obesity"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_tickangle=-30,
        yaxis_title="Average Obesity (%)",
        xaxis_title="Country",
        bargap=0.3
    )

    fig.update_traces(
        textposition="outside",
        selector=dict(type="bar")
    )

    st.plotly_chart(fig, use_container_width=True, key="obesity_countries")

# -----------------------------
# Obesity Trend – India
# -----------------------------
st.subheader("🇮🇳 Obesity Trend – India")

df = (
    obesity[obesity["Country"] == "India"]
    .groupby("Year", as_index=False)["Mean_Estimate"]
    .mean()
)

fig = px.line(
    df,
    x="Year",
    y="Mean_Estimate",
    markers=True,
    labels={
        "Year": "Year",
        "Mean_Estimate": "Average Obesity (%)"
    },
    title="Obesity Trend in India Over Time"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    yaxis_title="Average Obesity (%)",
    xaxis_title="Year"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

st.plotly_chart(fig, use_container_width=True, key="india_trend")

# -----------------------------
# Average Obesity by Gender
# -----------------------------
st.subheader("Average Obesity by Gender")

df_gender = (
    obesity.groupby("Gender", as_index=False)["Mean_Estimate"]
    .mean()
)

fig = px.bar(
    df_gender,
    x="Gender",
    y="Mean_Estimate",
    text_auto=".2f",
    labels={
        "Gender": "Gender",
        "Mean_Estimate": "Average Obesity (%)"
    },
    title="Average Obesity by Gender"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    yaxis_title="Average Obesity (%)",
    xaxis_title="Gender",
    bargap=0.4
)

fig.update_traces(
    textposition="outside",
    selector=dict(type="bar")
)

st.plotly_chart(fig, use_container_width=True, key="obesity_gender")

# -----------------------------
# Global Average Obesity Trend
# -----------------------------
st.subheader("🌐 Global Average Obesity per Year")

df_global = (
    obesity.groupby("Year", as_index=False)["Mean_Estimate"]
    .mean()
)

fig = px.line(
    df_global,
    x="Year",
    y="Mean_Estimate",
    markers=True,
    labels={
        "Year": "Year",
        "Mean_Estimate": "Average Obesity (%)"
    },
    title="Global Average Obesity Trend Over Time"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    yaxis_title="Average Obesity (%)",
    xaxis_title="Year"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(fig, use_container_width=True, key="global_trend")
import plotly.express as px

# -----------------------------------
# 👾 MALNUTRITION SECTION (Plotly-based)
# -----------------------------------
st.header("👾 Malnutrition Analytics")

col3, col4 = st.columns(2)

# -----------------------------
# Top 5 Countries – Malnutrition
# -----------------------------
with col3:
    st.subheader("Top 5 Countries – Malnutrition")

    df_country = (
        malnutrition.groupby("Country", as_index=False)["Mean_Estimate"]
        .mean()
        .sort_values("Mean_Estimate", ascending=False)
        .head(5)
    )

    fig = px.bar(
        df_country,
        x="Country",
        y="Mean_Estimate",
        text_auto=".2f",
        labels={
            "Country": "Country",
            "Mean_Estimate": "Average Malnutrition (%)"
        },
        title="Top 5 Countries by Average Malnutrition"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_tickangle=-30,
        yaxis_title="Average Malnutrition (%)",
        xaxis_title="Country",
        bargap=0.3
    )

    fig.update_traces(
        textposition="outside",
        selector=dict(type="bar")
    )

    st.plotly_chart(fig, use_container_width=True, key="malnutrition_top_countries")

# ---------------------------------
# Regions with Lowest Malnutrition
# ---------------------------------
with col4:
    st.subheader("Regions with Lowest Malnutrition")

    df_region = (
        malnutrition.groupby("Region", as_index=False)["Mean_Estimate"]
        .mean()
        .sort_values("Mean_Estimate", ascending=True)
        .head(5)
    )

    fig = px.bar(
        df_region,
        x="Region",
        y="Mean_Estimate",
        text_auto=".2f",
        labels={
            "Region": "Region",
            "Mean_Estimate": "Average Malnutrition (%)"
        },
        title="Regions with Lowest Average Malnutrition"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_tickangle=-40,
        yaxis_title="Average Malnutrition (%)",
        xaxis_title="Region",
        bargap=0.3
    )

    fig.update_traces(
        textposition="outside",
        selector=dict(type="bar")
    )

    st.plotly_chart(fig, use_container_width=True, key="malnutrition_low_regions")

# -----------------------------
# Africa Malnutrition Trend
# -----------------------------
st.subheader("Africa Malnutrition Trend")

df_africa = (
    malnutrition[malnutrition["Region"] == "Africa"]
    .groupby("Year", as_index=False)["Mean_Estimate"]
    .mean()
)

fig = px.line(
    df_africa,
    x="Year",
    y="Mean_Estimate",
    markers=True,
    labels={
        "Year": "Year",
        "Mean_Estimate": "Average Malnutrition (%)"
    },
    title="Malnutrition Trend in Africa"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    yaxis_title="Average Malnutrition (%)",
    xaxis_title="Year"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(fig, use_container_width=True, key="malnutrition_africa_trend")

# --------------------------------
# Gender-based Average Malnutrition
# --------------------------------
st.subheader("Gender-based Average Malnutrition")

df_gender = (
    malnutrition.groupby("Gender", as_index=False)["Mean_Estimate"]
    .mean()
)

fig = px.bar(
    df_gender,
    x="Gender",
    y="Mean_Estimate",
    text_auto=".2f",
    labels={
        "Gender": "Gender",
        "Mean_Estimate": "Average Malnutrition (%)"
    },
    title="Average Malnutrition by Gender"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    yaxis_title="Average Malnutrition (%)",
    xaxis_title="Gender",
    bargap=0.4
)

fig.update_traces(
    textposition="outside",
    selector=dict(type="bar")
)

st.plotly_chart(fig, use_container_width=True, key="malnutrition_gender")

# -----------------------------
# High CI Width Flags
# -----------------------------
st.subheader("🚨 High CI Width (>5)")

st.dataframe(
    malnutrition[malnutrition["CI_Width"] > 5]
    [["Country", "Year", "CI_Width"]]
)

# -----------------------------------
# 🔗 COMBINED ANALYSIS (Pandas-based)
# -----------------------------------
st.header("🔗 Combined Insights")

combined = obesity.merge(
    malnutrition,
    on=["Country", "Year"],
    suffixes=("_Obesity", "_Malnutrition")
)

st.subheader("Obesity vs Malnutrition Comparison")
st.dataframe(
    combined[
        combined["Country"].isin(countries)
    ][
        ["Country", "Year",
         "Mean_Estimate_Obesity",
         "Mean_Estimate_Malnutrition"]
    ]
)


st.subheader("Age-wise Obesity Trend")
st.dataframe(
    obesity.groupby(["Age_Group", "Year"])["Mean_Estimate"]
    .mean()
    .reset_index()
)
import re
from sqlalchemy import text

def load_sql_queries(file_path="queries.sql"):
    with open(file_path, "r", encoding="utf-8") as f:
        sql_text = f.read()

    # Remove block comments /* ... */
    sql_text = re.sub(r"/\*.*?\*/", "", sql_text, flags=re.DOTALL)

    # Remove single-line comments --
    sql_text = re.sub(r"--.*", "", sql_text)

    # Extract only SELECT queries
    queries = [
        q.strip()
        for q in sql_text.split(";")
        if q.strip().lower().startswith("select")
    ]

    return queries

# -----------------------------------
# 📊 SQL QUERY DROPDOWN (PowerBI-style)
# -----------------------------------
st.header("📊 SQL Analytics (from queries.sql)")

engine = get_engine()
queries = load_sql_queries("queries.sql")

selected_label = st.selectbox(
    "Select SQL Query",
    QUERY_LABELS
)

query_index = QUERY_LABELS.index(selected_label)
query = queries[query_index]

st.code(query, language="sql")

try:
    # Pass year ONLY if query expects it
    if ":year" in query.lower():
        df = pd.read_sql(text(query), engine, params={"year": int(year)})
    else:
        df = pd.read_sql(text(query), engine)

    if df.empty:
        st.warning("No data returned")
    else:
        st.dataframe(df)

        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) >= 1:
            st.bar_chart(
                df.set_index(df.columns[0])[numeric_cols[0]]
            )

except Exception as e:
    st.error("Query execution failed")
    st.code(str(e))

st.success("✅ SQL Analytics loaded successfully")
