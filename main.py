import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import requests as re
import json
import argparse
import csv
from bs4 import BeautifulSoup


def create_country_table(cur, conn):
    # store all country names in data in an LIST**
    base_url = "https://restcountries.com/v3.1/all"
    r = re.get(base_url)
    data = r.text
    dict = json.loads(data)
    #dict_sorted = sorted(dict.items(), key = lambda x: x[1])
    country_list = []
    for country in dict:
        country_list.append((country['name']['common'],country['cca3']))
    sorted_list = sorted(country_list, key = lambda x: x[1])

    # create tables
    cur.execute("CREATE TABLE IF NOT EXISTS CountryCode (id INTEGER PRIMARY KEY AUTOINCREMENT, c_code TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS CountryName (id INTEGER PRIMARY KEY AUTOINCREMENT, c_name TEXT)")
    conn.commit()
    
    # check if need to add 25
    cur.execute("SELECT COUNT (*) FROM CountryCode")
    count_row = cur.fetchall()
    count_row = count_row[0][0]
    # if all rows stored
    if (count_row >= 250):
        return

    for i in range(count_row, count_row+25):
        # insert item
        cur.execute("INSERT OR IGNORE INTO CountryCode (c_code) VALUES (?)", (sorted_list[i][1],))
        cur.execute("INSERT OR IGNORE INTO CountryName (c_name) VALUES (?)", (sorted_list[i][0],))
    conn.commit()


def create_GDP_table(cur, conn):
    # fetch all country code from the CountryCode table
    cur.execute("SELECT c_code FROM CountryCode")
    conn.commit()
    code = cur.fetchall()

    code_list = []
    for i in code:
        code_list.append(i[0])

  

    # create CountryGDP table
    cur.execute("CREATE TABLE IF NOT EXISTS CountryGDP (c_code TEXT UNIQUE, c_GDP NUMERIC)")
    conn.commit()

    # find how many items are currently in the CountryCode table
    cur.execute("SELECT COUNT (*) FROM CountryCode")
    count_row = cur.fetchall()
    count_row = count_row[0][0]
    

    # fetch new added country codes' according GDP
    for i in range(count_row - 25, count_row):

        base_url = f"https://api.worldbank.org/v2/country/{code_list[i]}/indicator/NY.GDP.MKTP.CD?format=json&date=2020"
        r = re.get(base_url)
        data = r.text
        dict = json.loads(data)
        # some countries don't have value for GDP, ignore those
        if len(dict) > 1 and dict[1] != None and dict[1][0]["value"] != None:
            cur.execute("INSERT INTO CountryGDP (c_code, c_GDP) VALUES (?,?)", (code_list[i], dict[1][0]["value"]))
    conn.commit()

                #print(dict[1][0]["value"])

    
def create_temperature_table(cur, conn):
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    need_create = True
    for name in res.fetchall():
        if "Temperature" == name[0]:
            need_create = False
    
    if need_create:

        soup = BeautifulSoup(re.get('https://listfist.com/list-of-countries-by-average-temperature').text, 'html.parser')
        body = soup.find('tbody')
        all_rows = body.find_all('tr')

        cur.execute("CREATE TABLE IF NOT EXISTS Temperature (country_name TEXT PRIMARY KEY, temp FLOAT)")
        conn.commit()

        for row in all_rows:
            country_name = row.find('td', {'class':'col-3 odd'})
            country_temp = row.find('td', {'class':'col-4 even'})
            cur.execute("INSERT INTO Temperature (country_name, temp) VALUES (?,?)", (country_name.getText(), country_temp.getText()))
        conn.commit()


##############################################################################################

