# Exploratory Data Analysis of COVID-19 Pandemic Metrics

## Project Description

### Project Objective:
The primary objective of this project is to conduct an in-depth exploratory data analysis of the COVID-19 pandemic metrics using the data available from the Our World in Data website. The goal is to uncover insights and relationships that can help better understand the progression and impact of the pandemic across different countries.

### Data Source:
The project will utilize the COVID-19 dataset available on the "Our World in Data" website (https://ourworldindata.org/coronavirus). This comprehensive dataset includes various metrics such as confirmed cases, deaths, testing, hospitalizations, vaccinations, policy responses, and more, for 207 countries over the course of the pandemic.

### Workflow 1: Exploring Correlations Between Categorical Variables and COVID-19 Metrics

This workflow involves using the Mann-Whitney U test to identify correlations between categorical variables and COVID-19 metrics like cases or deaths.

1. Process the data to create a dataset with relevant categorical variables (e.g., country income level, population density, etc.) and COVID-19 metrics.
2. Apply the Mann-Whitney U test to each categorical variable, comparing the COVID-19 metric values between the different categories.
3. For categorical variables with p-values below 0.05, create box plots to visualize the difference in the COVID-19 metric between the categories.
4. For categorical variables with p-values above 0.05, create line plots to show the trend in the COVID-19 metric over time, broken down by different categories.
5. Analyze the results to identify any significant relationships between the categorical variables and the COVID-19 metrics.

## Component analysis

| Abstract Workflow Node                  | Input(s)     | Output(s)                 | Implementation     |
|-----------------------------------------|--------------|---------------------------|--------------------|
| Load data and filter columns            | csv filename | filtered csv file         | CLI tool (csvkit)  |
| General data processing                 | csv file     | csv file as dataframe     | own implementation |
| Specific data processing for workflow 1 | csv file     | csv file as dataframe     | own implementation |
| Specific data processing for Workflow 2 | csv file     | csv file as dataframe     | own implementation |
| Specific data processing for Workflow 3 | csv file     | csv file as dataframe     | own implementation |
| Outcomes utils                          | csv file     | outcomes for each RQ      | own implementation |
| Correlation test                        | csv file     | plot figure and .txt file | own implementation |
| Mann-Whitney U test                     | csv file     | .txt file                 | own implementation |
| Regression plot                         | csv file     | plot figure and .txt file | own implementation |
| Workflow 2 plot                         | csv file     | plot figure and .txt file | own implementation |
| Box plot                                | csv file     | plot figure and .txt file | own implementation |
| Line plot                               | csv file     | plot figure and .txt file | own implementation |

## Usage

To use this project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have all required dependencies installed (you can find these in the `requirements.txt` file).
3. Run the analysis scripts provided for each research question.
4. Generated outputs such as plots and text files will be saved in the `results` directory.

## Contributing

We welcome contributions from the community! For detailed guidelines on how to get involved, please refer to our [Contribution Guidelines](CONTRIBUTING.md).

### Code of Conduct

All contributors are expected to follow the project's [Code of Conduct](CONDUCT.md). Please read it carefully before participating.

### Questions and Support

If you have any questions or need assistance, please open an issue on the project's GitHub repository so we can discuss the question together.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file for details.
