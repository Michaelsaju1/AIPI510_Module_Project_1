import csv

data = """
Virginia
387
California
383
Texas
320
Illinois
160
New York
141
Florida
139
Ohio
125
New Jersey
112
Georgia
106
Arizona
103
Washington
101
Oregon
96
Colorado
68
Massachusetts
60
North Carolina
57
Pennsylvania
56
Minnesota
52
Maryland
43
Michigan
41
Utah
40
Tennessee
39
Missouri
38
Nevada
30
Indiana
28
Iowa
25
Wisconsin
22
Nebraska
18
Alabama
16
South Carolina
15
Oklahoma
15
Louisiana
14
Connecticut
14
Kentucky
13
New Mexico
13
District of Columbia...
12
Kansas
11
Hawaii
10
Delaware
9
New Hampshire
9
Wyoming
8
Idaho
7
Maine
4
Rhode Island
4
South Dakota
3
Mississippi
3
West Virginia
3
Arkansas
3
Montana
2
North Dakota
2
"""

state_to_region = {
    "California": "CAL",
    "New York": "NY",
    "Florida": "FLA",
    "Texas": "TEX",
    "Virginia": "MIDA",
    "New Jersey": "MIDA",
    "Maryland": "MIDA",
    "Delaware": "MIDA",
    "Pennsylvania": "MIDA",
    "Ohio": "MIDW",
    "Illinois": "MIDW",
    "Indiana": "MIDW",
    "Michigan": "MIDW",
    "Wisconsin": "MIDW",
    "Minnesota": "MIDW",
    "Iowa": "MIDW",
    "Missouri": "CENT",
    "Kansas": "CENT",
    "Oklahoma": "CENT",
    "Arkansas": "CENT",
    "Louisiana": "CENT",
    "Tennessee": "TEN",
    "Kentucky": "TEN",
    "Georgia": "SE",
    "Alabama": "SE",
    "Mississippi": "SE",
    "North Carolina": "CAR",
    "South Carolina": "CAR",
    "Arizona": "SW",
    "New Mexico": "SW",
    "Nevada": "SW",   # partly NW or CAL, but lumped as SW for simplicity
    "Colorado": "NW",
    "Utah": "NW",
    "Idaho": "NW",
    "Montana": "NW",
    "Wyoming": "NW",
    "Washington": "NW",
    "Oregon": "NW",
    "Massachusetts": "NE",
    "Connecticut": "NE",
    "Rhode Island": "NE",
    "Vermont": "NE",
    "New Hampshire": "NE",
    "Maine": "NE",
    "West Virginia": "MIDA",
    "North Dakota": "MIDW",
    "South Dakota": "MIDW",
    "District of Columbia": "MIDA",
    # Outliers
    "Hawaii": "US48",  # doesn’t fit EIA-930, mark separately
}

lines = data.strip().split('\n')
output_filename = 'datacenters_by_state.csv'

with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['State', 'NumberOfDataCenters', 'Region'])  # add Region column

    total_data_centers = 0

    for i in range(0, len(lines), 2):
        state = lines[i].strip()
        if "..." in state:
            state = state.replace("...", "")
        count = int(lines[i + 1].strip())
        total_data_centers += count

        region = state_to_region.get(state, "Unknown")  # fallback if state not mapped
        writer.writerow([state, count, region])

print(f"Successfully created the CSV file: {output_filename}")
print(f"The total number of data centers is: {total_data_centers}")