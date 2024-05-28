import scrapy   #导入scrapy 包
 
#使用相对路径从我们刚刚编写的items.py中导入MusicListItem类
from ..items import MusicListItem 
 
#导入深拷贝包，用于在爬取多个页面时保存到pipeline中的歌单信息顺序不会乱，防止出现重复，非常关键
from copy import deepcopy
 
 
class MusicListSpider(scrapy.Spider):
    name = "MusicList"      #必须要写name属性，在pipeline.py中会用到
    allowed_domains = ["music.163.com"]   #设置爬虫爬取范围
    start_urls = ["https://music.163.com/discover/playlist"]  #起始爬取的页面，即歌单第一面
    offset = 0  #自己设置的一个指针，用于记录当前爬取的页码
 
    def parse(self, response):
        #使用.xpath语法来从HTML页面中解析需要的信息
        #获取一页中的全部歌单，保存到liList中
        liList = response.xpath("//div[@id='m-disc-pl-c']/div/ul[@id='m-pl-container']/li")
        
        #对liList中的歌单，一个一个遍历，获取歌单详细页面的信息
        for li in liList:
            itemML = MusicListItem()
            a_href = li.xpath("./div/a[@class = 'msk']/@href").extract_first()
            itemML["SongsListID"]= a_href[13:]
 
            #获取歌单详细页面的Url地址
            Url = "https://music.163.com" + a_href
            itemML["Url"] = Url
            #调用SongsListPageParse来获取歌单详细页面的信息
            yield scrapy.Request(Url, callback=self.SongsListPageParse, meta={"itemML" : deepcopy(itemML)})
 
 
        #爬取下一页
        if self.offset < 37:
            self.offset += 1
            #获取下一页的Url地址
            nextpage_a_url="https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=" + str(self.offset*35)
            print(self.offset ,nextpage_a_url)
            yield scrapy.Request(nextpage_a_url, callback=self.parse)
            print("开始爬下一页")
 
 
    #用于爬取每一个歌单中的详细页面信息
    def SongsListPageParse(self, response):
        cntc = response.xpath("//div[@class='cntc']")
        itemML = response.meta["itemML"]
 
        SongListName = cntc.xpath("./div[@class='hd f-cb']/div/h2//text()").extract_first()
        itemML["SongListName"] = SongListName #获取歌单名
 
        user_url = cntc.xpath("./div[@class='user f-cb']/span[@class='name']/a/@href").extract_first()
        user_id = user_url[14:]
        itemML["AuthorID"] = user_id           #获取歌单创作者id号
 
        time = cntc.xpath("./div[@class='user f-cb']/span[@class='time s-fc4']/text()").extract_first()
        itemML["CreationDate"] = time[0:10]     #获取歌单创建日期
 
        aList = cntc.xpath("./div[@id='content-operation']/a")
        Collection = aList[2].xpath("./@data-count").extract_first()
        itemML["Collection"] = Collection  #获取收藏量
        Forwarding = aList[3].xpath("./@data-count").extract_first()
        itemML["Forwarding"] = Forwarding  #获取转发量
        Comment = aList[5].xpath("./i/span[@id='cnt_comment_count']/text()").extract_first()
        itemML["Comment"] = Comment        #获取评论量
 
        tags = ""
        tagList = cntc.xpath("./div[@class='tags f-cb']/a")
        for a in tagList:
            tags = tags + a.xpath("./i/text()").extract_first() + " "
        itemML["Labels"] = tags
 
        songtbList = response.xpath("//div[@class='n-songtb']/div")
        NumberOfSongs = songtbList[0].xpath("./span[@class='sub s-fc3']/span[@id='playlist-track-count']/text()").extract_first()
        itemML["NumberOfSongs"] = NumberOfSongs
        AmountOfPlay = songtbList[0].xpath("./div[@class='more s-fc3']/strong[@id='play-count']/text()").extract_first()
        itemML["AmountOfPlay"] = AmountOfPlay
        yield itemML  #将爬取的信息传给 pipelines.py