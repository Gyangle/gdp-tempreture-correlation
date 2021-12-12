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




## Function Documentation
### create_GDP_table(cur, conn)
- Takes in cur and conn to create the table with 2 columns: country code and country GDP
   Using the ap link 'https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json&date=2020' 
   to fectch the according GDP for each country code in the CountryCode table. 
   The first time run this function should return an empty table in the database, 
   the rest times of running this table should add additional 25 items to the CountryGDP table""

### graph_TempGap_GDP(cur, conn,file_name)
- Takes in cur, conn and a file_name. Return a bar chart with x-axis as 
 4 different temperature ranges, y-axis be the average country GDP in that tneperature range.
 Should also create a csv file and put the calculated data into it

### create_country_table(cur, conn)
- Takes in cur, conn to create the tables for storing country codes and country names. It create a get
  request to the API end point provided by https://restcountries.com/. The function extract each country's
  name, with corresponding country code in CCA3 standard, stored them into sepearate table. Both table
  share an unique integer primary key. 
- During the fisrt run, it creates two tables and stored 25 items. For the steps of second and above, it
  adds 25 items at a time to both tables, till it reach the maximum of 250 countries. 

### graph_top10_gdp_temp(cur, conn)
- Takes in cur and conn to graph the Tempretue is celcius for the top 10 countries with the greatest amount of GDP(decending order). Also, write the calculated data used for graphing into the text file. 

### writeData(file, head, content)
- Takes in a file name, the header for csv content, the csv content itself. It writes the content and header 
  into the file. 
- The head should be an list/tuple with all fields in strings. The content should be a list with tuples of data in a row. Example: 
   ```
   writeData("top10.txt", ("country_names", "country_gdp"), [("1111", "222"), ("33333", "44444")])
   ```

### setUpDatabase(db_name)
- This function takes a file name of a database and create connection with it. Return the cur and conn for searching and modifing the database. 

### main()
- Parse the argument from command runner, run the desireable commands. 