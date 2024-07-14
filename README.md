# Exploratory Data Analysis of COVID-19 Pandemic Metrics

## Project Description
The primary objective of this project is to conduct an automated exploratory data analysis of the [COVID-19 dataset](https://ourworldindata.org/coronavirus) from Our World in Data.
The analysis focuses on the following 3 main research point:
1. Explore the influence of life expectancy, median age, GDP per capita and population density on COVID-19 metrics for a given year and continent.
   Given one of the just mentioned factors, compare the average number of new cases/deaths between countries with values of the factor above
   the median (of the continent) and those with values below the median. Is there a difference?
2. Understand how the number of total cases and deaths differs across continents on a yearly level.
3. Explore the relationship between new deaths, cases and vaccinations for covid-19, given a time period level (months or semesters).
   Are deaths and vaccinations correlated? How did all these metrics evolve in time? 

For point 3., due to missing values reasons, we restrict the analysis to Europe.

For each of the above research questions we provide 3 workflows enumerated accordingly, i.e workflow 1 tackles point 1, workflow 2 point 2 and workflow 3 point 3. For each workflow, by changing the configurable parameters (see below for details), it's possible to get insights on different declinations of each research point. For example, given point 2., it's possible to choose as outcome of interest either the total number of cases or the total number of deaths per continent and to choose the year of interest starting from 2020 up to 2024. <br>
For detailed information on the components of the workflows refer to the corresponding `requirements.md` files in the `docs` folder, while for details on how to launch each workflow and on the produced outputs, as well as configuration options, refer to the Usage section below.
All the workflows are based on the workflow management system [Snakemake](https://snakemake.readthedocs.io/en/v6.15.5/getting_started/installation.html).

### Data Source:
The project will utilize the [COVID-19 dataset](https://ourworldindata.org/coronavirus) provided by "Our World in Data". This comprehensive dataset includes various metrics such as confirmed cases, deaths, testing, hospitalizations, vaccinations, policy responses, and more, for 207 countries over the course of the pandemic. 

## Usage

To use this project, follow these steps:

1. Clone the repository to your local machine.
2. Install [Snakemake](https://snakemake.readthedocs.io/en/v6.15.5/getting_started/installation.html).
3. Activate snakemake environment.
4. Ensure you have all required dependencies installed (see `docs/requirements.txt`).
5. Add the project root (rse-project2) to the PYTHONPATH. On windows set yourself in the project root, then do:
```shell
    $env:PYTHONPATH = (Get-Location).Path 
    set PYTHONPATH=%cd%
 ``` 
This is necessary otherwise you will get import errors (no module named bin).

6. Run the workflows (or just the one of interest) by running the corresponding Snakefile with the desired configuration (see below) by setting
yourself in the corresponding directory: `bin\workflow_1`, `bin\workflow_2` or `bin\workflow_3`.
7. Check the analysis results in the `results` directory. For the processed datasets see  `data`.

### Run workflow 1
Workflow 1 refers to research point 1 and it allows to configure the following parameters:
- *continent* : can be one of ['Europe', 'Asia', 'Africa', 'America', 'Oceania']. The default option is Europe.
- *year* : the year to which analysis is restricted, from 2020 to 2024. The default option is 2021.
- *y* : the outcome plotted on y axis of the line plot. It can be either "new_cases" or "new_deaths". We used *y*="new_cases".

All the above parameters can be edited in the file `bin\workflow_1\configuration_w1.yaml`. Consistency checks are made within the workflow components, in case of invalid choices or mispellings you will receive an error. 

After choosing the desired configuration, make sure to be inside `bin\workflow_1` and run `SnakefileWorkflow1` this way to **get all** the outputs:

```shell
snakemake -s SnakefileWorkflow1 --cores all all
```

The produced files will be stored in  `results\workflow_1`, except for the processed datasets that will be stored in `data`.

To **delete all** the outputs run:

```shell
 snakemake -s SnakefileWorkflow1 --cores all clean
 ```

To produce just a single output run the above code with the name of the output file instead of the rule name (for this you will have to look inside the Snakefile how the output names are generated).

When changing the configuration the files are not overwritten, the new files will be added together with the existing ones. 

##### Outputs:

### Run workflow 2
Workflow 2 refers to research point 2 and it allows to configure the following parameters:
- *normalize* : can be either True (= outcomes are normalized by population) or False. The default option is False.
- *year* : the year to which analysis is restricted, from 2020 to 2024. The default option is 2023.

Here the above parameters are edited directly from the CL as shown below. Consistency checks are made within the workflow components, in case of invalid choices or mispellings you will receive an error. 

After choosing the desired configuration (in the example we use the default one), make sure to be inside `bin\workflow_2` and run `SnakefileWorkflow2` this way to **get all** the outputs:

```shell
snakemake -s SnakefileWorkflow2 --cores all all --config normalize=False year=2023
```

The produced files will be stored in  `results\workflow_2`, except for the processed datasets that will be stored in `data`.

To **delete all** the outputs run:

```shell
 snakemake -s SnakefileWorkflow2 --cores all clean
 ```

To produce just a single output run the above code with the name of the output file instead of the rule name (for this you will have to look inside the Snakefile how the output names are generated).

#### Outputs:
Given a chosen configuration for workflow 2, which will be of the form: {normalize, year}, the produeced outputs in `results\workflow_2` will be:

normalize == True:
- <ins>barplot_total_cases_norm_by_continent_{year}.png</ins>: bar plot showing total cases in the chosen year for each continent. For each continent, total cases is normalized by the population of that continent.
-  <ins>barplot_total_deaths_norm_by_continent_{year}.png</ins>: bar plot showing total deaths in the chosen year for each continent. For each continent, total deaths is normalized by the population of that continent.

normalize == False:
-  <ins>barplot_total_cases_by_continent_{year}.png</ins>: bar plot showing total cases in the chosen year for each continent.
-  <ins>barplot_total_deaths_by_continent_{year}.png</ins>: bar plot showing total deaths in the chosen year for each continent.

When changing the configuration the files are not overwritten, the new files will be added together with the existing ones.

### Run workflow 3
Workflow 3 refers to research point 3 and it allows to configure the following parameters:
- *germany* : can be either True (= restrict the analysis to Germany) or False (= consider whole Europe). The default option is False.
- *time* : choose the time period by which the data is aggregated, can be either 'month' or 'semester'. The default option is 'month'.
- *x*  and *y* : the variables for which the correlation is tested and for which the regression plot is produced (**only if** the hypothesis test results are significant). We used *x*='new_vaccinations' and *y*='deaths_over_cases'. Both *x* an *y* can be changed by choosing in the set ['new_vaccinations', 'new_deaths', 'new_cases', deaths_over_cases', 'month'], but keep in mind that other couples probably won't make a lot of sense (for example: it's obvious that new cases and new deaths are positively correlated).

All the above parameters can be edited in the file `bin\workflow_3\configuration_w3.yaml`. Consistency checks are made within the workflow components, in case of invalid choices or mispellings you will receive an error. 

After choosing the desired configuration, make sure to be inside `bin\workflow_3` and run `SnakefileWorkflow3` this way to **get all** the outputs:

```shell
snakemake -s SnakefileWorkflow3 --cores all all
```

The produced files will be stored in  `results\workflow_3`, except for the processed datasets that will be stored in `data`.

To **delete all** the outputs run:

```shell
 snakemake -s SnakefileWorkflow3 --cores all clean
 ```

To produce just a single output run the above code with the name of the output file instead of the rule name (for this you will have to look inside the Snakefile how the output names are generated).

#### Outputs:
Given a chosen configuration for workflow 3, which will be of the form: {germany, time, x, y}, from "germany" (it's bool) we derive the wildcard  {place}, which will be either "europe" or "germany". Then, the produeced outputs in `results\workflow_3` will be:
-  <ins>correlationtest_results__by_{time}_{place}.txt</ins> :  contains results of correlation hp test for x and y (values are calculated according to the chosen {time} and {place})
-  <ins>correlationtest_results__significance_by_{time}_{place}.txt</ins>: contains either True (= pvalue and correlation coefficient of the test are meaningful) or False. It's used to activate (or not) the rule to get the below regression  plot.
-  <ins>regplot_deaths_over_cases_new_vaccinations_by_{time}_{place}.png</ins>: either empty .png file (if above output is False) or .png file with regression and scatter plot of x and y (if above output is True).
-  <ins>trendplot_deaths_over_cases__new_cases_by_{time}_{place}.png</ins> : trend plot for deaths over cases vs new cases against {time}. For {place}. 
- <ins>trendplot_deaths_over_cases__new_vaccinations_by_{time}_{place}.png</ins> : trend plot for deaths over cases vs new vaccinations against {time}. For {place}. 
-  <ins>trendplot_new_deaths__new_cases_by_{time}_{place}.png</ins> : trend plot for new deaths vs new cases against {time}. For {place}.
-  <ins>trendplot_new_deaths__new_vaccinations_by_{time}_{place}.png </ins> : trend plot for new deaths vs new vaccinations against {time}. For {place}.

## Contributing

We welcome contributions from the community! For detailed guidelines on how to get involved, please refer to our [Contribution Guidelines](CONTRIBUTING.md).

## Code of Conduct

All contributors are expected to follow the project's [Code of Conduct](CONDUCT.md). Please read it carefully before participating.

## Questions and Support

If you have any questions or need assistance, please open an issue on the project's GitHub repository so we can discuss the question together. Otherwise 

## Contact information

Email addresses: [corona@uni-potsdam.de](mailto:corona@uni-potsdam.de), [nick.thomas@uni-potsdam.de](mailto:nick.thomas@uni-potsdam.de), [joy.md@uni-potsdam.de](mailto:joy.md@uni-potsdam.de), [omar.shindy@uni-potsdam.de](mailto:omar.shindy@uni-potsdam.de) .

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file for details.
