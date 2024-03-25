import pytube
import json
import os
import sys
from pytube import YouTube
from urllib import request
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def get_video(url, output):
    try:
        YouTube(url).streams.first().download(output)
        return True
    except Exception:
        return False


def get_metadata(video_id, api_key, output):
    url = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=snippet,contentDetails,statistics,status".format(video_id, api_key)
    res = request.urlopen(url=url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko)"}  # 请求的User-Agent
    req = request.Request(url=url, headers=headers)  # 包装请求对象
    res = request.urlopen(req)  # 发请求
    html = res.read().decode()  # 获取响应内容
    # html = eval(str(html).replace("\n", ""))
    json.dump(html, open(output, "w"), ensure_ascii=False)

    return 0


def move_page(b):
    for x in range(3):
        b.execute_script('window.scrollBy(0,250)')
        sleep(1)


# def get_data(html: str):
#     soup = BeautifulSoup(html, 'lxml')
#     goods_li = soup.select('#J_goodsList>ul>li')
#     for goods in goods_li:
#         price = goods.select_one('.p-price i').text
#         title = goods.select_one('.p-name.p-name-type-2 em').text.replace(' ', '').replace('\n', '')
#         shop = goods.select_one('.p-shop>span>a').text
#
#         shop_data.append([title, price, shop])
#
#     return shop_data


def num_page(num1, b):
    for i in range(num1):
        # 滚动页面
        move_page(b)

        # # 解析数据
        # get_data(b.page_source)
        # # 遇到下一页按钮
        # btn = b.find_element_by_class_name('pn-next')
        # # 点击下一页
        # btn.click()
        sleep(1)
        # 滚动的最后一页
        if i == num1 - 1:
            break


def get_vids():
    driver = Chrome()
    driver.get("https://www.youtube.com/shorts/qAaGSQyeYOA")

    sleep(10)
    data_tmp = []
    number = 0

    for i in range(10000000):
        button = driver.find_element(By.ID, "navigation-button-down")
        button.click()

        # elem = driver.find_element(By.ID, "player-container")
        # print(elem)
        # print(elem.text)

        data_tmp.append({
            "title": driver.title,
            "url": driver.current_url
        })
        print(len(data_tmp))

        if len(data_tmp) == 20:
            print(number)
            json.dump(data_tmp, open("../data/tmp-{}.json".format(str(number)), "w"), ensure_ascii=False)
            number += 1
            data_tmp = []

        sleep(5)


    # data = []
    # num_page(3, b)

    return 0


def collect_data():
    data = set()
    for file in os.listdir("../data/"):
        tmp = json.load(open("../data/"+file, "r"))
        for t in tmp:
            data.add(t["url"])

    data = list(data)
    json.dump(data, open("../data_all/20240322.json", "w"))


if __name__ == "__main__":
    # get_video("https://www.youtube.com/shorts/_7tQmQn_qO0", "test.mp4")
    # get_metadata("_7tQmQn_qO0", "")
    # get_vids()
    # collect_data()

    data = json.load(open("../data_all/20240322.json", "r"))

    if not os.path.exists("../data/metadatas/20240322"):
        os.mkdir("../data/metadatas/20240322")
    if not os.path.exists("../data/videos/20240322"):
        os.mkdir("../data/videos/20240322")

    for tmp in data:
        file_name = tmp.split("/")[-1]
        if not os.path.exists("../data/videos/20240322/{}.mp4".format(file_name)):
            get_video(tmp, "../data/videos/20240322/{}.mp4".format(file_name))
        if not os.path.exists("../data/metadatas/20240322/{}.json".format(file_name)):
            get_metadata(file_name, sys.argv[1], "../data/metadatas/20240322/{}.json".format(file_name))
        print("Done")
        sleep(1)