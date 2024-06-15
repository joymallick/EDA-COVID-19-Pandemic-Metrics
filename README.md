# Cornavirus (COVID-19) Cases EDA

## Project Description

The project aims at implementing an exploratory data analysis (EDA) workflow based on the dataset [Coronavirus (COVID-19) Cases](https://ourworldindata.org/covid-cases). <br>
The analysis focuses on the following five research questions:

1. In which continent were the highest number of cases and deaths recorded?
2. Has the implementation of hand washing facilities helped to reduce the number of total cases?
3. Restricting to Germany, how is the number of deaths related to number of people vaccinated?
4. Are the total number of deaths and life expectancy correlated?
5. How does the population density affect the total number of cases (country level)?

## Component analysis

| Abstract Workflow Node                                  | Input(s)     | Output(s)                 | Implementation     |
| ------------------------------------------------------- | ------------ | ------------------------- | ------------------ |
| Load data and filter columns                            | csv filename | filtered csv file         | CLI tool (csvkit)  |
| Data processing                                         | csv file     | csv file as dataframe     | own implementation |
| Outcomes utils                                          | csv file     | outcomes for each RQ      | own implementation |
| Deaths trend by continent (RQ1)                         | csv file     | plot figure and .txt file | own implementation |
| Hand washing facilities and tot cases correlation (RQ2) | csv file     | plot figure and .txt file | own implementation |
| Deaths and vaccinations trend(RQ3)                      | csv file     | plot figure and .txt file | own implementation |
| Deaths and life expectancy correlation(RQ4)             | csv file     | plot figure and .txt file | own implementation |
| Population density and tot cases correlation(RQ5)       | csv file     | plot figure and .txt file | own implementation |

## Usage

To use this project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have all required dependencies installed (you can find these in the `requirements.txt` file).
3. Run the analysis scripts provided for each research question.
4. Generated outputs such as plots and text files will be saved in the `results` directory.
