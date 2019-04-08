import requests
from bs4 import BeautifulSoup


def search():
    search_item = 'What is java'
    url= "https://www.google.co.in/search?q=" + search_item

    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")

    for match in soup.find_all('div' , class_ = "hJND5c"):
        match=match.text
        expected= 'wikipedia'
        if(expected in match):
            part=match.split(')')
            new_url=part[0]+')'
            response = requests.get(new_url)
            soup = BeautifulSoup(response.text, "lxml")
            for data in soup.find_all('div',class_="mw-parser-output"):

                for final in data.find_all('p', class_=''):
                    for unwanted in final.find_all('sup'):
                       unwanted.decompose()
                    final=final.text
                    print(final)


