import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import requests as re
import json
import argparse
from bs4 import BeautifulSoup

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
    # create table with desirable names and params
    #cur.execute("DROP TABLE IF EXISTS Countries")

    cur.execute("CREATE TABLE IF NOT EXISTS Countries (c_code TEXT PRIMARY KEY, c_name TEXT)")
    conn.commit()
    
    cur.execute("SELECT COUNT (*) FROM Countries")
    conn.commit()

    count_row = cur.fetchall()
    count_row = count_row[0][0]

    # if all rows stored
    if (count_row >= 250):
        return

    for i in range(count_row, count_row+25):
        # insert item
        cur.execute("INSERT OR IGNORE INTO Countries (c_code, c_name) VALUES (?,?)", (sorted_list[i][1], sorted_list[i][0]))


    """" Old code
    # write 25 items to db once
    counter = 0
    temp = []
    while(counter != len(country_list)):
        # apppend items to temp
        temp.append(country_list[counter])
        
        # when size of temp reach 25
        if len(temp) == 25:
            write_countries(cur, conn, temp) # 1. pass temp to the write_countries
            temp = []                        # 2. clear temp
        
        counter = counter + 1

    # if temp still has somthing left, but not yet commit
    if len(temp) != 0:
        write_countries(cur, conn, temp)
    """
    
"""
# write country data to db
def write_countries(cur, conn, country_list):
    for country in country_list:
        cur.execute("INSERT INTO Countries (c_code, c_name) VALUES (?,?)", (country[1], country[0]))
    conn.commit()
"""


def drop_table(cur, conn, table_name):
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()



def create_GDP_table(cur, conn):
    cur.execute("SELECT c_code FROM Countries")
    conn.commit()
    code = cur.fetchall()

    code_list = []
    for i in code:
        code_list.append(i[0])

    print(code_list)


def create_temperature_table(cur, conn):
    soup = BeautifulSoup(re.get('https://listfist.com/list-of-countries-by-average-temperature').text, 'html.parser')
    body = soup.find('tbody')
    all_rows = body.find_all('tr')

    cur.execute("CREATE TABLE IF NOT EXISTS Temperature (country_name TEXT PRIMARY KEY, temp FLOAT)")
    conn.commit()

    for row in all_rows:
        country_name = row.find('td', {'class':'col-3 odd'})
        country_temp = row.find('td', {'class':'col-4 even'})
        print(country_name.getText())
        print(country_temp.getText())
        cur.execute("INSERT INTO Temperature (country_name, temp) VALUES (?,?)", (country_name.getText(), country_temp.getText()))
    conn.commit()


def main():
    cur, conn = setUpDatabase('countries.db') # do not modify

    parser = argparse.ArgumentParser()
    parser.add_argument('--drop',  type=str)
    args = parser.parse_args()
    if  (args.drop):
        drop_table(cur, conn, args.drop)

    create_country_table(cur, conn) 
    # TODO: make one function here to create each table
    create_GDP_table(cur,conn)
    create_temperature_table(cur,conn)




if __name__ == "__main__":
    main()




