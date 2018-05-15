from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import re
import os

# 클리닝 함수
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#,$%&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text

# 크롤링 함수
def crowling(writer):
    #f = open('./data/navernews_data.csv', 'a', encoding='utf-8', newline='')
    #wr = csv.writer(f)

    # chromedriver 경로 설정
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.implicitly_wait(3)

    section = {"정치" : 100, "경제":101, "사회":102,"생활/문화":103,"세계":104,"IT/과학":105}
    for key in section.keys():
        # chrome으로 네이버 뉴스 접속
        driver.get("http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=" + str(
            section[key]) + "&date=20180516")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        notices = soup.select('li > div.ranking_text > div.ranking_headline > a')

        for i in range(1):
            driver.find_element_by_link_text(notices[i].text).click()
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(2)
            title = soup.select_one('#articleTitle').text
            content = soup.select_one("#articleBodyContents")
            output = ""
            for text in content.contents:
                stripped = str(text).strip()
                if stripped == "":
                    continue
                if stripped[0] not in ["<", "/"]:
                    output += str(text).strip()
            output.replace("&apos;", '')
            content = output.replace("본문 내용TV플레이어", '')
            title = clean_text(title)
            content = clean_text(content)
            writer.writerow({"title":title,"content":content})
            driver.back()
            time.sleep(2)

#파일 쓰기
def csv_writer():
    if os.path.exists('./data/navernews_data.csv'):
        with open('./data/navernews_data.csv', 'a', encoding='utf-8',newline='') as csvfile:
            fieldnames = ['title', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            crowling(writer)
    else:
        with open('./data/navernews_data.csv', 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['title', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            crowling(writer)

csv_writer()