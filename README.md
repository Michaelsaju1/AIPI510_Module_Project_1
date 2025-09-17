# AIPI510_Module_Project_1
This will be Project 1 for AIPI 510.
Second Draft:
Context: With the advancement of technology becoming so prevalent in modern times, it is crucial that 

Gap Problem: What are the weakest points in our power infrastructure? 

Literature Review:

Methodology:

Solution:

Analyis:

Conclusion:

Areas for Future Exploration:

How much are we short by right now and how short will we be in the next five to ten years?





Rough Draft Phase:
Project:
What is the biggest difference between Forecasted and Actual demand and what regions are those underdemand areas? Why are they like that?

Steps:
1. Take Data from 2015 by subregion and put it all together.
2. Figure out what the data means
3. Conduct Exporatory Analysis - Answer the following questions:
● Data Context
  ○ What is the source of the data, and how was it collected?
The source of the data is the U.S. Energy Information Administration.
  ○ Are there any known biases or limitations in the data?
######################LOOK OVER THIS
There are no known biases or limtations. However there is a disclaimer: The information submitted by reporting entities is preliminary data and is made available "as-is" by EIA. Neither EIA nor reporting entities are responsible for reliance on the data for any specific use. Essentially there
  ○ How does the data relate to the problem or question you are trying to solve?
● Data Sampling
  ○ Is the dataset representative of the population of interest?
  ○ Is there a need to split the data into train and test sets for modeling purposes?
  ○ Are there any specific subsets or segments of the data that require separate analysis?
● Data Structure
  ○ What are the dimensions of the dataset (number of rows and columns)?
  ○ What are the data types of the variables (numerical, categorical, text, etc.)?
  ○ Are there any missing values, and if so, how are they represented?
● Descriptive Statistics
  ○ What are the central tendency measures (mean, median, mode) for numerical variables?
  ○ What are the measures of dispersion (range, variance, standard deviation) for numerical
    variables?
  ○ What is the distribution of the variables (normal, skewed, etc.)?
● Data Quality
  ○ Are there any duplicated rows or inconsistent values?
  ○ Are there any outliers or extreme values that need attention?
  ○ Do the values make sense based on the context and domain knowledge?
● Variable Relationships
  ○ Is there any correlation between pairs of numerical variables?
  ○ Are there any noticeable patterns or trends in the data?
  ○ How are categorical variables related to numerical variables?
● Data Visualization
  ○ How can the variables be visualized effectively (histograms, scatterplots, box plots, etc.)?
  ○ Do the visualizations reveal any interesting patterns or insights?
  ○ Are there any subgroups or clusters that can be identified visually?
● Feature Engineering
  ○ Are there any new features that can be derived from the existing ones?
  ○ Is there a need to transform or scale any variables?
  ○ Are there any variables that can be combined or decomposed?****
5. Data Integration
  ○ Integrating multiple sources of data together (ensure consistent formatting)
6. Data Cleaning
   a. So take out unneccessary columns (only keep UTC Time at the end of hour at the end of the hour for times because we can use this to tell us everything else).
   b. Take out empty columns or columns with NaN values. Validate this with Univariate solution (Pearson's/Spearman's Correlation)
   c. Find where the biggest differences are and make a new column
  ○ Handling Missing Values
  ○ Removing Duplicates
  ○ Handling Outliers
7. Data Transformation
  ○ Normalization/standardization
  ○ Encoding categorical variables
  ○ Handling skewed data via log transformation
8. Handling imbalanced data
9. Feature Engineering
  ○ Creating new features
  ○ Creating interaction features
10. Data Augmentation
  ○ For images, text
11. Dimensionality Reduction
12. Feature Selection
  ○ Correlation analysis
  ○ Recursive feature elimination
  ○ Univariate Selection
13. Feature Engineering
  ○ Creating new features
  ○ Creating interaction features
14. Data Augmentation
  ○ For images, text
15. Dimensionality Reduction
16. Feature Selection
  ○ Correlation analysis
  ○ Recursive feature elimination
  ○ Univariate Selection
17. Data Partitioning
○ Train/test splits
○ Cross validation
18. Preventing Data Leakage
19. Data Versioning & Reproducibility

Submission Deliverables:
1. Public Communication Deliverable (submitted as link)
   Must include:
   A clear and engaging title
   An explanation of why this story matters and who it's for (your audience)
   Key findings supported by visualizations and examples
   Discussion of data limitations, bias, and ethical implications (in accessible language)
   A compelling narrative arc—what surprised you? What should we take away?
2. GitHub Repository (submitted as link)
   Must include:
   All code used for preprocessing, EDA, and feature engineering (scripts, not just notebooks)
   A README with:
      Overview of your project
      Dataset description and citation
      Step-by-step instructions to reproduce your analysis
      Use of branches and pull requests
   Each group member must make at least one PR
      Use best practices for reviews and commits
   Raw and cleaned data (or, if restricted, a clear description of how to access/generate it)
5. Presentation (8 minutes max) (presented in class on Sep 30th)
  Must inlcude:
      Your audience and why this story matters
      Your dataset and topic of interest
      Key trends and visualizations uncovered during EDA
      Any engineered features that shaped your analysis
      The story your data tells and its ethical implications
      Final takeaways

Brainstorming Phase:
Scope
What: Electricty Demand in MegaWatt Hours
Where: This will be in U.S. Lower 48 (the ones on the traditional map)
When: from 2015 - now

1. Power grid data
   This would be a three phase process:
   Phase 1: We would be identifying where the week points are currently and in the future in our energy grid and by how much. We would also be predicting where the week points will be. It will account for the injestion of electric cars intop the power grid and flying supersonic and these new data centers.
   Phase 2: Then we would predict how much energy we should input into the grid with nuclear power and whether that would be enough with the introduction of electric cars and our projection for the energy we should need.(AIPI 510)

Resources:
1. Data to find out what where the week points currently are
https://www.eia.gov/electricity/gridmonitor/dashboard/electric_overview/US48/US48

Questions:
1. Are there toehr sources opf data that we coudl also use to help with this?
Yes we can use carbon emmission data to als help 

Things to know

Top weaknesses in infrastructue
1. Aging infrastructure
2. Cyber Vulnberabilities
3. Extreme weatehr and climate exposure
4. Renewable integration challenges

How it works:

<img width="865" height="395" alt="image" src="https://github.com/user-attachments/assets/9aeb554b-fd62-4125-b839-5f72bf89d89d" />

Solutions right now?
Decentralized power like Decentralized Energy Resources
Weaknesses here ripple into national security, economic resilience, and climate adaptation

   Then we would go back and take the perspective of General Matter on Uranium Enrichment (Scott Nolan) and make recommendations on where exactly to put theses power plants. That decision would be optimizing where it wopuld have the biggest impact on the energy grid, allow for the most growth based on state law and minimze the enemy's ability to havce a significant impact on out energy grid. (AIPI 530)

   
5. Solving the debt problem
6. Sex trafficking

Option 2: Measuring power if we really want to go all out
In this competition with the U.S. and China, we need to optimize to stay the world power right now and ensure that we will continue to be. How do we do this? It starts with understanding where we are at now. Currently The NAtional Intelligence COunciul uses a blend of GDP< R&D,spoending, population and military capability to measure power. But they're so off and we can do such a better job than that. Our solution? A Multivariate Integrated Model combining Class Realsim Gross INdicators (GDP, Military Spending, population, land area, industrial output), Beckley's Framework with Net Resource Models to subtract liabilities (poverties, internal instability). It will continue to add.\