def graph_TempGap_GDP(cur, conn,file_name):
    average_GDP = []
    temps_range = []

    temps_range.append("-20~0")
    temps_range.append("0~10")
    temps_range.append("10~20")
    temps_range.append("20~30")


   

    cur.execute(
        """
        SELECT AVG(CountryGDP.c_GDP)
        FROM CountryCode JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
        WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
        AND CountryGDP.c_code = CountryCode.c_code 
        AND Temperature.temp >= -20 AND Temperature.temp < 0
        """)
    

    conn.commit()
    data = cur.fetchall()
    average_GDP.append(data[0][0])
    


    cur.execute(
            """
            SELECT AVG(CountryGDP.c_GDP)
            FROM CountryCode JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
            WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
            AND CountryGDP.c_code = CountryCode.c_code 
            AND Temperature.temp >= 0 AND Temperature.temp < 10
            """)

    conn.commit()
    data_2 = cur.fetchall()
    average_GDP.append(data_2[0][0])

    cur.execute(
            """
            SELECT AVG(CountryGDP.c_GDP)
            FROM CountryCode JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
            WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
            AND CountryGDP.c_code = CountryCode.c_code 
            AND Temperature.temp >= 10 AND Temperature.temp < 20
            """)
    conn.commit()
    data_3 = cur.fetchall()
    average_GDP.append(data_3[0][0])

    cur.execute(
            """
            SELECT AVG(CountryGDP.c_GDP)
            FROM CountryCode JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
            WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
            AND CountryGDP.c_code = CountryCode.c_code 
            AND Temperature.temp >= 20 AND Temperature.temp < 30
            """)

    conn.commit()
    data_4 = cur.fetchall()
    average_GDP.append(data_4[0][0])




    with open(file_name, "w", newline="") as fileout:
        
        header = ["Temperature Range", "Average GDP"]

        csvwriter = csv.writer(fileout) 

        csvwriter.writerow(header)


        
        for i in range(0,4):
            row_value = []
            row_value.append(temps_range[i])
            row_value.append(average_GDP[i])
            csvwriter.writerow(row_value)

        #row_value.append(average_GDP)
    
    fileout.close()


    plt.bar(temps_range, average_GDP, align='center', alpha=0.5)
    plt.xticks(temps_range, rotation = 90)
    plt.ylabel('Countries Average GDP')
    plt.xlabel('Temperature Ranges')
    plt.title('Average Country GDP in Different Temperature Range')
    plt.show()


def graph_top10_gdp_temp(cur, conn):
    cur.execute(
        """
        SELECT CountryName.c_name, Temperature.temp
        FROM CountryCode  JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
        WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
        AND CountryGDP.c_code = CountryCode.c_code
        ORDER BY CountryGDP.c_GDP DESC
        LIMIT 10
        """)
    conn.commit()
    data = cur.fetchall()
    country_names = []
    temps = []
    for i in data:
        country_names.append(i[0])
        temps.append(i[1])

    plt.figure(figsize=(10, 5))
    plt.barh(country_names, temps, color ='royalblue', alpha=0.7)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
    )
    plt.xlabel("Country Names(From greatest GDP to lowest)")
    plt.ylabel("Average Tempreture", labelpad=-680)
    plt.title("Average Tempreture for Countries with TOP10 GDP")
    plt.show()


def grah_GDPvsTemp(cur, conn, scaled = False):
    cur.execute(
        """
        SELECT CountryGDP.c_GDP, Temperature.temp
        FROM CountryCode  JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
        WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
        AND CountryGDP.c_code = CountryCode.c_code
        """
    )
    conn.commit()
    data = cur.fetchall()
    GDP = []
    temperature = []
    for i in data:
        GDP.append(round(i[0], 2))
        temperature.append(i[1])
    
    plt.scatter(GDP, temperature, color="orange", alpha=1)
    plt.ylabel('Temperature(°C)')
    plt.yticks(rotation=20)
    if scaled:
        plt.xscale('log')
        plt.xlabel('GDP($)')
        plt.title('Log of Countries\' GDP vs Temperature')
    else: 
        plt.xlabel('Log of GDP($)')
        plt.title('Countries\' GDP  vs Temperature')

    plt.grid(True)
    plt.show()
    

##############################################################################################

# Create Database connection
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    

def drop_table(cur, conn, table_name):
    if table_name == "all":
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res.fetchall():
            if name[0] != "sqlite_sequence": # avoid deleting meta data for auto increment
                cur.execute(f"DROP TABLE IF EXISTS {name[0]}")
        
    else:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

##############################################################################################

def main():
    cur, conn = setUpDatabase('countries.db') # do not modify
     
     # process the drop command
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop',  type=str)
    parser.add_argument('--top10', action='store_true')
    parser.add_argument('--tempRange',action='store_true')
    parser.add_argument('--gdpTemp',action='store_true')
    parser.add_argument('--gdpTempScaled',action='store_true')
    args = parser.parse_args()
    if  (args.drop):
        drop_table(cur, conn, args.drop)
        return
    # draw top10_gdp_temp
    if  (args.top10):
        graph_top10_gdp_temp(cur, conn)
        return
    # draw graph_TempGap_GDP
    if  (args.tempRange):
        graph_TempGap_GDP(cur, conn, "tempGapGDP.txt")
        return
    # draw grah_GDPvsTemp
    if  (args.gdpTemp):
        grah_GDPvsTemp(cur, conn)
        return
    # draw *scaled* grah_GDPvsTemp
    if  (args.gdpTempScaled):
        grah_GDPvsTemp(cur, conn, True)
        return

    # initialize tables/ add data
    create_country_table(cur, conn) 
    create_GDP_table(cur,conn)
    create_temperature_table(cur,conn)
    
    #graph_top10_gdp_temp(cur, conn)
    #graph_TempGap_GDP(cur, conn)
    # grah_GDPvsTemp(cur, conn)

if __name__ == "__main__":
    main()




