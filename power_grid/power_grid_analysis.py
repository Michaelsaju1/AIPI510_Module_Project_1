#%% md
# ## Power Grid Analysis
# 
# For our AIPI 510 Data Storytelling project, we intend to use the EIA.gov EIA-930 Data. This shows the generation and energy consumption for the electrical powergrid in the United States.
#%% md
# ## Load the Data
# 
# We're going to load a full year's worth of data. This is looking at July 2024 - June 2025. We'll download both files now.
#%%
import urllib.request
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

path = Path()

files = {
    "EIA930_BALANCE_2025_Jan_Jun.csv": "https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2025_Jan_Jun.csv",
    "EIA930_BALANCE_2024_Jul_Dec.csv": "https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2024_Jul_Dec.csv",
    "EIA930_Reference_Tables.xlsx": "https://www.eia.gov/electricity/930-content/EIA930_Reference_Tables.xlsx"
}

# Download each file
for key, value in files.items():
    filename = path / key
    url = value
    # If the file does not already exist in the directory, download it
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)
#%% md
# ## Read Data
# 
# Our first step is to understand the data and read the rows and columns that exist. We need to explore and understand what all of the columns actually mean before we can work with the data.
#%%
df1 = pd.read_csv("EIA930_BALANCE_2024_Jul_Dec.csv")
df2 = pd.read_csv("EIA930_BALANCE_2025_Jan_Jun.csv")

# Concat both dataframes
df = pd.concat([df1, df2], ignore_index=True)

df["UTC Time at End of Hour"] = pd.to_datetime(df["UTC Time at End of Hour"])

print(df["UTC Time at End of Hour"].min(), "to", df["UTC Time at End of Hour"].max())

print(df.columns)

df.head(10)
#%% md
# ## Understanding the data
# 
# At first, there appear to be a lot of columns. If we look at the first ten, we can see that there are a lot of NaN values. However, the reason is that this is for only one balancing authority. Each balancing authority uses different types of power generation to meet demand. We're only seeing the first ten hours from the AECI balancing authority. It would be illogical to assume that one authority could have *every* type of power generation. If we look at another balancing authority, we can see the missing values are different. Below is the AVA balancing authority. You can see that they generate power with solar, whereas AECI does not. The key takeaway is that different balancing authorities have different ways of generating power.
#%%
df.iloc[4419:4429]
#%% md
# ## Explaining the meaning of our columns
# 
# After a quick glance at the data, we can tell based on the dates and times that we have time series data down to the hour. However, there are a couple things that are not as intuitive that are explained below:
# 
# First, it is important to understand what some of the terminology means:
# 
#  - Balancing Authority (BA's): are the companies responsible for balancing electricity supply, demand, and interchange on their electric systems in real time. There are many BAs and the spreadsheet with more information about what they mean can be found here: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.eia.gov%2Felectricity%2F930-content%2FEIA930_Reference_Tables.xlsx&wdOrigin=BROWSELINK
# 
#  - Demand: Derived by taking the total metered net electricity generation within its
# electric system and subtracting the total metered net electricity interchange occurring
# between the BA and its neighboring BAs. Total demand should equal or approximate the sum of demand by subregion.
# 
#  - Net generation: Derived from the metered output of electric generating units in a
# BA's electric system. Generators on the distribution system are typically not included. Total net generation should equal the sum of net generation by energy source.
# 
#  - Total interchange: Net metered tie line flow from one BA to another directly
# connected BA. Typically, demand equals net generation minus total interchange.
# 
# Next it is important to understand the differences between imputed and adjusted data values:
# 
#  - Adjusted values: To incorporate commercial arrangements, such as dynamic scheduling arrangements and interchanges on pseudo ties, BAs normally adjust their metered physical flow values to produce this alternative view of grid operations.
#   - Imputed values: With imputed values, BAs occasionally report anomalous data values such as blank, zero, negative, and unreasonably high or low values. We perform a basic imputation process for several data elements. The process for imputing is slightly different for Demand, Net Generation, and Total Interchange, but usually, the EIA imputes values if the value is missing or reported as negative, zero, or at least 1.5 times greater than the maximum of past total demand values reported by that BA.
# 
# Third, there are three sources of bias in this data. These biases include:
# 
# 1. There are several generation BAs that do not directly serve retail customers. Therefore
# they do not report demand or demand forecasts.
# 2. City of Homestead (HST) has a small number of local generators that do not always produce
# electricity, so it will not always have net generation to report.
# 3. Dynamic Scheduling and Pseudo ties can introduce some level of bias onto demand, demand
# forecast, net generation and interchange.
# 
# Finally, it is important to understand the sources of energy. The sources of energy include Coal, Natural Gas, Nuclear, All Petroleum Products, Hydropower Excluding Pumped Storage, Pumped Storage, Solar without Integrated Battery Storage, Solar with Integrated Battery Storage, Wind without Integrated Battery Storage, Wind with Integrated Battery Storage, Battery Storage, Other Energy Storage, Unknown Energy Storage, Geothermal, Other Fuel Sources, Unknown Fuel Sources
#%% md
# ## Understanding Demand by Balancing Authority
# 
# We have three demand values that matter to us. We have just demand, adjusted demand, and imputed demand. We can create a new DataFrame comparing the three demands to see how they interact with each other. For most of them, we can see that $Demand_{Adjusted}=Demand+Demand_{Imputed}$. We can do this by Adding up the Demand and Imputed Demand which should equal the Adjusted Demand. We can also add another column that sets this all to zero by taking the adjusted demand and subtracting it from the sum of the demand and imputed demand.
# 
# ### Conclusion
# From this exploration, we can conclude that using the Adjusted Demand is the most useful metric to use for demand.
#%%
demand_by_ba = df.groupby(["Balancing Authority", "Region"])["Demand (MW)"].sum()
adjusted_demand_by_ba = df.groupby(["Balancing Authority", "Region"])["Demand (MW) (Adjusted)"].sum()
imputed_demand_by_ba = df.groupby(["Balancing Authority", "Region"])["Demand (MW) (Imputed)"].sum()

