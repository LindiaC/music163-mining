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

### 按歌单列举歌曲

相关文件：`Songlist2Songs.py`

相关API：`/playlist/detail?id=`，`/song/detail?id=`

本文件实现功能：读取当前目录下指定csv（以`MusicList_2024-05-28T02-23-05.csv`为例），对于每一行的歌单id与API接口组合为url，获取到歌单下歌曲id，再将歌曲id与API接口组合为url，提取有用字段整理成如下格式，写入当前目录下的`songlist2songs.txt`：

```
欧美R&B入坑曲：封神旋律 是谁的一代青春##欧美 R&B/Soul 90后 ##10009377589##78	2772113::I wanted you::Ina Wroldsen::100	5100462::Dilemma::Nelly|Kelly Rowland::100	28718313::The Way I Still Love You::Reynard Silva::100	518904648::Paris in the Rain::Lauv::100	1786865::Because Of You::Ne-Yo::100	1571835::Call You Tonight::Johnta Austin::100	461544117::Starboy::The Weeknd|Daft Punk::100	29133008::Before You Break My Heart::Stevie Hoang::100	479223413::I Like Me Better::Lauv::100	29412405::In The Shadow Of The Sun::Professor Green::100	18513043::Love you like I do::Jamillions::100	431610014::Starboy::The Weeknd|Daft Punk::100	1830419924::Peaches::Justin Bieber|Daniel Caesar|Giveon::100	17793578::Be On You::Flo Rida|Ne-Yo::100	2051548110::Nothin' on Me::Leah Marie Perez::100	1934649::Shape Of My Heart::Sting::100	1955978156::Shut up My Moms Calling::Hotel Ugly::100	1420972635::Come Around Me::Justin Bieber::100	544199008::Done for Me (feat. Kehlani)::Charlie Puth|Kehlani::100	1985237093::24 Hours::Anthony Russo::100	1320329379::Talk Dirty::Jason Derulo::100	1786869::So Sick::Ne-Yo::100	19827042::Call You Tonight::Whitney Houston::100	1909814194::Every summertime::Jerry1::100	37955047::BLUE::Troye Sivan|Alex Hope::100	29758362::Trouble I'm In::Twinbed::100	1928397447::sun and moon::Anees::100	1318733599::Sunflower::Post Malone|Swae Lee::100	442867526::Die For You::The Weeknd::100	1369602061::double take::Dhruv::100	26643898::Billie Jean (Extended)::Michael Jackson::100	1774229::The One::Matt Cab::95	2058139099::One Of The Girls::The Weeknd|JENNIE|Lily-Rose Depp::100	29950374::Shy::Jai Waetford::100	1325449675::i swear i'll never leave again::keshi::100	35301130::One Last Time::Ariana Grande::100
```

每行第一组为歌单信息，后续为歌单对应歌曲信息，格式同前文，一个歌单内每组信息之间用`\t`分隔。歌曲歌手数量大于1时，用`|`分隔。

处理结果已上传至`songlist2songs.txt`

## 数据挖掘

参考了[netease-music-recommendation](https://github.com/feiyutalk/netease-music-recommendation)、[Music_recommendation](https://github.com/microw/Music_recommendation)

### 使用Music Recommend System 

运行`Music Recommend System.ipynb`，可以查找和一个歌单(user)最接近的10个歌单(user)，以及不同算法的评估。

### 根据若干首歌推荐相似的前10首歌

运行`Music Recommend System.ipynb`，后面部分代码，结果存放于result.txt里。

## 用户界面

相关文件：`Music_Recommend_UI.py`

使用tkinter编写UI，直接clone仓库内所有内容可确保成功运行。如使用自己数据，请整理好类似的文件格式和结构，或者修改代码中相应路径部分

运行效果视频如下：

<video id="video" controls="" preload="none">
      <source id="mp4" src="demo.mp4" type="video/mp4">
</videos>


