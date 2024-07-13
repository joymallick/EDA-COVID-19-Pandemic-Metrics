# Workflow 2: Exploring in which continent the highest number of deaths and cases were recorded.
The results that can be derived by this workflow allow to get an overview of how the number of deaths or cases differed by continents. The workflow has 4 components, among which the processing components (1 and 2) are tailored to the covid-19 dataset. 

### Uml activity diagram
![Alt text](./Workflow3ActivityDiagram.png)
### Explanation
1. Perform a general processing of the covid-19 dataset, in particular create new time columns: year, semster, month.
2. Process the data to create a dataset with relevant variables (e.g. total_cases,total_deaths) and COVID-19 metrics.
3. Create a bar plot of total_cases or total_deaths for each continent over a chosen year between 2020 to 2023.


## Component analysis

| Abstract Workflow Node                  | Input(s)     | Output(s)                 | Implementation     |
|-----------------------------------------|--------------|---------------------------|--------------------|
| Data processing            | csv file name, outfile name | .csv file         | own implementation  |
| Data processing workflow 2    | csv file name, outfile name, normalize(True or False)  | .csv file   | own implementation |
| Bar plot                   | csv file name, outfile name, event   | .png  file | own implementation |



