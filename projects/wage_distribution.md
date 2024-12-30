## Project Overview

This project explores the income distribution of households across different income groups using [census data](https://data.census.gov/table/ACSST5Y2020.S1901?q=S1901). The primary objective is to visualize the distribution patterns and analyze how income is distributed among households in various brackets. Ridgeline charts were chosen as the visualization method to provide an intuitive and aesthetically appealing representation of density across multiple categories.

### Data Preparation

The data was sourced from the U.S. Census Bureau and contains household income estimates categorized by income brackets for different years. Key steps in preparing the data include:

- Cleaning:
    - Removed symbols such as %, ±, and commas to ensure numerical consistency.
    - Filtered out rows with missing or invalid data in the households_estimate column.
- Data Filtering:
     - Focused the analysis on the year 2010 for simplicity and clarity.
     - Removed rows with non-positive values in households_estimate.
 - Ensuring Validity:
     - Verified that each income group contained valid numeric data to avoid empty groups in the visualization.

### Methodology

The ridgeline chart was created using Python with pandas for data manipulation, and joypy for visualization. 
This project is currently in progress, and just plots the distributions over time. Future enhancements will be added. 

![Wage Distribution Ridgeline Plot](../static/images/wage_distribution_ridgeline_plot.png)

## Tools and Libraries
- **Python**
- **Pandas**

## Future Work
This analysis can be extended by:

- Comparing and measuring income distributions across multiple years to identify trends.
- Measuing spread of distributions within, and across years. 
- Expanding the visualization to include additional household categories (e.g., families, nonfamily households).

## Acknowledgments
Dataset is from US Census Bureau: https://data.census.gov/table/ACSST5Y2020.S1901?q=S1901

## Author
This project was developed by John Curran.