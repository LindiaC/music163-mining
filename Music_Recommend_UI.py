import io
from surprise import KNNBaseline, Reader
from surprise import Dataset

import os
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
import tkinter as tk
import time
import tkinter.ttk
import surprise
import pickle

import gensim

from tkinter.ttk import Separator

# UI
################################################################################################################
# 创建窗口：实例化一个窗口对象。

def startup():
    global list_algo
    global id_name_dic
    global name_id_dic
    global trainset
    global song_dic
    global song_model
    global song_id_name_dic
    global song_name_id_dic
    # 重建歌单id到歌单名的映射字典
    id_name_dic = pickle.load(open("./pro_data/playlist.pkl","rb"))
    result.set("加载歌单id到歌单名的映射字典完成...")
    # 重建歌单名到歌单id的映射字典
    name_id_dic = {}
    for playlist_id in id_name_dic:
        name_id_dic[id_name_dic[playlist_id]] = playlist_id
    result.set("加载歌单id到歌单名的映射字典完成...\n加载歌单名到歌单id的映射字典完成...")
    file_path = os.path.expanduser('./163_music_suprise_format.txt')
    # 指定文件格式
    reader = Reader(line_format='user item rating timestamp', sep=',')
    # 从文件读取数据
    music_data = Dataset.load_from_file(file_path, reader=reader)
    # 计算歌曲和歌曲之间的相似度
    result.set("加载歌单id到歌单名的映射字典完成...\n加载歌单名到歌单id的映射字典完成...\n构建数据集...")
    trainset = music_data.build_full_trainset()
    result.set("加载歌单id到歌单名的映射字典完成...\n加载歌单名到歌单id的映射字典完成...\n构建数据集...\n加载歌单推荐模型")
    # 可以用下面的方式载入
    list_algo = surprise.dump.load('./model/recommendation.model')[1]
    # list_algo.fit(trainset)
    result.set("加载歌单id到歌单名的映射字典完成...\n加载歌单名到歌单id的映射字典完成...\n构建数据集...\n加载歌单推荐模型...\n加载歌曲库...")
    # 加载歌曲的id——name+"\t"+artist
    song_dic = pickle.load(open("./pro_data/song.pkl","rb"))
    result.set("加载歌单id到歌单名的映射字典完成...\n加载歌单名到歌单id的映射字典完成...\n构建数据集...\n加载歌单推荐模型...\n加载歌曲库...\n加载歌曲推荐模型...")
    # 加载训练模型
    model_file_path = "./model/song2vec.model"
    song_model = gensim.models.Word2Vec.load(model_file_path)

    # 重建歌曲id到歌曲名的映射字典
    song_id_name_dic = pickle.load(open("./pro_data/song.pkl","rb"))
    # print("加载歌曲id到歌曲名的映射字典完成...")
    # 重建歌曲名到歌曲id的映射字典
    song_name_id_dic = {}
    for song_id in song_id_name_dic:
        song_name_id_dic[song_id_name_dic[song_id]] = song_id
    # print("加载歌曲名到歌曲id的映射字典完成...")
    # print (song_name_id_dic)
    result.set("加载歌单id到歌单名的映射字典完成...\n加载歌单名到歌单id的映射字典完成...\n构建数据集...\n加载歌单推荐模型...\n加载歌曲库...\n加载歌曲推荐模型...\n完成！！")

def Songlist_Recommend(current_playlist):
    global list_algo
    global id_name_dic
    global name_id_dic
    global trainset 
    algo=KNNBaseline()
    algo.fit(trainset)
    playlist_id = name_id_dic[current_playlist]
    # print("歌单id", playlist_id)
    # 取出来对应的内部user id => to_inner_uid
    playlist_inner_id = algo.trainset.to_inner_uid(playlist_id)
    # print("内部id", playlist_inner_id)

    playlist_neighbors = algo.get_neighbors(playlist_inner_id, k=10)

    # 把歌曲id转成歌曲名字
    # to_raw_uid映射回去
    playlist_neighbors = (algo.trainset.to_raw_uid(inner_id)
                        for inner_id in playlist_neighbors)
    playlist_neighbors = (id_name_dic[playlist_id]
                        for playlist_id in playlist_neighbors)

    return playlist_neighbors

