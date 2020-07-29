from win32com.client import Dispatch
from newsapi import NewsApiClient
import requests
import json
newsapi = NewsApiClient(api_key='93aa36a48c83413ba9553ea1cf609c7f')

def read_headlines(headlines):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(headlines)

def read_news():
    url =  ('http://newsapi.org/v2/top-headlines?country=in&apiKey=93aa36a48c83413ba9553ea1cf609c7f')
    # url = "https://api.breakingapi.com/news?api_key=9C560CC576E24D86904F673A67A2BCB4&type=headlines&locale=hi-IN"
    response = requests.get(url)
    text = response.text
    json_data = json.loads(text)
    for data in range(0, 2):
        read_headlines(json_data['articles'][data]['title'])
