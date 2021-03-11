from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import requests

from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.komu    # 'komu'라는 이름의 db를 사용합니다. 'komu' db가 없다면 새로 만듭니다.

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/open_seoul_art_center')
def open_seoul_art_center():
    return render_template('seoul_art_center.html')

@app.route('/seoul_art_center', methods=['GET'])
def seoul_art_center():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.sac.or.kr/site/main/program/schedule#n', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # logo = soup.select('#header > div.width-auto > div > div.logo > a > img')
    exhibitions = soup.select('.romantic-slide > div')

    # Extract links and append to the list Links[]
    links = []
    for exhibition in exhibitions:
        link = exhibition.select_one('div > a')['href']
        if link not in links:
            links.append(link)
        else:
            break


    # Inside each link, get title, image, and info (description)
    exhibition_list = []
    for link in links:
        data = requests.get(link, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        og_title = soup.select_one('meta[property="og:title"]')
        url_title = og_title['content']
        og_image = soup.select_one('meta[property="og:image"]')
        url_image = og_image['content'].split(".jpg")[0]
        # title = soup.select_one('#contents > div.cwa-top.show-view > dl > dt > p.title > span').text
        duration = soup.select_one('#contents > div.cwa-top.show-view > dl > dt > ul > li:nth-child(1) > span:nth-child(2)').text.strip()

    #     temp = [title, duration]
    #     # info = soup.select_one('#contents > div.cwa-top.show-view > dl > dt')
    #     # src_exhibition = {'title': title}
    #     # db.exhibition.insert_one(src_exhibition)
        temp = {'title': url_title, 'img': url_image, 'duration': duration}
        # if db.exhibition.find_one(temp):
        #     pass
        # else:
        #     db.exhibition.insert_one(temp)
        exhibition_list.append(temp)
    # result = list(db.exhibition.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'exhibition': exhibition_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