demand_df = pd.concat([demand_by_ba, adjusted_demand_by_ba, imputed_demand_by_ba], axis=1)

demand_df["Demand + Imputed"] = demand_df["Demand (MW)"] + demand_df["Demand (MW) (Imputed)"]

demand_df["Check Difference"] = demand_df["Demand (MW) (Adjusted)"] - (
        demand_df["Demand (MW)"] + demand_df["Demand (MW) (Imputed)"])

demand_df = demand_df.reset_index()

demand_df.to_csv("demand_comparison.csv", index=False)
#%% md
# ## Understanding Generation by Balancing Authority
# 
# We can run nearly identical code as above to understand generation and look for discrepancies. We can see that, again, for most of the balancing authorities, we have $Generation_{Adjusted}=Generation+Generation_{Imputed}$ once again. Some of them are inaccurate. Next, we'll see which ones are inaccurate in both generation and demand, just in generation, and just in demand.
# 
# ### Conclusion
# Again, we can see that adjusted generation is the most useful metric to us here.
#%%
generation_by_ba = df.groupby(["Balancing Authority", "Region"])["Net Generation (MW)"].sum()
adjusted_generation_by_ba = df.groupby(["Balancing Authority", "Region"])["Net Generation (MW) (Adjusted)"].sum()
imputed_generation_by_ba = df.groupby(["Balancing Authority", "Region"])["Net Generation (MW) (Imputed)"].sum()

generation_df = pd.concat([generation_by_ba, adjusted_generation_by_ba, imputed_generation_by_ba], axis=1)

generation_df["Generation + Imputed"] = generation_df["Net Generation (MW)"] + generation_df[
    "Net Generation (MW) (Imputed)"]

generation_df["Check Difference"] = generation_df["Net Generation (MW) (Adjusted)"] - (
        generation_df["Net Generation (MW)"] + generation_df["Net Generation (MW) (Imputed)"])

generation_df = generation_df.reset_index()

generation_df.to_csv("generation_comparison.csv", index=False)
#%% md
# ## Understanding Inaccuracies
# 
# We will now locate balancing authorities where the check difference is non zero. We can then turn it into a set and find the intersections and differences. This will tell us which balancing authorities have inaccuracies and whether it is just in demand, generation, or both.
# 
# ### Conclusion
# One interesting thing we can see from this, is that in a lot of the inaccurate imputations, the region is NW (Northwest). One hypothesis is that balancing authorities in the Northwest may use different types of power generation than other regions. We can now look into seeing which type of power generation is used most per region.
#%%
def show_with_region(df, ba_list):
    return df[df["Balancing Authority"].isin(ba_list)][["Balancing Authority", "Region"]]


