# encoding : utf-8
import time
import re
import pymysql
from selenium import webdriver
import csv
import requests

def getHotSong(singer_id):
    url = 'http://localhost:3000/artists?id='+str(singer_id)
    # driver = webdriver.Edge()
    page_src = requests.get(url).json()
    time.sleep(1)
    # page_src = driver.page_source
    return page_src

# format 2925502::Si Seulement::Lynnsha::100.0
def json_to_csv(json, singer_name):
    hotsongs = json['hotSongs']
    for song in hotsongs:
        data = str(song['id']) + '::' + song['name'] + '::' +str(singer_name)+ '::'+str(song['pop']) + '\n'
        with open('song.csv', 'a',encoding='utf-8') as f:
            f.write(data)

with open('singer.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        singer_id = row[0]
        singer_name = row[1]
        json = getHotSong(singer_id)
        json_to_csv(json, singer_name)
        print("write ", singer_name, "successfully")
        

