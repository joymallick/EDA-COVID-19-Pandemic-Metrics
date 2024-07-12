# Exploratory Data Analysis of COVID-19 Pandemic Metrics

## Project Description
The primary objective of this project is to conduct an automated exploratory data analysis of the [COVID-19 dataset](https://ourworldindata.org/coronavirus) from Our World in Data.
The analysis focuses on the following 3 main research point:
1. Understand how the number of cases and deaths differ across continents on a yearly level.
2. Explore the influence of factors such as life expectancy, GDP per capita, and population density on the number of cases and deaths. Given one of the just mentioned factors, compare the average number of cases/deaths between countries with values of the factor above the median and those with values below the median.
3. Explore the relationship between deaths, cases and vaccinations. Are deaths and vaccinations correlated? How did all these metrics evolve in time? 

For point 3., due to missing values reasons, we restrict the analysis to Europe.

For each of the above research questions we provide 3 workflows enumerated accordingly, i.e workflow 1 tackles point 1, workflow 2 point 2 and workflow 3 point 3. <br>
For detailed information on the structure refer to the corresponding `requirements.md` files in the `docs` folder, while for details on how to launch each workflow and on the produced outputs, as well as configuration options, refere to the [Usage](Usage) section below.
All the workflows are based on the workflow management system [Snakemake](https://snakemake.readthedocs.io/en/v6.15.5/getting_started/installation.html).

### Data Source:
The project will utilize the [COVID-19 dataset](https://ourworldindata.org/coronavirus) provided by "Our World in Data". This comprehensive dataset includes various metrics such as confirmed cases, deaths, testing, hospitalizations, vaccinations, policy responses, and more, for 207 countries over the course of the pandemic. 

## Usage

To use this project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have all required dependencies installed (you can find these in the `docs/requirements.txt` file).
3. Activate snakemake environment
4. Run the workflows (or just the one of interest) by running the corresponding Snakefile with the desired configuration (see below).
5. Check the results in the `results` in directory. When running all the 3 workflows, the `results` directory (with the default configuration for all the workflows) will have the following structure:

**add tree for results with all the results inside**.
### Workflow 3
Workflow 3 refers to research question 3 and it allows to configure the following parameters:
- *germany* : can be either True (= restrict the analysis to Germany) or False (= cpnsider whole Europe). The default option is False.
- *time*: choose the time period by which the data is aggregated, can be either 'month' or 'semester'. The default option is 'month'.
- *x*  and *y*: the variables for which the correlation is tested and for which the regression plot is produced (**only if** the hypothesis test results are significant). We used *x*='new_vaccinations' and *y*='deaths_over_cases'. Both *x* an *y* can be changed by choosing in the set ['new_vaccinations', 'new_deaths', 'new_cases', deaths_over_cases', 'month'], but keep in mind that other couples probably won't make a lot of sense (for example: it's obvious that new cases and new deaths are positively correlated).

All the above parameters can be edited in the file `configuration_w3.yaml`. Consistency checks are made within the workflow components, in case of invalid choices or mispelling you will receive an error. 

After choosing the desired configuration run `SnakefileWorkflow3` this way to **get all** the outputs:

`snakemake -s SnakefileWorkflow3 --cores all all --configfile configuration_w3.yaml`

The produced files will be stored in  `results\results_w3`, except for the processed datasets that will be stored in `data`.

To **delete all** the outputs run:

`snakemake -s SnakefileWorkflow3 --cores all clean --configfile configuration_w3.yaml`

To produce just a single output run the above code with the name of the output file instead of the rule name.


## Contributing

We welcome contributions from the community! For detailed guidelines on how to get involved, please refer to our [Contribution Guidelines](CONTRIBUTING.md).

### Code of Conduct

All contributors are expected to follow the project's [Code of Conduct](CONDUCT.md). Please read it carefully before participating.

### Questions and Support

If you have any questions or need assistance, please open an issue on the project's GitHub repository so we can discuss the question together. Otherwise 

### Contact information

Email addresses: [corona@uni-potsdam.de](mailto:corona@uni-potsdam.de), [nick.thomas@uni-potsdam.de](mailto:nick.thomas@uni-potsdam.de), [joy.md@uni-potsdam.de](mailto:joy.md@uni-potsdam.de), [omar.shindy@uni-potsdam.de](mailto:omar.shindy@uni-potsdam.de) .

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file for details.
