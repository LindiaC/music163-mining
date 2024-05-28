import pandas as pandas
import os

file_path = 'MusicList_2024-05-28T02-23-05.csv'
data = pandas.read_csv(file_path, encoding='utf-8')

for index, row in data.iterrows():
    name = row['SongListName']
    tag = row['Labels']
    id = row['SongsListID']
    Collection = row['Collection']
    item = name + '##' + tag + '##' + str(id) + '##' + str(Collection) + '\n'
    with open('songlist.csv', 'a',encoding='utf-8') as f:
            f.write(item)