import requests
from bs4 import BeautifulSoup
import os
#
# from bs4 import BeautifulSoup # BeautifulSoup是python处理HTML/XML的函数库，是Python内置的网页分析工具
# import urllib # python自带的爬操作url的库
#
#
# # 该方法传入url,返回url的html的源代码
# def getHtmlCode(url):
#   # 以下几行注释的代码在本程序中有加没加效果一样,但是为了隐藏自己避免被反爬虫可以假如这个伪装的头部请求
#   headers = {
#     'User-Agent': 'Mozilla/5.0(Linux; Android 6.0; Nexus 5 Build/MRA58N) \
#     AppleWebKit/537.36(KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
#   }
#   # 将headers头部添加到url，模拟浏览器访问
#   url = urllib.request.Request(url, headers=headers)
#
#   # 将url页面的源代码保存成字符串
#   page = urllib.request.urlopen(url).read()
#   # 字符串转码
#   page = page.decode('UTF-8')
#   return page
#
#
# # 该方法传入html的源代码，通过截取其中的img标签，将图片保存到本机
# def getImage(page):
#   # 按照html格式解析页面
#   soup = BeautifulSoup(page, 'html.parser')
#   # 格式化输出DOM树的内容
#   print(soup.prettify())
#   # 返回所有包含img标签的列表，因为在Html文件中图片的插入呈现形式是<img src="..." alt=".." /
#   imgList = soup.find_all('img')
#   x = 0
#   # 循环找到的图片列表，注意，这里手动设置从第2张图片开始，是因为我debug看到了第一张图片不是我想要的图片
#   for imgUrl in imgList[1:]:
#     print('正在下载： %s ' % imgUrl.get('src'))
#     # 得到scr的内容，这里返回的就是Url字符串链接，如'https://img2020.cnblogs.com/blog/1703588/202007/1703588-20200716203143042-623499171.png'
#     image_url = imgUrl.get('src')
#     # 这个image文件夹需要先创建好才能看到结果
#     image_save_path = './image/%d.jpg' % x
#     # 下载图片并且保存到指定文件夹中
#     urllib.request.urlretrieve(image_url, image_save_path)
#     x = x + 1
# if __name__ == '__main__':
#   # 指定要爬取的网站
#   url = 'https://image.baidu.com'
#   # 得到该网站的源代码
#   page = getHtmlCode(url)
#   # 爬取该网站的图片并且保存
#   getImage(page)


#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36

kv = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 '}
#请求
def GetHtmlHTML(url, kv):
    try:
        r = requests.get(url, headers = kv)
        r.raise_for_status()  # 不是200报错
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('请求错误')

#分析
def fillPhotList(soup):
    phot_list = []
    tag_mass = BeautifulSoup.find_all(soup, {'img'})
    #print(tag_mass)
    for i in range(len(tag_mass)):
        phot_site = (tag_mass[i].attrs['src'])
        #print(phot_site)
        phot_list.append(phot_site)
    print(phot_list)
    return phot_list

#查看是否存在文件夹
def file_confirm(matter):
    if not os.path.exists(matter):
        os.makedirs(matter)
        print(f'{matter}创建成功')

#下载保存
def havePhot(photlist, kv, matter, counts):
        for i in range(len(photlist)):
            phot = requests.get(photlist[i], headers = kv)
            with open(f'./{matter}/{matter}+{counts}+{i}.jpg','wb')as f:
                f.write(phot.content)
            # thread_lock.release()
            print(f'{matter}+{counts}+{i}.jpg下载完成')

#主函数
def main():
    matter = input('图片内容')
    counts = int(input('大致需要图片数量')) // 1
    file_confirm(matter)
    for count in range(counts+5):
        url = f"https://cn.bing.com/images/async?q={matter}&first={count*50}&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased_Landscape" \
              "&mmasync=1&dgState=x*0_y*0_h*0_c*7_i*71_r*9&IG=3ABC8EDB67A0437FBDC8BF88BA9B2DCA&SFX=3&iid=images.5602"
        # /images/api/custom/search?q=%e7%83%9f%e5%9b%b1&id=5A178F1359FCBD05C0C8D7A11F54FC09CB8C5C2B&preserveIdOrder=1&count=25&offset=0&skey=7NM_K_lXYXTKAVYeTo0YC6xQSMB1HoIaryOpkywR_Fg&safeSearch=Strict&IG=B8D792518B5E4FFABC7736D75DFE2C86&IID=idpfs&SFX=1
        # url = f"https://cn.bing.com/images/api/custom/search?q={matter}&id=5A178F1359FCBD05C0C8D7A11F54FC09CB8C5C2B&preserveIdOrder=1&count=25&offset=0&skey=7NM_K_lXYXTKAVYeTo0YC6xQSMB1HoIaryOpkywR_Fg&safeSearch=Strict&IG=B8D792518B5E4FFABC7736D75DFE2C86&IID=idpfs&SFX=1"
        html = GetHtmlHTML(url, kv)
        soup = BeautifulSoup(html, 'lxml')
        photList = fillPhotList(soup)
        havePhot(photList, kv, matter,count)


main()


#


