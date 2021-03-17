import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


list_ = []


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_="gkInnerInsetLeft").find('div', class_="itemListView")
    products = product_list.find_all('article', class_="itemView groupLeading")

    for product in products:
        try:
            photo = 'https://vesti.kg' + product.find('img').get('src')
        except:
            photo = ''
        try:
            title = product.find('a').get('title')
        except:
            title = ''

        data = {'title': title, 'photo': photo}

        list_.append(data)
    return list_


def main():
    news_url = 'https://vesti.kg/obshchestvo.html'
    news = get_page_data(get_html(news_url))
    return news











