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
### -- gdpTempScaled
- Graph logarithmic scaled Graph GDP vs Temperature
### --drop all
- Drop all the tables except the meta data table
### --drop [table names]
- drop a specific table




## Documentation

def create_GDP_table(cur, conn)
"" Takes in cur and conn to create the table with 2 columns: country code and country GDP
   Using the ap link 'https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json&date=2020' 
   to fectch the according GDP for each country code in the CountryCode table. 
   The first time run this function should return an empty table in the database, 
   the rest times of running this table should add additional 25 items to the CountryGDP table""


def graph_TempGap_GDP(cur, conn,file_name)

"" Takes in cur, conn and. file_name. Return a bar chart with x-axis as 
 4 different temperature ranges, y-axis be the average country GDP in that tneperature range.
 Should also create a csv file and put the calculated data into it"




