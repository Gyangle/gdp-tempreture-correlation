# Visualization on Correlation between GDP and Average Tempreture of a Country
## Group members:
- Grant Yang (gyangle@umich.edu)
- Coco Yu
- Rachel Xie

## How to run:
1. To drop all table to reset the database
```
python3 main.py --drop all
```
2. To create table and fetch for data to database
```
python3 main.py # or just hit run in VSCode
```
3. After fetching at least data 3 times, render the graph
 ```
python3 main.py [table arguments, see below ]
```   

## Arguments:
### --top10
- Graph Average Tempreture for Countries with TOP10 GDP
### --tempRange
- Graph Average Country GDP in Different Temperature Range
### --gdpTemp
- Graph GDP vs Temperature
### --drop all
- Drop all the tables except the meta data table
### --drop [table names]
- drop a specific table