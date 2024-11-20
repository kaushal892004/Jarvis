import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclist
import requests
from gtts import gTTS
import pygame
import os
# from openai import OpenAI
import openai
import hugchat
import google.generativeai as genai

#for Taking input from user as a audio/speach
recognizer = sr.Recognizer()

#used for converting user input to text
engine = pyttsx3.init() 

#for getting latest news article headline we use API of  " https://newsapi.org/ " for News
news_api_key = "enter_yours_key"

#with pyttsx3 module----------------------------------------------------------
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

#---------------------------------------------------------------------------

#with gTTS module----------------------------------------------------------
def speak(text):

    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")     

#---------------------------------------------------------------------------

#let request handled by GeminiAi ----------------------------------------------
def aiProcess(command):
  
    try:
        # Configure the API key
        genai.configure(api_key="add_your_key")

        # Initialize the Generative Model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Define the system message and user message
        system_message = "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."
        user_message = command

        # Concatenate the messages into a single string
        full_prompt = f"System: {system_message}\nUser: {user_message}"

        # Generate content based on the full prompt
        response = model.generate_content(full_prompt)

        # Speak out the response text
        speak(response.text)

        return response.text

   
    except Exception as e:
        # Handle any other errors that occur
            print(f"An unexpected error occurred: {e}")

#---------------------------------------------------------------------------

#for process the request of user --------------------------------------------
def processCommand(c):
    if  "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")  
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/feed/")   
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/") 
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com/")

    elif c.lower().startswith("play"): 
        song = " ".join(c.lower().split(" ")[1:])
        # song = (c.lower().split(" ")[1:])
        link = musiclist.music[song]
        webbrowser.open(link)

    elif "tell me the news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # output = aiProcess(c)
        # speak(output)    
        aiProcess(c)

#---------------------------------------------------------------------------

#main------------------------------------------------------------------------
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=1)
            word = r.recognize_google(audio)
            #listining for 'jarvis' word
            if(word.lower() == "jarvis"):
                speak("how can i help you")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("No Input! {0}".format(e))

#---------------------------------------------------------------------------            
    


