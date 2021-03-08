

import requests

from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.sac.or.kr/site/main/program/schedule#n', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
exhibitions = soup.select('.romantic-slide > div')
links = []
for exhibition in exhibitions:
    link = exhibition.select_one('div > a')['href']
    if link not in links:
        links.append(link)


temp = []
for link in links:
    data = requests.get(link, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('#contents > div.cwa-top.show-view > dl > dt > p.title > span').text
    if title not in temp:
        temp.append(title)