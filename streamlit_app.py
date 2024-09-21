import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

@st.cache
def load_data():
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Cancer", "Sex"],
        var_name="Age",
        value_name="Deaths",
    )

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
    )

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)
    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

    return df

df = load_data()

### P1.2 ###

st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())
year = st.slider("Select Year", min_year, max_year, min_year)
subset = df[df["Year"] == year]

### P2.1 ###

### P2.2 ###
sex = st.radio("Select Sex", options=["M", "F"], index=0) 
subset = subset[subset["Sex"] == sex]
### P2.2 ###

### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
available_countries = df["Country"].unique().tolist()
countries = st.multiselect(
    "Select Countries", 
    options=available_countries, 
    default=[
        "Austria",
        "Germany",
        "Iceland",
        "Spain",
        "Sweden",
        "Thailand",
        "Turkey"
    ]
)

subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
available_cancers = df["Cancer"].unique().tolist()
cancer = st.selectbox(
    "Select Cancer Type", 
    options=available_cancers, 
    index=available_cancers.index("Malignant neoplasm of stomach")
)

subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

click = alt.selection_multi(fields=['Age'], bind='legend')

if subset.empty:
    st.error("No data available for the given selection.")
else:
    ### Heatmap: Mortality rate by country and age group
    heatmap = alt.Chart(subset).mark_rect().encode(
        x=alt.X("Age", sort=["Age <5", "Age 5-14", "Age 15-24", "Age 25-34", "Age 35-44", "Age 45-54", "Age 55-64", "Age >64"]),
        y=alt.Y("Country", title="Country"),
        color=alt.Color("Rate", scale=alt.Scale(type="log", domain=[0.01, 1000], clamp=True), title="Mortality rate per 100k"),
        tooltip=[alt.Tooltip('Country'), alt.Tooltip('Age'), alt.Tooltip('Rate', title='Mortality rate per 100k')]
    ).properties(title=f"{cancer} mortality rates for {sex} in {year}", height=300)

    ### Population Bar Chart: Total population by country for the selected age group
    population_bar = alt.Chart(subset).mark_bar().encode(
        x=alt.X('sum(Pop):Q', title='Total Population'),
        y=alt.Y('Country:N', sort='-x'),
        tooltip=[alt.Tooltip('Country'), alt.Tooltip('sum(Pop):Q', title='Total Population')]
    ).properties(title="Total Population by Country", height=300)

    ### Age Distribution: Population distribution across age groups by country
    age_distribution = alt.Chart(subset).mark_bar().encode(
        x=alt.X('sum(Pop):Q', stack='normalize', title='Population Distribution (%)'),
        y=alt.Y('Country:N', sort='-x', title='Country'),
        color=alt.Color('Age:N', legend=alt.Legend(title="Age Groups")),
        tooltip=[alt.Tooltip('Country:N'), alt.Tooltip('Age:N'), alt.Tooltip('sum(Pop):Q')]
    ).properties(title="Age Distribution by Country", height=300)

    combined_chart = alt.vconcat(heatmap, population_bar, age_distribution)
    st.altair_chart(combined_chart, use_container_width=True)

### P2.5 ###

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data available for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")