demand_discrep = demand_df.loc[demand_df["Check Difference"] != 0, "Balancing Authority"]
gen_discrep = generation_df.loc[generation_df["Check Difference"] != 0, "Balancing Authority"]

demand_discrep = set(demand_discrep)
gen_discrep = set(gen_discrep)

both = demand_discrep.intersection(gen_discrep)
only_demand = demand_discrep.difference(gen_discrep)
only_gen = gen_discrep.difference(demand_discrep)

print("Discrepancies in both demand and generation:")
print(show_with_region(demand_df, both))

print("")
print("Discrepancies only in demand:")
print(show_with_region(demand_df, only_demand))

print("")
print("Discrepancies only in generation:")
print(show_with_region(generation_df, only_gen))
#%% md
# ## Understanding Sources of Power Generation
# 
# This graph will plot out how much power is generated in each region and what type of power is used in said region. This graph definitely looks overwhelming, but not to worry. You can focus on the orange section on the Northwest region. Notice that the amount of hydropower for every other region is significantly lower.
#%%
adjusted_cols = [col for col in df.columns if "(Adjusted)" in col and "Net Generation (MW) from" in col]
df[adjusted_cols] = df[adjusted_cols].fillna(0)
gen_by_region = df.groupby("Region")[adjusted_cols].sum()
custom_colors = [
    "#1f77b4",
    "#9467bd",
    "#2ca02c",
    "#d62728",
    "#ff7f0e",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#ff9896",
    "#c5b0d5",
    "#c49c94",
    "#f7b6d2",
    "#c7c7c7",
    "#dbdb8d",
    "#9edae5",
]

ax = gen_by_region.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 7),
    color=custom_colors
)

plt.title("Adjusted Net Generation by Fuel Source per Region")
plt.ylabel("Net Generation (MW)")
plt.xlabel("Region")
plt.legend(
    title="Fuel Source",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)
plt.tight_layout()
plt.show()
#%% md
# ## Demand vs. Generation
# 
# We'll now take a look at demand for March 2025. Why March 2025? Because my birthday is in March. Allegedly. One of the interesting things we're doing here is scaling it to the 99th percentile. If you don't, then you see a pretty egregious outlier. There's even one outlier that has -50,000MW of generation. This does help us show that it does appear to be a pretty linear relationship. As demand goes up, so does generation. While this may seem fairly obvious, any point of interest where demand is too high would be interesting. Showing us the 99th percentile shows us that there are actually not that many outliers.
#%%
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharex=False, sharey=False)

# --- Left: full scale ---
axes[0].scatter(df["Demand (MW)"], df["Net Generation (MW)"], alpha=0.5)
max_val = max(df["Demand (MW)"].max(), df["Net Generation (MW)"].max())
axes[0].plot([0, max_val], [0, max_val], 'r--', label="1:1 Line")
axes[0].set_title("Full Scale")
axes[0].set_xlabel("Actual Demand (MW)")
axes[0].set_ylabel("Net Generation (MW)")
axes[0].legend()

# --- Right: zoomed to 99th percentile ---
axes[1].scatter(df["Demand (MW)"], df["Net Generation (MW)"], alpha=0.5)
axes[1].plot([0, max_val], [0, max_val], 'r--', label="1:1 Line")
xlim = df["Demand (MW)"].quantile(0.99)
ylim = df["Net Generation (MW)"].quantile(0.99)
axes[1].set_xlim(0, xlim)
axes[1].set_ylim(0, ylim)
axes[1].set_title("Zoomed to 99th Percentile")
axes[1].set_xlabel("Actual Demand (MW)")
axes[1].set_ylabel("Net Generation (MW)")
axes[1].legend()

plt.suptitle(" NW Region: Demand vs. Net Generation (March 2025)", y=1.02)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

#%% md
# ## Demand vs. Generation
# 
# In the graph below, we can see the demand and generation are kept quite closely in sync. We do wee a large spike in the data, and some dips at the beginning and end. The dips at the beginning and end can likely be attributed to the data starting and ending. The spike looks quite interesting. It looks like it was at the end of December.
#%%
daily = df.groupby(df["UTC Time at End of Hour"].dt.date)[["Demand (MW)", "Net Generation (MW)"]].sum()

