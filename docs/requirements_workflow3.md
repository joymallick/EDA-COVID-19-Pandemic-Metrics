# Workflow 3: exploring relationship between deaths, cases and vaccinations for Covid-19.
The results of this workflow allow to get an overview of the relationship between number of new cases, deaths and vaccinations by month or semester. The analysis can be
performed either considering whole Euorpe or the specific case of Germany. The workflow has 5 components, among which 3 are tailored to the covid-19 dataset (components 1, 2 and 5).
## Abstract workflow
### Uml activity diagram
![Alt text](./Workflow3ActivityDiagram.png)
### Explanation
1. Perform a general processing of the covid-19 dataset, in particular create new time columns: year, semster, month.
2. Perform a specific processing of output of component 1 for the research aim of this workflow: aggregate data by either month or semester, filter by continent == Europe or by location == Germany, and create a new outcome, "deaths_over_cases", storing the ratio between new number of deaths and new number of cases w.r.t the chosen time period (month/semester).
3. Correlation test: the component performs a spearman hypothesis test for two columns of choice of a given dataset. In our case this component is run with the dataset output of component 2 and variables: "new vaccinations" and "deaths_over_cases".
4. Regression plot: the component produces a regression plot (including scatter plot) for two columns of choice of a given dataset. We will run this component with the variables fed to component 3 **only if** the results of the correlation test are significant w.r.t provided thresholds for pvalue and absolute value of the correlation.
5. Trend plots: the component produces 3 trend plots, i.e plots showing two y variables over the same x axis, that here is a time variable. The produced trend plots compare "new deaths"-"new cases", "new deaths"-"new vaccinations", and "deaths_over_cases"-"new_vaccinations". The x variable is either month or semester. 

## Component analysis

| Abstract Workflow Node                  | Input(s)     | Output(s)                 | Implementation     |
|-----------------------------------------|--------------|---------------------------|--------------------|
| data processing            | csv file name, outfile name | .csv file         | own implementation  |
| data processing workflow 3                 | csv file name, outfile name, time period (month or semseter), germany (True or False)  | .csv file   | own implementation |
| correlation test                         | csv file name, outfile name, var1, var2,  pvalue and correlation abs thresholds     | .txt files (x2) with results and results significance     | own implementation |
| regression plot                   | csv file, x, y, outfile name    | .png  file | own implementation |
| trend plots                    | csv file name, outfile name (x3),  x variable     | .png file  (x3)            | own implementation |


