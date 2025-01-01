import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")  # Loaded from environment

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(15)
    finally:
        pygame.mixer.quit()
        os.remove("temp.mp3")

def aiProcess(command):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Used environment
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Nova."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error with AI processing: {str(e)}"

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Song '{song}' not found in library.")
    elif "news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles[:5]:  # Limit to 5 articles
                    speak(article['title'])
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            speak(f"Error fetching news: {str(e)}")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    mic_index = 1  
    print("Available microphones:", sr.Microphone.list_microphone_names())
    recognizer = sr.Recognizer()

    speak("Initializing Nova...")
    while True:
        try:
            with sr.Microphone(device_index=mic_index) as source:
                # Listen for wake word
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word...")
                try:
                    audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
                    word = recognizer.recognize_google(audio)
                    print(f"Recognized wake word: {word}")
                    if "hello" in word.lower():  
                        speak("Yes, how can I help?")
                        
                        # Listen for the actual command
                        print("Listening for command...")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
                        try:
                            command = recognizer.recognize_google(audio)
                            print(f"Recognized command: {command}")
                            processCommand(command)  # Handle the command
                        except sr.UnknownValueError:
                            print("Sorry, I didn't catch the command.")
                            speak("Sorry, I didn't catch that. Please repeat.")
                        except sr.RequestError as e:
                            print(f"Google Speech Recognition error: {e}")
                            speak("There was an error with speech recognition.")
                except sr.UnknownValueError:
                    print("Sorry, I didn't catch the wake word.")
                except sr.RequestError as e:
                    print(f"Google Speech Recognition error: {e}")
        except KeyboardInterrupt:
            print("Exiting program...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
