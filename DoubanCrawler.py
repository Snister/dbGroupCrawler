# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:21:34 2016

@author: Zhs
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:39:53 2016

@author: Zhs
"""

import requests
import re
import os
import os.path

class DoubanCrawler():
    """ 抓取豆瓣小组的图片
        抓取链接为讨论分页页面
        load_pages()传递参数为抓取页数   
    
    """

    def __init__(self):
        """ 在当前文件夹下新建images文件夹存放抓取的图片 """
        self.homeUrl = "https://www.douban.com/group/haixiuzu/discussion"
        self.pageUrls = []
        self.images = []
        if not os.path.exists('./db_hxz_images'):
            os.mkdir('./db_hxz_images')

    def __load_singlePage(self,pageUrl):
        """ 加载页面 """
        return requests.get(url = pageUrl).content

    def __make_ajax_url(self, No):
        """ 返回ajax请求的url """
        return self.homeUrl + "?start=" + str(No)

    def __load_more(self, maxNo):
        """ 刷新页面 """
        return requests.get(url = self.__make_ajax_url(maxNo)).content
        
    def __save_pages(self, htmlPage):
        """ 保存帖子地址 """
        prog = re.compile(r'href="(\S+\d\/)"\s?title')
        self.pageUrls.extend(prog.findall(htmlPage))
        
    def load_pages(self,num=5):
        """ 从html页面中提取帖子的信息 """
        for i in range(0,num):
            print "加载第{}页".format(i+1)
            self.__save_pages(self.__load_more(i*25))
        return self.images
            
    def __process_data(self, htmlPage):
        """ 从html页面中提取图片信息 """
        #print "=====================" 
        pat = re.compile(r'topic-figure[\s\S]{0,50}(https[\s\S]{0,200}jpg)')
        imgs = pat.findall(htmlPage)
        if imgs == []:
            return None
        for i in range(0,len(imgs)):
            info = {}
            try:
                info['id'] = re.search('p\d{8}.*',imgs[i]).group()
                info['url'] = imgs[i]
                self.images.append(info)
            except :
                print 'img error'

            #print self.images[i]
    def __save_image(self, imageName, content):
        """ 保存图片 """
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def get_image_info(self):
        """ 得到图片信息 """
        pages = self.pageUrls
        if pages == []:
            return None
        for i in range(0,len(pages)):
            self.__process_data(self.__load_singlePage(pages[i]))
            print "提取第{}条记录".format(i)
        return self.images

    def down_images(self):
        """ 下载图片 """
        print "{} image will be download".format(len(self.images))
        for key, image in enumerate(self.images):
            print 'download {0} ...'.format(key)
            try:
                req = requests.get(image["url"])
            except :
                print 'error'
            imageName = os.path.join("./db_hxz_images", image["id"])
            self.__save_image(imageName, req.content)


if __name__ == '__main__':
    hc = DoubanCrawler()
    hc.load_pages(1)
    hc.get_image_info()
    hc.down_images()