import os
import time
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 创建Chrome浏览器实例
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # 无头模式，不显示浏览器窗口
driver = webdriver.Chrome(options=chrome_options)

# 搜索关键字并获取搜索结果页面
keyword = 'cat'
driver.get('https://www.google.com/imghp')
search_box = driver.find_elements(By.CSS_SELECTOR, 'q')

search_box.send_keys(keyword)
search_box.send_keys(Keys.RETURN)
time.sleep(1) # 等待页面加载

# 获取搜索结果中的所有图片链接并下载
img_urls = []
img_elems = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')
for img_elem in img_elems:
    img_url = img_elem.get_attribute('src')
    if img_url and img_url.startswith('http'):
        img_urls.append(img_url)

if not os.path.exists(keyword):
    os.mkdir(keyword)
for i, img_url in enumerate(img_urls):
    try:
        filename = f'{keyword}/{keyword}_{i}.jpg'
        urlretrieve(img_url, filename)
        print(f'Downloaded {filename}')
    except Exception as e:
        print(f'Failed to download {img_url}: {e}')

# 关闭浏览器
driver.quit()
