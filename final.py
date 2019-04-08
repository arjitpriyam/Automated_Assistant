import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pyglet
import time,os
import nltk.data
from urllib.request import urlopen
import vlc
import pafy
import playsound


v_link =""
search_item="Shahrukh khan wikipedia"
final_data=""
def stt():
    r = sr.Recognizer()
    playsound.playsound("unsure.mp3",True)
    with sr.Microphone() as source:
        print("Speak Anything")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print ("Done!")

        try:
            global search_item
            search_item= r.recognize_google(audio)
        except:
            print("Sorry Could not get you")

def find_weather():
    global search_item
    search_item = search_item.split(' ')
    city = search_item[-1]
    api_address = 'https://api.openweathermap.org/data/2.5/weather?appid=afa3ebada3c264c1ca0e9c048462837f&q='
    url = api_address+city
    json_data = requests.get(url).json()
    formatted_data = (json_data['main']['temp']) - 273.15
    global final_data
    final_data="The temperature in {} is {} degree Celcius".format(city,formatted_data)


def search():
    global search_item
    url = "https://www.google.co.in/search?q=" + search_item
    tokenizer = nltk.data.load('english.pickle')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    for match in soup.find_all('div', class_="hJND5c"):
        match = match.text
        expected = 'wikipedia'
        if (expected in match):
            if ('CachedSimilar' in match):
                part = match.split('CachedSimilar')
                new_url = part[0]
            else:
                new_url=match
            response = requests.get(new_url)
            soup = BeautifulSoup(response.text, "lxml")
            for data in soup.find_all('div', class_="mw-parser-output"):

                for final in data.find_all('p', class_=''):
                    for unwanted in final.find_all('sup'):
                        unwanted.decompose()
                    final = final.text
                    final=list(tokenizer.tokenize(final))
                    global final_data
                    final_data = final[0]
                    print(final_data)
                    break
                break
        #else:
        #    final_data= "Sorry I could not find anything on the internet"

def news():
    news_url = "https://news.google.com/news/rss"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    final_news = []
    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item",limit=5)
    for news in news_list:
        print(news.title.text)
        final_news.append(news.title.text)
    global final_data
    final_data = ''.join(final_news)

def music():
    global final_data
    final_data="What song do you want to play"
    tts()
    stt()
    global search_item
    print(search_item)
    song_name = search_item
    search_item=""
    url = "https://www.youtube.com/results?search_query="
    final_url = '{}{}'.format(url, song_name)
    response = requests.get(final_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vid = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'}, limit=1)
    for v in vid:
        v_link = 'https://www.youtube.com' + v['href']
    print(v_link)
    video = pafy.new(v_link)
    best = video.getbestaudio()
    play_url = best.url

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(play_url)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    time.sleep(1.5)
    duration = player.get_length() / 1000
    time.sleep(duration)

def remember():
    global search_item
    search_item="What do you want me to remember?"
    tts()
    stt()
    with open("remem.txt",'a') as f:
        f.write(search_item)
        f.write("\n")

def retrieve():
    print("Into retrieve function")
    global final_data
    if os.path.exists("remem.txt"):
        with open("remem.txt","r") as f:
            final_data=f.read()
    else:
        final_data = "Sorry I do not remember anything"

def forget():
    if os.path.exists("remem.txt"):
        os.remove("remem.txt")
    else:
        global final_data
        final_data=" Sorry I do not remember anything"

def tts():
    file=gTTS(text=final_data,lang="en")
    filename = 'temp.mp3'
    file.save(filename)

    music = pyglet.media.load(filename,streaming=False)
    music.play()

    time.sleep(music.duration)
    os.remove(filename)



#stt()
if "weather" in search_item:
    print("In weather")
    find_weather()
elif "news" in search_item:
    print("In News")
    news()
elif "song" in search_item:
    print("In song")
    music()
elif "remember" and "this" in search_item:
    print("In remember")
    remember()
elif "remember" and "tell me" in search_item:
    print("In Tell")
    retrieve()
elif "remember" and "forget" in search_item:
    print("In Forget")
    forget()
else:
    print("In Search:" + search_item)
    search()

#tts()
