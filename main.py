import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import requests as re
import json
import argparse
from bs4 import BeautifulSoup

# command arg 1: 
# python3 main.py --drop all
# drop all the tables except the meta data table

# command arg 2: 
# python3 main.py --drop [table names]
# drop a specific table


# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    

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
    # if all rows stored
    if (count_row >= 250):
        return

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

        cur.execute("DROP TABLE IF EXISTS Temperature")
        cur.execute("CREATE TABLE IF NOT EXISTS Temperature (country_name TEXT PRIMARY KEY, temp FLOAT)")
        conn.commit()

        for row in all_rows:
            country_name = row.find('td', {'class':'col-3 odd'})
            country_temp = row.find('td', {'class':'col-4 even'})
            cur.execute("INSERT INTO Temperature (country_name, temp) VALUES (?,?)", (country_name.getText(), country_temp.getText()))
        conn.commit()


##############################################################################################


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
    args = parser.parse_args()
    if  (args.drop):
        drop_table(cur, conn, args.drop)


      # initialize tables
    create_country_table(cur, conn) 
    create_GDP_table(cur,conn)
    create_temperature_table(cur,conn)
  


   

  



if __name__ == "__main__":
    main()