plt.figure(figsize=(12, 6))
plt.plot(daily.index, daily["Demand (MW)"], color="blue", label="Actual Demand (MW)")
plt.plot(daily.index, daily["Net Generation (MW)"], color="red", label="Net Generation (MW)", linestyle='--')

plt.title("NW Region: Daily Demand vs Net Generation (July 2024 - July 2025)")
plt.xlabel("Date")
plt.ylabel("Total MW (Daily Sum)")
plt.legend()
plt.tight_layout()
plt.show()
#%% md
# ## Plotting Time Series Decomposition
# 
# Since this is time series data, we can plot out the residuals to see the trend, seasonality, and residuals. We can see that the trend varies depending on the region. This makes sense. Some regions have a very harsh summer and demand more air conditioning. Some regions have colder winters and demand more heat, but may have nicer summers and not need as much air conditioning. We can also see that there are 12 "peaks" in our seasonality. This aligns with our dataset being 12 months. We can assume there likely is a peak day of the month. However, it's unclear if each peak day of the month has any usefulness to us or whether it's random.
#%%
from statsmodels.tsa.seasonal import seasonal_decompose

regions = df["Region"].unique()

for region in regions:
    adjusted_mw_perday_oneregion = df[df["Region"] == region].set_index("UTC Time at End of Hour")[
        "Net Generation (MW) (Adjusted)"].resample("D").sum()

    result = seasonal_decompose(adjusted_mw_perday_oneregion, model="additive", period=30)

    result.plot()
    plt.suptitle(f"Seasonal Decomposition of Adjusted Net Generation ({region})", y=1.02)
    plt.show()
#%% md
# ## Finding the spikes
# 
# We can see that after plotting our data, there is actually no pattern to the spikes that we could find. Initially, we thought that maybe it was because there was an extra surge on the fist or last day of the month. Since this is grouped by region and not balancing authority, it's hard to pinpoint it to one specific balancing authority and whether they potentially have an artificial influx due to data or business processing.
#%%
adjusted_mw_perday_allregions = df.set_index("UTC Time at End of Hour").groupby("Region")[
    "Net Generation (MW) (Adjusted)"].resample(
    "D").sum().reset_index()

# Add a year month column, we need just the year and month to properly group by and find the max
adjusted_mw_perday_allregions["YearMonth"] = adjusted_mw_perday_allregions["UTC Time at End of Hour"].dt.to_period("M")

# Now we can find the highest day per month and find adjusted net generation
max_days = adjusted_mw_perday_allregions.loc[adjusted_mw_perday_allregions.groupby(["Region", "YearMonth"])[
    "Net Generation (MW) (Adjusted)"].idxmax()].sort_values(["Region", "UTC Time at End of Hour"])

regions = adjusted_mw_perday_allregions["Region"].unique()

for region in regions:
    subset = adjusted_mw_perday_allregions[adjusted_mw_perday_allregions["Region"] == region]
    peaks = max_days[max_days["Region"] == region]

    # Plot the actual generation in a line
    plt.figure(figsize=(12, 6))
    plt.plot(
        subset["UTC Time at End of Hour"],
        subset["Net Generation (MW) (Adjusted)"],
        label="Daily Total"
    )

    # Scatter plot the peak day (it's just one dot per month)
    plt.scatter(
        peaks["UTC Time at End of Hour"],
        peaks["Net Generation (MW) (Adjusted)"],
        color="red", s=80, label="Monthly Peak"
    )

    # We want to see the specific day of the month for each month
    for _, row in peaks.iterrows():
        day_label = row["UTC Time at End of Hour"].day
        month_label = row["UTC Time at End of Hour"].month
        label = f"{month_label}/{day_label}"
        plt.text(
            row["UTC Time at End of Hour"],
            row["Net Generation (MW) (Adjusted)"],
            str(label),
            color="black", fontsize=9, ha="center", va="bottom"
        )

    plt.title(f"Daily Adjusted Net Generation with Monthly Peaks ({region})")
    plt.ylabel("Net Generation (MW)")
    plt.xlabel("Date (UTC)")
    plt.legend()
    plt.tight_layout()
    plt.show()
