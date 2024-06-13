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
|Load data and filter columns       |csv filename    |filtered        |CLI tool (csvkit)        |
|                                   |                |csv file        |                         |
|-----------------------------------|----------------|----------------|-------------------------|
|Data processing                    |csv file        |csv file        |own implementation       |
|                                   |                |as dataframe    |(use Pandas)             |
|-----------------------------------|----------------|----------------|-------------------------|
|Compute % growth                   |growth var,     |% growth  var   |own implementation       |
|                                   |time period,    |                |                         |
|                                   |and total var   |                |                         |
|-----------------------------------|----------------|----------------|-------------------------|
|Correlation hp test and            |% growth vars   |                |own implementation       |
|linear regression model            |                |                |                         |
|-----------------------------------|----------------|----------------|-------------------------|
|Bar plot                           |var             |plot            |own implementation       |
|-----------------------------------|----------------|----------------|-------------------------|     
|Line plot                          |x and y         |plot            |own implementation       |
|-----------------------------------|----------------|----------------|-------------------------|  
|Log results                        |results of      |log to .txt file|CLI tool (>)             |
|                                   |a function      |                |                         |   
|----------------------------------_|----------------|----------------|-------------------------|
## Usage

## Contributing

## License


