import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #00E5FF;
}

h2,h3 {
    color: #00E676;
}

[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 2px solid #00E5FF;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,229,255,0.5);
}
</style>
""", unsafe_allow_html=True)

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(
    page_title="Energy Economy Carbon Analytics",
    page_icon="🌍",
    layout="wide"
)

# -------------------
# LOAD DATA
# -------------------
df = pd.read_csv("data/carbon_clean.csv")

# -------------------
# SIDEBAR
# -------------------
st.sidebar.title("🌍 Navigation")

search_country = st.sidebar.text_input(
    "🔍 Search Country"
)

country_list = sorted(df["country"].dropna().unique())

if search_country:
    country_list = [
        c for c in country_list
        if search_country.lower() in c.lower()
    ]

country = st.sidebar.selectbox(
    "Select Country",
    country_list
)

year = st.sidebar.slider(
    "Select Year",
    int(df["year"].min()),
    int(df["year"].max()),
    2024
)


filtered_df = df[
    (df["country"] == country)
    &
    (df["year"] <= year)
]


# -------------------
# TITLE
# -------------------
st.title("🌍 Energy Economy Carbon Analytics Platform")

st.markdown("""
Analyze carbon emissions, energy consumption,
economic growth and sustainability trends.
""")
rank = (
    df.groupby("country")["co2"]
    .sum()
    .sort_values(ascending=False)
)

if country in rank.index:
    st.success(
        f"🌍 {country} ranks #{rank.index.get_loc(country)+1} globally in total CO₂ emissions"
    )
    latest = filtered_df.iloc[-1]

st.info(
    f"""
    📊 Latest Snapshot

    Country: {country}

    CO₂ Emissions: {latest['co2']:.2f}

    GDP: {latest['gdp']:.0f}

    Population: {latest['population']:.0f}
    """
   )

tab1, tab2, tab3, tab4, tab5 = st.tabs([
"📊 Dashboard",
"🌍 Country Analysis",
"📈 Forecasting",
"⚔️ Compare Countries",
"ℹ️ About"
])

with tab1:

    # KPI CARDS
    col1,col2,col3,col4,col5 = st.columns(5) 

    col1.metric(
        "🌍 Total CO2",
        f"{filtered_df['co2'].sum():,.0f}"
    )

    col2.metric(
        "👥 Population",
        f"{filtered_df['population'].max():,.0f}"
    )

    col3.metric(
        "💰 GDP",
        f"${filtered_df['gdp'].max()/1e9:.2f} B"
    )

    col4.metric(
        "🏭 CO2 Per Capita",
        f"{filtered_df['co2_per_capita'].mean():.2f}"
    )
    if (
    filtered_df["co2"].sum() > 0
    and
    filtered_df["gdp"].mean() > 0
    ):

      sustainability_score = (
        filtered_df["gdp"].mean()
        /
        filtered_df["co2"].sum()
     )
     
    # Sustainability Score
    col5.metric(
        "🌱 Sustainability",
        f"{sustainability_score:,.2f}"
      )
   

    
    st.subheader("🗺️ Global CO₂ Emissions Map")

    map_df = df[df["year"] == year]

    fig_map = px.choropleth(
    map_df,
    locations="iso_code",
    color="co2",
    hover_name="country",
    color_continuous_scale="Turbo",
    title=f"Global CO₂ Emissions ({year})"
    )

    fig_map.update_layout(
    template="plotly_dark",
    height=600
    )

    st.plotly_chart(
    fig_map,
    use_container_width=True
     )
    #==================================================================

    # CO₂ Trend Over Time

    #===================================================================

    st.subheader("📈 CO₂ Trend Over Time")

    fig = px.line(
        filtered_df,
        x="year",
        y="co2",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 GDP vs CO₂")

    scatter_df = filtered_df.dropna(
    subset=["gdp", "co2", "population", "co2_per_capita"]
    )

    fig2 = px.scatter(
    scatter_df,
    x="gdp",
    y="co2",
    size="population",
    color="co2_per_capita",
    hover_name="country"
   )

    fig2.update_layout(
    template="plotly_dark",
    height=600
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("🏭 Top CO₂ Emitting Countries")

    top10 = (
    df[
        ~df["country"].str.contains(
            "income|GCP|OECD|Europe|Asia|Africa|World|Union",
            case=False,
            na=False
        )
    ]
    .groupby("country")["co2"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
    )

    fig3 = px.bar(
        top10,
        x="co2",
        y="country",
        orientation="h",
        color="co2"
    )

    fig3.update_layout(template="plotly_dark")

    st.plotly_chart(fig3, use_container_width=True)


with tab2:

    st.header("🌍 Country Analysis")
    csv = filtered_df.to_csv(index=False)

    st.download_button(
    "📥 Download Country Report",
    csv,
    file_name=f"{country}_report.csv",
    mime="text/csv"
    )

    selected_columns = st.multiselect(
    "Choose Columns",
    filtered_df.columns.tolist(),
    default=[
        "country",
        "year",
        "co2",
        "gdp"
         ]
    )

    st.dataframe(
    filtered_df[selected_columns]
    )
    st.write(f"Currently analyzing: {country}")

    st.metric(
        "Latest CO₂",
        round(filtered_df["co2"].iloc[-1],2)
        if len(filtered_df)>0 else 0
    )

    st.metric(
        "Latest GDP",
        round(filtered_df["gdp"].iloc[-1],2)
        if len(filtered_df)>0 else 0
    )

    st.line_chart(
        filtered_df.set_index("year")["co2"]
    )


with tab3:

    st.header("📈 CO₂ Emission Forecasting")

    forecast_df = filtered_df.dropna(
        subset=["year", "co2"]
    )

    if len(forecast_df) > 10:

        # Features & Target
        X = forecast_df[["year"]]
        y = forecast_df["co2"]

        # Polynomial Regression
        poly = PolynomialFeatures(degree=3)

        X_poly = poly.fit_transform(X)

        model = LinearRegression()

        model.fit(
            X_poly,
            y
        )

        # Future Years
        future_years = np.arange(
            forecast_df["year"].max() + 1,
            forecast_df["year"].max() + 21
        ).reshape(-1, 1)

        future_poly = poly.transform(
            future_years
        )

        predictions = model.predict(
            future_poly
        )

        # Avoid Negative Predictions
        predictions = np.maximum(
            predictions,
            0
        )

        future_df = pd.DataFrame({
            "year": future_years.flatten(),
            "predicted_co2": predictions
        })

        st.subheader(
            f"Future CO₂ Forecast for {country}"
        )

        # Historical Data
        fig_forecast = px.line(
            forecast_df,
            x="year",
            y="co2",
            title=f"{country} Historical vs Forecasted CO₂"
        )

        # Forecast Line
        fig_forecast.add_scatter(
            x=future_df["year"],
            y=future_df["predicted_co2"],
            mode="lines+markers",
            name="Polynomial Forecast"
        )

        fig_forecast.update_layout(
            template="plotly_dark",
            height=650,
            xaxis_title="Year",
            yaxis_title="CO₂ Emissions"
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )

        # 2040 Prediction
        prediction_2040 = future_df[
            future_df["year"] == 2040
        ]["predicted_co2"].values[0]

        st.metric(
            "📊 Predicted CO₂ in 2040",
            f"{prediction_2040:,.2f}"
        )

        st.info(
            "Forecast generated using Polynomial Regression (Degree 3) based on historical CO₂ trends."
        )

    else:

        st.warning(
            "Not enough historical data available for forecasting."
        )
with tab4:

    st.header("⚔️ Compare Countries")

    country1 = st.selectbox(
        "Country 1",
        country_list,
        key="country1"
    )

    country2 = st.selectbox(
        "Country 2",
        country_list,
        key="country2"
    )

    compare_df1 = df[
        df["country"] == country1
    ]

    compare_df2 = df[
        df["country"] == country2
    ]

    fig_compare = px.line(
        title=f"{country1} vs {country2} CO₂ Emissions"
    )

    fig_compare.add_scatter(
        x=compare_df1["year"],
        y=compare_df1["co2"],
        mode="lines",
        name=country1
    )

    fig_compare.add_scatter(
        x=compare_df2["year"],
        y=compare_df2["co2"],
        mode="lines",
        name=country2
    )

    fig_compare.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )

with tab5:

    st.header("ℹ️ About Project")

    st.write("""
    ### Energy Economy Carbon Analytics Platform

    Features:
    - Global CO₂ Emissions Map
    - Country Analysis
    - GDP vs CO₂ Relationship
    - Country Comparison
    - Downloadable Reports
    - Forecasting Module

    Technologies Used:
    - Python
    - Pandas
    - Plotly
    - Streamlit
    - Power BI

    Developed as an Energy + Data Analytics project.
    """)