#%% md
# ## Transitioning to AI Datacenters
# 
# Now that we have a good idea of what our power grid looks like, we can focus on the more interesting part of our project: datacenters. Why do the exercises above? Exploring the data is quite important and familiarity helps when you want to dive deeper into it. Understanding how the power grid works in general helps us drill down on datacenters more effectively. The most important thing we learned is that supply and demand must be kept very closely together. Any shortage is bad. We also know that the power grid is interconnected. Balancing authorities can transfer power from themselves to other balancing authorities in need. Translating this information to datacenters will not be an easy task.
# 
# Firstly, we have a list of datacenters by state. However, each BA does not "belong" to a state. The good news is that we're not interested in all 50 states for the scope of this project. We're mostly interested in Virginia, California, and Texas. They by far have the most amount of datacenters. What we can do is figure out the interchange between BA's. If a BA from another state is exporting a lot to the BA that handles Virginia, we can assume it is under strain. Doing it by region alone is not enough. This can be proven quite easily. Take a look at the datacenters in Virginia and West Virginia. WV has three whereas VA has the most. They technically are under the same BA. It's not enough to just look at the region nor state. BA is the only way we can get granular enough.
# 
# Also, we must understand that generation and demand itself does not tell the full story. It is important that both must be kept in sync. Now, we're taking a deeper look into *how* this happens between balancing authorities.
# 
# ### Generating an API Key
# 
# To run the code below, you must generate an API key [here](https://www.eia.gov/opendata/register.php). You then will need to create a `.env` file and put your API key in as follows
# ```
# EIA_API_KEY=<your api key>
# ```
#%%
import requests
import os
from dotenv import load_dotenv

load_dotenv()
eia_api_key = os.getenv("EIA_API_KEY")

url = "https://api.eia.gov/v2/electricity/rto/interchange-data/data/"


def fetch_interchange_to_csv(start="2025-01-01T00", end="2025-07-31T00", output_file="interchange_data.csv",
                             max_rows=None):
    offset = 0
    length = 5000
    total_fetched = 0
    header_written = False

    # We can't use Pandas. It will run out of memory
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        print("Now calling the API. This will take a few minutes, please be patient.")
        while True:
            params = {
                "frequency": "hourly",
                "data[0]": "value",
                "start": start,
                "end": end,
                "sort[0][column]": "period",
                "sort[0][direction]": "desc",
                "offset": offset,
                "length": length,
                "api_key": eia_api_key,
            }

            response = requests.get(url, params=params)
            data = response.json()

            if "response" not in data:
                print("Bad response", data)
                break

            rows = data["response"]["data"]
            if not rows:
                print("Data successfully fetched!")
                break

            interchange_ba = pd.json_normalize(rows)
            interchange_ba.rename(
                columns={
                    "fromba": "FromBA",
                    "fromba-name": "FromBAName",
                    "toba": "ToBA",
                    "toba-name": "ToBAName",
                    "value": "MWh",
                },
                inplace=True,
            )

            if "period" in interchange_ba.columns:
                interchange_ba["period"] = pd.to_datetime(interchange_ba["period"], errors="coerce")
            if "MWh" in interchange_ba.columns:
                interchange_ba["MWh"] = pd.to_numeric(interchange_ba["MWh"], errors="coerce")

            interchange_ba.to_csv(f, index=False, header=not header_written)
            header_written = True

            total_fetched += len(interchange_ba)
            offset += length

            if max_rows and total_fetched >= max_rows:
                break

    print(f"Saved {total_fetched} rows to {output_file}")


fetch_interchange_to_csv(start="2025-08-01T00", end="2025-08-31T00", output_file="interchange_aug_2025.csv",
                         max_rows=None)
#%% md
# ## Feature Engineering
# 
# Now that we have the CSV of the BA transactions, we can add the region per each for better visibility. We also see that some of them are negative megawatts. This discrepancy is documented by the EIA themselves. As per the EIA:
# > **External interchange reporting consistency**: BAs are physically connected to their neighboring BAs by one or more transmission lines. These lines have meters that measure the flow of electricity between BAs. Interchange reported by BA 1 with BA 2 should be the exact reverse of the interchange reported by BA 2 with BA 1. For example, if BA 1 reports +100 MW interchange with BA 2, BA 2 should report -100 MW with BA 1.
#  Correcting incorrect interchange values for one or both of the BAs in a BA pair is particularly challenging because it is difficult to identify misreported data and the reason for mismatches. We have found that a number of BAs are not reporting using a data source with checked-out values. In addition, some BAs are not appropriately accounting for pseudo-ties or dynamic schedules in their reporting.
# 
# In short, a positive or negative MWh actually *does* carry meaning. It tells us direction and if it's flipped or not. If the MWh is negative, it means the From and To are flipped. We added a new column to show that and make it crystal clear. However, we have not flipped any of the negatives to positives or vice versa.
# 
# We did feature engineer the region. However, sometimes the BA is just "CAL", for example. This is a region in itself, not a BA. We want to drop these since it's just a pseudo grouping. This dataset combines the generic "CAL" regions *and* the BA data. By dropping BAs that are equal to a region, we get solely BA to BA data.
#%%
ba_lookup_path = "EIA930_Reference_Tables.xlsx"
df_lookup = pd.read_excel(ba_lookup_path, engine="openpyxl")
df_lookup = df_lookup[["BA Code", "Region/Country Code", "Region/Country Name"]].rename(
    columns={
        "BA Code": "BA",
        "Region/Country Code": "RegionCode",
        "Region/Country Name": "RegionName"
    }
)

