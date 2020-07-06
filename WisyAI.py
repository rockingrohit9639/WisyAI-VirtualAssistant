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
        r.energy_threshold = 350
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
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("rohitbhatwara1@gmail.com", "password")
    server.sendmail("rohitbhatwara1@gmail.com", to, content)
    server.close()

if __name__ == '__main__':
     # wish_me()
     while 1:
        query = take_command().lower()
     #Logics for tasks
        if 'wikipedia' in query:
            speak("searching wikipedia")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(result)
            speak(result)
        elif 'youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
        elif 'google' in query:
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
        else:
            webbrowser.open(query)





