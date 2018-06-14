import configparser
import os
import pprint
import datetime
import requests
from bs4 import BeautifulSoup
import connectdb

#getting list of websites from the config file

def get_config():
    config=configparser.ConfigParser()
    config.read(get_location())
    #print(config.sections())
    data=dict()
    for each_sections in config.sections():
        for each_data in config[each_sections]:
            data[each_data]=config[each_sections][each_data]
    #pprint.pprint(data)
    return data

#get config location

def get_location():
    return os.getcwd()+'/config.ini'

#get website data

def get_website_data():

    data=get_config()
    #pprint.pprint(data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    request=requests.get(data.get('weatherkol'),headers=headers)
    print(request.status_code)
    soup=BeautifulSoup(request.content,'html.parser')
    #print(soup.prettify())
    #getting the temperature by scraping the website
    #5 day temparature list
    div=soup.findAll('div',attrs={'id':'feed-tabs'})
    date_div=div[1].findAll('h4')
    condition=div[1].findAll('span',attrs={'class':'cond'})
    small_temp = div[1].findAll('span', attrs={'class': 'small-temp'})
    now=datetime.datetime.now()
    count=0
    main_data_div=div[1].findAll('span',attrs={'class':'large-temp'})
    for each_temps in main_data_div:
        #print(date_div[count].get_text()+":"+each_temps.get_text()[:-1])
        #database instance

        dbModule=connectdb.Dbfunction(data.get('hostname'),data.get('port'),data.get('dbname'),data.get('collection'))
        oldpayload={
            "date":date_div[count].get_text(),
            "year": now.year,
        }
        if count==0:
            smltemp=float(small_temp[count].get_text()[1:-2])
        else:
            smltemp = float(small_temp[count].get_text()[1:-1])
        payload={
            "date":date_div[count].get_text(),
            "year":now.year,
            "temp":float(each_temps.get_text()[:-1]),
            "smalltemp":smltemp,
            "cond":condition[count].get_text(),
            "unit":"C"
        }

        print(dbModule.upsert(payload=payload,oldpayload=oldpayload))
        count+=1

if __name__ == '__main__':
    get_website_data()

