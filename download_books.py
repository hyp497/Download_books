import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import re
from selenium.webdriver.common.keys import Keys

title = "人教版五年纪数学上册"
url = r'https://mp.weixin.qq.com/s/zHCLBfzakDoR2JgKw3uMpQ'  # 书籍链接
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    "Cookie": "_ga=GA1.2.81785167.1622732031; urs_guid_ops=7b5bb4e0-3d6a-4bae-8c65-d153df5c4e2c; _4c_=fVJNj5swEP0rK59jgr/A5Fa1UtVLb1WPkTEmoGUxsh3YdJX/3hlCstKutBwsz/Obp5n3eCNL50ZyYAXnpShYoZTQO/LsLpEc3oid8JzxOIeBHEiX0hQP+/2yLNlooslOft5bPyY3pv3Qz45aP7tgTo76liIj0jgZ616pDZFyTgdzHm1HdsT6xoEiqzKdlVCnf1BJncN1Cr4523RMlwkpi6ufYvMMD42be+uOS9+kDnuVKN7RzvWnLgGsC4noFJCScQXF0o+NXz42buijseR8lcNFwuUYgwVw9KMDtHbJQPUbr8Ev0aH69y74F/dU4dAeHCN/V8UIZXCtC2FlQRX7hJvcLdsQsHkD6Q2cZhwOLoO3ZsAOCAe4zqbeQ0zkxfQI/Px2/PPrB67KSq1YUWa3AHkuGLnuyOstUc25UrzSCtxNEB8Yk+MHjNA3W7SEi1aqptBUSVFRaeuc1nWlKM9Zq0tjWCvQwlVT5IpxpriuOIjM/V2jZoJLAe1G1jWVhRS0csJS0RotTcFlmWvymKsUZQVz4Z+2zsX0faxp2BTZO1nluITkd7J8LDHNn9jbylJ8XvkWGzr4RZ/82He9/gc=; PODAAC_Drive=YLkNy17mdgiPnrZTjKD2GAAAAA8"
}

all_files = os.listdir('.')
if "{}_url.txt".format(title) not in all_files:

    chrome = webdriver.Chrome(executable_path='E:\download\chromedriver\chromedriver.exe')
    chrome.get(url)
    chrome.maximize_window()

    # 滚动网页到最底端，因为网页是动态加载的，所以必须滚动到最底端才能加载出所有的图片，源码中才能看到图片的url地址，从而可以下载图片
    for i in range(5000):
        try:
            chrome.find_element_by_tag_name('html').send_keys(Keys.DOWN)
            time.sleep(0.01)
        except:
            print('页面到达了底部！')

    time.sleep(3)
    html = chrome.page_source
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup)
    a = soup.find_all('img')
    all_url = []
    ff = open('./{}_url.txt'.format(title), 'w')
    for ss in a:
        img_url = ss.get('data-src')
        if img_url:
            print(img_url)
            all_url.append(img_url)
            ff.write(img_url + '\n')

    ff.close()
    print(len(all_url))
    chrome.close()

####################################下载书籍################################
files = open('./{}_url.txt'.format(title), 'r')

all_url = files.readlines()

for i, url in enumerate(all_url):
    try:
        html = requests.get(url, headers=headers)
        if not os.path.exists('./{}'.format(title)):
            os.makedirs('./{}'.format(title))
        with open('./{}/tupian_{}.jpg'.format(title, i), 'wb') as jpg:
            jpg.write(html.content)
    except:
        print(i, "  ", url, "下载失败")