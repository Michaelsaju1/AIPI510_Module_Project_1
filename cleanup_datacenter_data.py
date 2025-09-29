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

# Split the multi-line string into a list of individual lines.
lines = data.strip().split('\n')

# The name for the output CSV file.
output_filename = 'data_centers_by_state.csv'

# Open the file in 'write' mode. `newline=''` prevents extra blank rows.
with open(output_filename, 'w', newline='') as csvfile:
    # Create a csv writer object to handle writing rows.
    writer = csv.writer(csvfile)

    # Write the header row for the CSV file.
    writer.writerow(['State', 'NumberOfDataCenters'])

    # Initialize a variable to store the sum of data centers.
    total_data_centers = 0

    # Iterate through the lines list, taking two items at a time (a state and a number).
    # The `range` function is given a "step" of 2.
    for i in range(0, len(lines), 2):
        # The state is the current line.
        state = lines[i]

        # The number of data centers is the next line.
        count_str = lines[i+1].strip()

        # The number of data centers is the next line.
        count = lines[i + 1]

        # Clean up the "District of Columbia..." entry by removing the ellipsis.
        if "..." in state:
            state = state.replace("...", "")

        # Write the state and its corresponding count as a new row in the CSV.
        writer.writerow([state.strip(), count.strip()])
        total_data_centers += int(count_str)

print(f"Successfully created the CSV file: {output_filename}")
print(f"The total number of data centers is: {total_data_centers}")
