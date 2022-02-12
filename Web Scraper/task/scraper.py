import os
import string

import requests

from bs4 import BeautifulSoup


# Stage 5/5: Soup, Sweet Soup
def url_search():
    page = int(input())
    article_type = input()
    
    for i in range(1, page + 1):
        r = requests.get('https://www.nature.com/nature/articles',
                         params={'searchType': 'journalSearch', 'sort': 'PubDate',
                                 'year': '2020', 'page': i})
        
        url = r.url
        parent_directory = os.getcwd()
        directory_name = f'Page_{i}'
        path = os.path.join(parent_directory, directory_name)
        os.mkdir(path)
        search_article(url, article_type, path)
    return


def search_article(url, type_, directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles_list = soup.find_all('article')
    saved_articles = []
    for i in articles_list:
        try:
            article_type = i.find('span', class_='c-meta__type').text
            if article_type == type_:
                link = i.find('a').get('href')
                article_url = f'https://www.nature.com{link}'
                saved_articles.append(save_content(article_url, directory))
        except AttributeError:
            continue
    return


def save_content(url, directory):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('title').text
    file_title = f'{rename(title)}.txt'
    content = soup.find('div', class_='c-article-body').text.strip()
    os.chdir(directory)
    with open(file_title, 'wb') as file:
        file.write(bytes(content, encoding='UTF-8'))
    return file_title


def rename(name):
    punctuation = string.punctuation + '’'
    for i in name:
        if i in punctuation:
            if i is not name[-1]:
                name = name.translate(name.maketrans(i, ' '))
            else:
                name = name.strip(i)
    name = name.translate(name.maketrans(' ', '_'))
    return name


url_search()
