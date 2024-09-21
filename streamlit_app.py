import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

@st.cache
def load_data():
    # Load cancer data and population data
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

    # Merge the cancer and population data
    df = pd.merge(left=cancer_df, right=pop_df, how="left")

    # Fill missing population values by backfilling, grouped by Country, Sex, and Age
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")

    # Drop any remaining rows with missing data
    df.dropna(inplace=True)

    # Group by relevant columns and sum the Deaths and Pop values
    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()

    # Calculate the cancer mortality rate per 100,000 population
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
# replace with st.radio
sex = st.radio("Select Sex", options=["M", "F"], index=0)  # Default to "M"

# Further filter the dataset based on the selected sex
subset = subset[subset["Sex"] == sex]
### P2.2 ###

# Display the filtered subset
st.write(subset)
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

# Heatmap with selection
heatmap = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country", title="Country"),
    color=alt.Color(
        "Rate",
        scale=alt.Scale(type="log", domain=[0.01, 1000], clamp=True),
        title="Mortality rate per 100k"
    ),
    tooltip=[alt.Tooltip('Country'), alt.Tooltip('Age'), alt.Tooltip('Rate', title='Mortality rate per 100k')]
).add_selection(
    click  # Add interactive selection
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
    height=300
)

# Bar chart for the sum of population, filtered by selected age
population_bar = alt.Chart(subset).mark_bar().encode(
    x=alt.X('sum(Pop):Q', title='Total Population'),
    y=alt.Y('Country:N', sort='-x'),
    tooltip=[alt.Tooltip('Country'), alt.Tooltip('sum(Pop):Q', title='Total Population')]
).transform_filter(
    click  # Filter to display only data for selected age groups
).properties(
    title="Population by country for selected age group",
    height=300
)

# Existing bar chart code for total population by country
population_total = alt.Chart(df).mark_bar().encode(
    x=alt.X("Pop:Q", title="Sum of population size"),
    y=alt.Y("Country:O", sort='-x'),
    tooltip=[alt.Tooltip('Country'), alt.Tooltip('Pop:Q', title='Sum of population size')]
).properties(
    title="Sum of population size by country",
    height=300
)

# Combine all charts vertically
combined_chart = alt.vconcat(heatmap, population_bar, population_total)

# Display the chart in Streamlit
st.altair_chart(combined_chart, use_container_width=True)
### P2.5 ###

st.altair_chart(combined_chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
