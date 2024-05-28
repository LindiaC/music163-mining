# music163-mining
网易云音乐数据挖掘全家桶2024焕然一新版

## 数据获取

部分数据可以直接通过解析网页元素获得

需要使用API的部分，原Node.js版本API已停止维护（就是直接在网址后面加/api就可以访问的那个），详情请见 https://github.com/Binaryify/NeteaseCloudMusicApi

因此使用了[Qt的替代版本](https://github.com/s12mmm3/QCloudMusicApi)

### 安装Qt版本的API库

·访问 https://github.com/s12mmm3/QCloudMusicApi/releases

·下载对应版本的release，例如`QCloudMusicApi-6.6.2-win64_msvc2019_64`

### API用法

支持直接通过url访问

· 运行刚刚下载的`QCloudMusicApi-6.6.2-win64_msvc2019_64/bin/ApiServer.exe`

· 参考[原Node.js版本API帮助文档](https://binaryify.github.io/NeteaseCloudMusicApi/#/)，使用方式完全一致，例如原文档中调用方法为`/song/detail?ids=347230`，则通过url访问`http://localhost:3000/song/detail?ids=347230`即可获得相同功能

### 获取所有歌手

相关文件：`getAllSinger.py`（参考了https://github.com/microw/Music_recommendation ）

本文件实现功能：获取所有华语男歌手、女歌手、组合的{id,姓名}，写入当前目录下的`singer.csv`。其他地区只需要修改相应参数即可。

```
5538,汪苏泷
3684,林俊杰
2116,陈奕迅
```

爬取结果（2024.05.27）已上传至`singer.csv`，共计约5700行

### 获取（大部分）歌曲

思路是通过上一步获取的歌手id，得到所有歌手详情页面的歌曲，也就是在访问网易云歌手页面所看到的“热门单曲50”。

相关文件：`getSingerHotSong.py`

相关API：`/artists?id=`

本文件实现功能：读取当前目录下`singer.csv`，对于每一行的歌手id与API接口组合为url，使用`requests`直接获取访问url获得的json数据并提取有用的字段，整理成如下格式，写入当前目录下的`song.csv`：

```
1908049566::算了吧::Aioz::100
1492023926::是想你的声音啊（说唱版）::Aioz::100
1849998058::22秒::Aioz::100
```

即`歌手id::歌曲名::歌手名::热度`，此格式为几个数年前网易云音乐推荐系统项目所处理的歌曲信息格式，例如[netease-music-recommendation](https://github.com/feiyutalk/netease-music-recommendation)、[Music_recommendation](https://github.com/microw/Music_recommendation)等等。

爬取结果（2024.05.27）已上传至`song.csv`，共计约260000行

### 获取所有歌单

相关文件夹：`wyyMusic`（参考了https://blog.csdn.net/qq_52181283/article/details/122277915 ， 有微小改动，请根据参考链接内教程步骤运行）

结果格式：

```
AmountOfPlay,AuthorID,Collection,Comment,CreationDate,Forwarding,Labels,NumberOfSongs,SongListName,SongsListID,Url
16286,445189786,78,1,2024-05-07,1,欧美 R&B/Soul 90后 ,36,欧美R&B入坑曲：封神旋律 是谁的一代青春,10009377589,https://music.163.com/playlist?id=10009377589
```


爬取结果（2024.05.28）已上传至`MusicList_2024-05-28T02-23-05.csv`，共计约600行

接下来再重新保存为便于数据挖掘的格式。

相关文件：`SonglistProcessor.py`

本文件实现功能：读取当前目录下指定csv（以`MusicList_2024-05-28T02-23-05.csv`为例），提取有用字段写入当前目录下`songlist.csv`：

```
欧美R&B入坑曲：封神旋律 是谁的一代青春##欧美 R&B/Soul 90后 ##10009377589##78
荒诞美学｜神秘诡谲°优雅与疯狂##欧美 另类/独立 兴奋 ##9355373057##1026
```

即`歌单名##标签##歌单id##收藏量`，此格式为几个数年前网易云音乐推荐系统项目所处理的歌曲信息格式，例如[netease-music-recommendation](https://github.com/feiyutalk/netease-music-recommendation)、[Music_recommendation](https://github.com/microw/Music_recommendation)等等。

处理结果已上传至`songlist.csv`

