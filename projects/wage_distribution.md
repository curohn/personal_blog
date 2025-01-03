## Project Overview

This project explores the income distribution of households across different income groups using [census data](https://data.census.gov/table/ACSST5Y2020.S1901?q=S1901). This project was aimed at being a demonstration of an exploritory data analysis. Starting with data and a question, ending with deeper understanding into the data and what it shows. It's written like a story from the first person perspective, in order to show my methodology and thought process into the analysis. While this writeup can give you the basics, I'd highly recommend reading the whole notebook available on [github.](https://github.com/curohn/wage_distribution)

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

This project is currently in progress, and just plots the distributions over time. Future enhancements will be added. 

![Wage Distribution Ridgeline Plot](../static/images/wage_distribution_ridgeline_plot.png)
![Wage Distribution Line Chart](../static/images/wage_distribution_line_chart.png)

## Tools and Libraries
- **Python**
- **Pandas**
- **MatPlotLib**
- **Seaborn**

## Future Work
This analysis can be extended by:

- Comparing and measuring income distributions across multiple years to identify trends.
- Measuing spread of distributions within, and across years. 
- Expanding the visualization to include additional household categories (e.g., families, nonfamily households).

## Acknowledgments
Dataset is from US Census Bureau: https://data.census.gov/table/ACSST5Y2020.S1901?q=S1901

## Author
This project was developed by John Curran.