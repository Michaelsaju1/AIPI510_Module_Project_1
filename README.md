# Tracing the Currents: From Flows to Data Centers

## Project Overview
This project aims to develop a heuristic to find hidden data centers using power grid data. We explored how U.S. power grid flows can reveal the relationship between electricity demand, transmission constraints, and the growth of data centers — particularly those supporting AI infrastructure.


## Getting Started
You should register for an API key [here](https://www.eia.gov/opendata/register.php) so that you can run the API calls to download the EIA data.


### Prerequisites
Python 3.11+, Git

### Installation
Clone the repo. Then, create and activate a virtual environment:

```
git clone https://github.com/Michaelsaju1/AIPI510_Module_Project_1.git

cd AIPI510_Module_Project_1

python3 -m venv .venv    # Create the virtual environment
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

You can then install the dependencies in the virtual environment
```
pip install -r requirements.txt
```

### Running the file

The correct Jupyter notebook to use is `power_grid_analysis.ipynb`.
