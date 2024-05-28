import pandas as pandas
import os
import requests

file_path = 'MusicList_2024-05-28T02-23-05.csv'
data = pandas.read_csv(file_path, encoding='utf-8')

for index, row in data.iterrows():
    list_name = row['SongListName']
    list_tag = row['Labels']
    list_id = row['SongsListID']
    list_Collection = row['Collection']
    list_item = list_name + '##' + list_tag + '##' + str(list_id) + '##' + str(list_Collection)

    list_url = 'http://localhost:3000/playlist/detail?id=' + str(list_id)
    list_src = requests.get(list_url).json()
    song_item = ''
    for song in list_src['playlist']['trackIds']:
        song_id = song['id']
        song_url = 'http://localhost:3000/song/detail?id='+str(song_id)
        song_src = requests.get(song_url).json()
        song_name = song_src['songs'][0]['name']
        song_singer = ''
        for singer in song_src['songs'][0]['ar']:
            song_singer += singer['name']
            if singer != song_src['songs'][0]['ar'][-1]:
                 song_singer += '|'
        song_pop = song_src['songs'][0]['pop']
        song_item += '\t'+ str(song_id) + '::' + song_name + '::' + song_singer + '::' + str(song_pop)
    with open('songlist2songs.txt', 'a',encoding='utf-8') as f:
        f.write(list_item + song_item + '\n')
        print("write ", list_name, "successfully")