def Song_Recommend(song_name):
    global song_dic
    global song_model
    global song_id_name_dic
    global song_name_id_dic
    song_id = song_name_id_dic[song_name]
    result = song_model.wv.most_similar(positive=song_id)
    return result

def ConfirmSonglist():
    global list_algo
    songlist = songlist_entry.get()
    # messagebox.showinfo(title="歌单名", message=songlist)
    playlist_neighbors = Songlist_Recommend(songlist)
    output = "和歌单 《" + songlist + "》 最接近的10个歌单为：\n"
    for playlist in playlist_neighbors:
        output += playlist + "\n"
    result.set(output)

def ConfirmSong():
    global song_dic
    global song_model
    song = song_entry.get()
    artist = artist_entry.get()
    song_name = song + "\t" + artist
    song_result = Song_Recommend(song_name)
    output = "和歌曲 《" + song_name + "》 最接近的10个歌曲为：\n"
    for song in song_result:
        output += song_dic[song[0]] + "\n"
    result.set(output)


def Cancel():
    result.set("")
    songlist_entry.delete(0, END)
    song_entry.delete(0, END)
    artist_entry.delete(0, END)

root = Tk()

# 窗口大小
root.geometry("600x600+374+182")

#  窗口标题
root.title("Music Recommendation System")

############################################################
# 添加标签控件
title = Label(root, text="网易云音乐歌曲推荐", font=("微软雅黑", 25), fg="black")
# 定位
title.grid(row=0, column=1)
#############################################################

start = tk.Button(root, text='START', command=lambda:startup())
start.grid(row=1, column=1, padx=5, pady=5)
#############################################################
sub1 = Label(root, text="根据歌单推荐歌单", font=("微软雅黑", 10), fg="black")
# 定位
sub1.grid(row=2, column=1)
###################################################################
tk.Label(root, text='请输入歌单名').grid(
    row=3, column=0, padx=5, pady=5)  # 创建label 提示这是输入歌单

songlist_entry = tk.Entry(root, font=("微软雅黑",10), width=30)
songlist_entry.grid(row=3, column=1, padx=5, pady=5)  # 创建歌单名称输入框

songlist_confirm = tk.Button(root, text='确认', command=lambda:ConfirmSonglist())
songlist_confirm.grid(row=3, column=2, padx=5, pady=5)
##########################################################################
sub2 = Label(root, text="根据歌曲推荐歌曲", font=("微软雅黑", 10), fg="black")
# 定位
sub2.grid(row=4, column=1)
##########################################################################
tk.Label(root, text='请输入歌曲名').grid(
    row=5, column=0, padx=5, pady=5)  # 创建label 提示这是输入歌曲

song_entry = tk.Entry(root, font=("微软雅黑",10), width=30)
song_entry.grid(row=5, column=1, padx=5, pady=5)  # 创建歌曲名称输入框


###
tk.Label(root, text='请输入歌手名').grid(
    row=6, column=0, padx=5, pady=5)
artist_entry = tk.Entry(root, font=("微软雅黑",10), width=30)
artist_entry.grid(row=6, column=1, padx=5, pady=5)

song_confirm = tk.Button(root, text='确认', command=lambda:ConfirmSong())
song_confirm.grid(row=6, column=2, padx=5, pady=5)

result = tk.StringVar()   # 创建字符串变量
result.set("请按START初始化")   # 初始化字符串变量
tk.Label(root,textvariable=result,justify=LEFT).grid(row=7, column=1, padx=5, pady=5)

cancel = tk.Button(root, text='取消', command=lambda:Cancel())
cancel.grid(row=8, column=1, padx=5, pady=5)


root.mainloop()