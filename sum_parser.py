import requests
from bs4 import BeautifulSoup


base_url = 'http://sum.in.ua/?swrd='
word = 'шевченко'

def parsing(word):
    url = base_url + word
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find_all('div', id='article')
    result = ''
    if len(article) == 0:
        article = soup.find('div', id='search-res')
        result = article.find('p').text.replace('Можливо, стануть у пригоді: ', '').replace('Можливо, ви шукали:', '')
        result = result.replace('Можливо, вас зацікавить:', '')
    else:
        for i in article:
            for j in i.find_all('p'):
                if j.attrs == {'class': ['tom', 'comm']}:
                    pass
                else:
                    result += str(j.text + '\n\n')

    return result


if __name__ == '__main__':
    print(parsing(word))
