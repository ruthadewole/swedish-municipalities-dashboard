import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv(
    "swedish_municipalities.csv",
    dtype={"code": str}
)
df.loc[
    df["municipality"] == "Borgholm",
    "land_area_km2"
] = 676.76

df.loc[
    df["municipality"] == "Essunga",
    "land_area_km2"
] = 234.53

county_to_region = {
    "Blekinge": "South",
    "Gotland": "South",
    "Halland": "South",
    "Jönköping": "South",
    "Kalmar": "South",
    "Kronoberg": "South",
    "Skåne": "South",
    "Västra Götaland": "South",
    "Östergötland": "South",

    "Dalarna": "Central",
    "Stockholm": "Central",
    "Södermanland": "Central",
    "Uppsala": "Central",
    "Värmland": "Central",
    "Västmanland": "Central",
    "Örebro": "Central",

    "Gävleborg": "North",
    "Jämtland": "North",
    "Norrbotten": "North",
    "Västerbotten": "North",
    "Västernorrland": "North"
}


df["region"] = df["county"].map(county_to_region)
st.sidebar.header("Filters")

region_options = [
    "All regions",
    "South",
    "Central",
    "North"
]


selected_region = st.sidebar.selectbox(
    "Choose a region",
    region_options
)

if selected_region == "All regions":
    filtered_df = df
else:
    filtered_df = df[df["region"] == selected_region]

st.title("Swedish Municipalities Dashboard")

st.write("Population data for Sweden's 290 municipalities.")

st.subheader("Overview")
total_municipalities = len(filtered_df)
total_population = filtered_df["population"].sum()


column1, column2 = st.columns(2)

column1.metric(
    "Number of municipalities",
    total_municipalities,
        border=True

)

column2.metric(
    "Total population",
    f"{total_population:,.0f}",
        border=True


)
st.subheader("Density and land-area extremes")

highest_density = filtered_df.loc[
    filtered_df["density"].idxmax()
]

lowest_density = filtered_df.loc[
    filtered_df["density"].idxmin()
]

largest_land_area = filtered_df.loc[
    filtered_df["land_area_km2"].idxmax()
]

smallest_land_area = filtered_df.loc[
    filtered_df["land_area_km2"].idxmin()
]

density_column1, density_column2 = st.columns(2)

density_column1.metric(
    f"Highest density — {highest_density['municipality']}",
    f"{highest_density['density']:,.1f} people/km²",
        border=True

)

density_column2.metric(
    f"Lowest density — {lowest_density['municipality']}",
    f"{lowest_density['density']:,.1f} people/km²",
        border=True

)

area_column1, area_column2 = st.columns(2)

area_column1.metric(
    f"Largest land area — {largest_land_area['municipality']}",
    f"{largest_land_area['land_area_km2']:,.1f} km²",
        border=True

)

area_column2.metric(
    f"Smallest land area — {smallest_land_area['municipality']}",
    f"{smallest_land_area['land_area_km2']:,.1f} km²",
        border=True

)
st.subheader("Top 10 municipalities by population")

top_10_population = filtered_df.nlargest(
    10,"population"
)

st.bar_chart(
    top_10_population,
    x="municipality",
    y="population",
    horizontal=True,
    sort="-population",
    color="municipality"

)


st.subheader("Regional population comparison")

region_summary = (
    df.groupby("region", as_index=False)
    .agg(
        municipalities=("municipality", "count"),
        population=("population", "sum")
    )
)

population_pie = px.pie(
    region_summary,
    names="region",
    values="population",
    color="region",
    color_discrete_map={
        "South": "#F4A261",
        "Central": "#457B9D",
        "North": "#2A9D8F"
    },
    title="Percentage of Sweden's population by region"
)

population_pie.update_traces(
    textposition="inside",
    textinfo="label+percent"
)

st.plotly_chart(
    population_pie,
    width="stretch"
)



st.dataframe(
    filtered_df,
    hide_index=True
)


st.dataframe(df)

