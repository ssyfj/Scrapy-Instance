import scrapy
from scrapy_splash import SplashRequest

from zymkPro.items import ZymkproItem


class ZymkSpider(scrapy.Spider):
    name = 'zymk'
    start_chapter = 700
    allowed_domains = []
    start_urls = ['http://www.zymk.cn/2/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                dont_filter=True)

    def parse(self,response):
        # 获取首页中所有的章节
        Cp_a = response.xpath('//ul[@id="chapterList"]/li') #解析实体
        for cp in Cp_a:
            cp_url = cp.xpath("./a/@href").extract_first()  #获取链接
            cp_title = cp.xpath("./a/text()").extract_first()   #获取文本
            try:
                if int(cp_title.split("话")[0]) < self.start_chapter:
                    continue
            except ValueError:
                print("异常番号")
                continue
            if not cp_url.startswith("http"):
                cp_url = "https://www.zymk.cn/2/%s" % cp_url

            print("+++++++++++++++++++",cp_url)
            yield SplashRequest(url=cp_url,callback=self.parseNextClsPage,
                                args={'timeout': 3600,'wait':1})


    def parseNextClsPage(self,response):
        # 下面是所有章节去查找所有的图片
        xh_img = response.xpath('//img[@class="comicimg"]')
        xh_img_samp = xh_img.xpath("./@src").extract_first()

        ch_name = response.xpath('//div[@id="readEnd"]/div/p/strong/text()').extract_first()
        href_list = xh_img_samp.split(".jpg")
        xh_img_href_list = []

        xh_pages = response.xpath("//select[@class='selectpage']")
        xh_pagesC = xh_pages.xpath("./option[1]/text()").extract_first()

        xh_pagesCount = int(xh_pagesC.split("/")[1][:-1])
        xh_href_form = (href_list[0][:-1]).split("//")[1]

        #新操作
        xh_href_form_l = xh_href_form.split("/")
        xh_href_form_l[0] = "mhpic.xiaomingtaiji.net"
        xh_href_form = "/".join(xh_href_form_l)

        xh_href_latt = href_list[1]

        for i in range(1,xh_pagesCount+1):
            new_img_href= "http://"+xh_href_form+("%d.jpg"%i)+xh_href_latt    #获取所有图片信息
            item_obj = ZymkproItem(title=ch_name, img_url=new_img_href,img_number=i)
            yield item_obj