interchange_path = "interchange_aug_2025.csv"
df_interchange = pd.read_csv(interchange_path, parse_dates=["period"])

df_interchange = df_interchange.merge(df_lookup, left_on="FromBA", right_on="BA", how="left").rename(
    columns={"RegionCode": "FromRegionCode", "RegionName": "FromRegionName"}).drop(columns=["BA"])

df_interchange = df_interchange.merge(df_lookup, left_on="ToBA", right_on="BA", how="left").rename(
    columns={"RegionCode": "ToRegionCode", "RegionName": "ToRegionName"}).drop(columns=["BA"])

pseudo_bas = [
    "CAL", "MIDA", "MIDW", "CENT", "NE", "NW", "NY", "SE", "SW",
    "TEN", "TEX", "US48", "CAN", "MEX"
]

df_interchange = df_interchange[
    ~df_interchange["FromBA"].isin(pseudo_bas) &
    ~df_interchange["ToBA"].isin(pseudo_bas)
    ].copy()

# This gets us the "true" direction
df_interchange["Direction"] = df_interchange["MWh"].apply(lambda x: "From -> To" if x > 0 else "To -> From")

df_interchange.to_csv("interchange_aug_2025_with_regions.csv", index=False)
print("Done with feature engineering. Added region and imputed regions to new file.")

#%%
df_normalized = df_interchange.copy()

mask_negative = df_normalized["MWh"] < 0
df_normalized.loc[mask_negative, ["FromBA", "ToBA"]] = df_normalized.loc[mask_negative, ["ToBA", "FromBA"]].values
df_normalized.loc[mask_negative, ["FromBAName", "ToBAName"]] = df_normalized.loc[
    mask_negative, ["ToBAName", "FromBAName"]].values
df_normalized.loc[mask_negative, ["FromRegionCode", "ToRegionCode"]] = df_normalized.loc[
    mask_negative, ["ToRegionCode", "FromRegionCode"]].values
df_normalized.loc[mask_negative, ["FromRegionName", "ToRegionName"]] = df_normalized.loc[
    mask_negative, ["ToRegionName", "FromRegionName"]].values
df_normalized.loc[mask_negative, "MWh"] = -df_normalized.loc[mask_negative, "MWh"]

exports_by_ba = df_normalized.groupby(["FromBA", "FromBAName", "FromRegionCode", "FromRegionName"])[
    "MWh"].sum().reset_index().rename(columns={"MWh": "TotalExportsMWh"}).sort_values("TotalExportsMWh",
                                                                                      ascending=False)

imports_by_ba = df_normalized.groupby(["ToBA", "ToBAName", "ToRegionCode", "ToRegionName"])[
    "MWh"].sum().reset_index().rename(columns={"MWh": "TotalImportsMWh"}).sort_values("TotalImportsMWh",
                                                                                      ascending=False)

top_flows = df_normalized.groupby(["FromBA", "FromBAName", "ToBA", "ToBAName"])["MWh"].sum().reset_index().sort_values(
    "MWh", ascending=False)

