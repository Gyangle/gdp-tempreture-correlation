import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import requests as re
import json

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
    country_list = []
    for country in dict:
        country_list.append((country['name']['common'],country['cca3']))

    # create table with desirable names and params
    cur.execute("DROP TABLE IF EXISTS Countries")
    cur.execute("CREATE TABLE Countries (c_code TEXT PRIMARY KEY, c_name TEXT)")
    conn.commit()
    
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

# write country data to db
def write_countries(cur, conn, country_list):
    for country in country_list:
        cur.execute("INSERT INTO Countries (c_code, c_name) VALUES (?,?)", (country[1], country[0]))
    conn.commit()


def main():
    cur, conn = setUpDatabase('countries.db') # do not modify
    create_country_table(cur, conn) 
    # TODO: make one function here to create each table


if __name__ == "__main__":
    main()




