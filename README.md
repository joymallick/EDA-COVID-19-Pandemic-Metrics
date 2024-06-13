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
### Research question 3
|Abstract Workflow Node             |Input(s)        |Output(s)       |Implementation           |
|-----------------------------------|----------------|----------------|-------------------------|
|Load data and filter columns       |csv filename    |filtered csv file| CLI tool (csvkit)      |
|Data processing                    |csv file        |csv file as dataframe|own implementation (use Pandas)|
|Compute % growth                   |growth var, time period, and total var|% growth  var|own implementation|
|Correlation hp test and linear regression model|% growth vars|                |own implementation|
|Bar plot                           |var             |plot            |own implementation       |     
|Line plot                          |x and y         |plot            |own implementation       |  
|Log results                        |results of a function|log to .txt file|CLI tool (>)|   

## Usage

## Contributing

## License


