"""
WisyAI - Virtual Assistant
Author - Rohit Saini
Purpose - To Increase my experience
"""

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import json
import requests
from newspaperReader import read_news
from passwordGenerator import password_gen
import pyperclip as pc
import time

url = "http://api.openweathermap.org/data/2.5/weather?appid=e7ab056bcf4fa908ed098789e9ee78d7&q=khurja"
response = requests.get(url)
whether = response.json()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    '''
    Function to speak anthing given as param.
    :param audio:
    :return:
    '''
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    '''
    Function to wish according to time
    :return:
    '''
    hour = int(datetime.datetime.now().hour)
    if hour > 1 and hour < 12:
        speak("Good Morning Dear")
    elif hour == 12:
        speak("Good noon dear")
    elif hour > 12 and hour < 16:
        speak("Good afternoon Dear")
    else:
        speak("good evening dear")

    speak("I am Wisy how may i help you sir")

def take_command():
    '''
    It takes an input from the user using microphone.
    :return: String
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said : {query}\n")
    except Exception as e:
        # print(e)
        print("Please Say That Again...")
        return "None"
    return query

def sendEmail(to, content):
    '''
    Function to send email to someone
    :param to:
    :param content:
    :return: none
    '''
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("rohitbhatwara1@gmail.com", "password")
    server.sendmail("rohitbhatwara1@gmail.com", to, content)
    server.close()

def weather():
    '''
    Function to forecast the weather
    :return: none
    '''
    curr_temp = whether["main"]["temp"]
    city = whether["name"]
    desc = whether["weather"]
    speak("okay")
    speak("The time is" + str(datetime.datetime.now().strftime("%H%M")))
    speak("Current Temperature" + "in" + city  + "is" + str(curr_temp) + "degree kelvin")
    speak("Today there will be " + desc[0]['description'] + "in your city")
    speak("Have a good day")
    speak("Todays news headlines are")
    read_news()


if __name__ == '__main__':
    # Logics for tasks
    wish_me()
    # weather()
    while 1:
        query = take_command().lower()
        if 'wikipedia' in query:
            try:
                speak("searching wikipedia")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                print(result)
                speak(result)
            except Exception as e:
                speak("Sorry sir i could not search this try another things")
        elif 'youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")
        elif 'play music' in query:
            speak("playing music ")
            music_path = "G:\Songs"
            songs = os.listdir(music_path)
            os.startfile(os.path.join(music_path, songs[0]))
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            print(f"Current time is {strTime}")
            speak(f"current time is {strTime}")
        elif 'code editor' in query:
            py_path = "C:\\Users\\C.Tech Computers\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(py_path)
        elif 'send email' in query:
            try:
                print("What should i say ?")
                speak("What should i say")
                content = take_command()
                to = "rohit@anything.com"
                sendEmail(to, content)
                speak("Email has been send")
            except Exception as e:
                print(e)
                speak("Sorry sir i could not send your email at the moment")
        elif 'how are you' in query:
            speak("I am good well thanks and how about you")
        elif 'i am good' in query:
            speak("Okay... How may i help you")
        elif 'generate password' in query:
            speak("yes why not. Please enter the length of password")
            password = password_gen()
            speak("Here is your well secured password. It is also copied to your clipboard you can paste it anywhere")
            print(f"Your Password : {password}")
            pc.copy(password)
        elif 'news headline' in query:
            speak("Here are some latest news headlines from India")
            read_news()
        elif 'who are you' in query:
            speak("Hey I am Wisy. I am A I model designed by Rohit saini. And I am under development.")
        elif 'what can you do' in query:
            speak("Well I am under development but you can try these listed commands")
            print("1. Wikipedia anything\n2. Open YouTube\n3. Open Google\n4. Play Music\n5. Open code editor\n6. Generate a password\n7.Send Email\n7. Read News Healines for today")
            time.sleep(4)
            speak("so what can i do for you")
        elif 'exit' in query:
            speak("Exiting the program hope you liked me")
            exit(0)