#exports_by_ba.to_csv("ba_exports_summary.csv", index=False)
#imports_by_ba.to_csv("ba_imports_summary.csv", index=False)
top_flows.to_csv("ba_top_flows.csv", index=False)
#%%
print("Top 10 BA to BA Flows:")
print(top_flows.head(10))
#%% md
# ## Conclusion
# 
# The analysis shows that the two largest balancing authority (BA) flows in the U.S. are into the Midcontinent Independent System Operator (MISO) and the Arizona Public Service Company (AZPS).
# 
# * AZPS recorded 6,179,925 MWh of transfers
# * MISO received 5,890,099 MWh of transfers
# 
# These volumes are significantly larger than other balancing authorities. For comparison, the New York Independent System Operator (NYISO) recorded 3,485,272 MWh. This is logical given that New York has the second-highest concentration of data centers in the U.S.
# 
# The two leading flows, however, highlight very different dynamics:
# 
# 1. Arizona (AZPS) Flows: A Western Transit Hub
# 
#    * Arizona stands out because of geography rather than generation or consumption.
#    * AZPS and neighboring utilities like SRP act as transit hubs in the Western Interconnection. Power from the Pacific Northwest and the desert Southwest often passes through Arizona en route to California’s massive load centers.
#    * This makes Arizona’s transfer volumes appear exceptionally high, even though the state itself does not produce or consume as much as PJM or MISO.
# 
# 2. PJM–MISO Flows: High Volume, Strong Interconnection
# 
#    * Virginia, within PJM territory, hosts the largest concentration of U.S. data centers, supported by a robust nuclear generation fleet.
#    * This allows PJM to export power to neighboring regions.
#    * Crucially, PJM and MISO share an extensive AC interconnection along their border, making them natural high-volume trading partners. Power can flow freely across this seam, which is one of the busiest in the U.S. grid.
# 
# 3. PJM–NYISO Flows: High Demand, but Constrained Capacity
# 
#    * NYISO's high demand stems from its large data center footprint.
#    * But PJM's ability to send energy to NYISO is limited. Transfers are bottlenecked by a handful of High Voltage Direct Current (HVDC) ties, such as Neptune, Hudson, and Cross-Sound, along with constrained AC lines in Upstate New York.
#    * This means that even if PJM has ample supply, the physical infrastructure restricts how much can actually be delivered to NYISO.
# 
# #### Key Takeaway
# 
# The largest BA flows underscore both infrastructure realities and regional demand drivers.
# 
# * MISO’s flows are large because it is tightly interconnected with PJM, forming a seamless and active corridor of power exchange.
# * Arizona’s flows are large because of its geographic role as a highway, moving power across the West to serve California.
# * By contrast, NYISO's needs are substantial but capped by interconnection limits, showing how transmission infrastructure is as critical as generation in shaping actual flows.
# 
# #### So how do we find these data centers?
# 
# It is like finding a needle in a haystack, but with this exploratory data analysis and a couple other pieces of information, we know a couple of things; First there are a ton of discrepancies with the NE because of the hydropower generation. But we can identify suspect BA's with unusually high flows. After comparing top flows to known data center hotspots, if a BA has very high transfers but isn't widely recognized as a major load center, it could indicate:
# 
# 1. pass-through transit role (like Arizona)
# 2. unreported/undeclared data centers
# 
# TVA (Tennessee Valley Authority) shows up with 2.8 million MWh from MISO. TVA is less commonly discussed in public data center maps than, say, Virginia or Phoenix, but it has low-cost nuclear and hydro which could attract "quiet" hyperscale builds.
# 
# ## Ultimately, the (TVA) would be the result of this heuristic based on our analysis.
#%% md
# ## Next steps
# The next step is to figure out why this is the case and to try and pinpoint this down even more. The data that we used for this was just from the month of August; from here we can concatenate the data for the rest of the months and conduct time series analysis for BA to BA. Understanding the BA's that imported the most power over time and when they did it would be incredibly important. This is because they will most likely correlate with the time that these data centers started being built. Essentially our goal is to improve this heuristic as much as possible.
#%% md
# ### AI Disclosure
# 
# ChatGPT was used to help generate the Matplotlib graph showcasing the "Adjusted Net Generation by Fuel Source per Region". Since there were a lot of columns, ChatGPT was used to assist in attempting to visualize the large amount of columns in a way that made sense.
# 
# ChatGPT was also used to assist in revising an initial attempt to download data from the EIA API. I ran into issues running out of memory and used ChatGPT to help rethink how such large amounts of data are downloaded and processed to disk rather than to memory.
# 
# We also used ChatGPT to help with some minor clarifications with syntax relating to Pandas.
# 
# We also used ChatGPT to help come up with insights. It helped understand network connections and helped with the needle in the haystack problem of using the data to create a valuable heuristic.