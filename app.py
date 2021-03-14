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
        duration = soup.select_one('#contents > div.cwa-top.show-view > dl > dt > ul > li:nth-child(1) > span:nth-child(2)').text.strip()
        temp = {'title': url_title, 'img': url_image, 'duration': duration}
        exhibition_list.append(temp)

    return jsonify({'result': 'success', 'exhibition': exhibition_list})

@app.route('/open_arte_museum')
def open_arte_museum():
    return render_template('arte_museum.html')

@app.route('/arte_museum', methods=['GET'])
def arte_museum():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://artemuseum.com/', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    exhibitions = soup.select('#s2020090711366db0dfcc7 > main > div:nth-child(4) > div > div > div > div > div > div')

    exhibition_list = []
    for exhibition in exhibitions:
        title = exhibition.select_one('#container_w2020090801b6efdb353b6 > div > div > h4').text.strip()
        image = exhibition.select_one('#gal_item_ > img')['data-original']

        temp = {'title': title, 'image': image}

        exhibition_list.append(temp)

    return jsonify({'result': 'success', 'exhibition': exhibition_list})
#gal_item_ > img

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
