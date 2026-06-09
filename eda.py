import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/owid-co2-data.csv")

# ...........................Understanding Data..........................................................................................
'''
# Check dataset size
print("Dataset Shape:", df.shape)

# First 5 rows
print(df.head())

# World data
world = df[df["country"] == "World"]

# Plot
plt.figure(figsize=(12,6))
plt.plot(world["year"], world["co2"])

plt.title("Global CO₂ Emissions Over Time")
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions")
plt.grid(True)

#plt.show()

print(df.info())

print(df.isnull().sum().sort_values(ascending=False))

print(df.duplicated().sum())

print(world.shape)

print(df.describe())
'''
#..................................Data Cleaning.................................................................................



important_cols = [
    "country",
    "year",
    "co2",
    "co2_per_capita",
    "population",
    "gdp",
    "coal_co2",
    "oil_co2",
    "gas_co2",
    "iso_code",
    "methane",
    "total_ghg",
    "temperature_change_from_co2"
] 

df_clean = df[important_cols]

'''print(df_clean.head())
print(df_clean.shape)
print(df_clean.columns) 

print(df_clean.isnull().sum().sort_values(ascending=False))

print(df_clean["country"].nunique())

print(df_clean["year"].min())

print(df_clean["year"].max())
'''

df_country = df_clean[
    (df_clean["iso_code"].notna()) &
    (df_clean["iso_code"].str.len() == 3)
]

latest_year = df_country["year"].max()

top_emitters = (
    df_country[df_country["year"] == latest_year]
    .sort_values("co2", ascending=False)
    [["country","co2"]]
    .head(10)
)

print(top_emitters)

#......................................Creating separated dataset................................................................


#..................................World dataset............................................................................

df_world= df_clean[df_clean['country'] == 'World']
print(df_world.head())
print(df_world.shape)

#...................................Major Countries................................................................................

df_major = df_clean[
    df_clean["country"].isin(
        ["India","China","United States","World"]
    )
]

#....................................Modern Era...................................................................................

print(df_clean[df_clean["gdp"].notnull()]["year"].min())
df_modern = df_clean[df_clean["year"] >= 1990]

print(df["year"].min())
print(df["year"].max())