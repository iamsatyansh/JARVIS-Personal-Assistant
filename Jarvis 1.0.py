# Importing required libraries
import pyttsx3  # Text-to-speech conversion
import datetime  # Fetch current time and date
import speech_recognition as sr  # Convert speech to text
from time import sleep # Pause execution
import smtplib  # Send emails (currently unused)
import pyautogui  # Automate GUI interactions
import webbrowser as wb  # Open URLs in the browser
import time 
import wikipedia  # Fetch summaries from Wikipedia
import pywhatkit as kit  # Miscellaneous tasks like playing YouTube
from newsapi import NewsApiClient  # Fetch news headlines
import clipboard  # Copy-paste functionality
import os  # Interact with the operating system
import pyjokes  # Get random jokes
import random  # For randomness (e.g., coin flips)
from nltk.tokenize import word_tokenize  # Tokenize sentences into words
import psutil  # Fetch system information like CPU and battery
import requests  # Make HTTP requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 210)  # Set default speaking speed

# Function to make the AI speak
def speak(audio):
    """Converts text to speech and speaks it out."""
    engine.say(audio)
    engine.runAndWait()

# Function to change voice between male and female
def getvoices(voice):
    """Sets the voice of the assistant and speaks a greeting."""
    voices = engine.getProperty('voices')
    if voice == 1:  # Male voice
        engine.setProperty('voice', voices[0].id)
        speak("Hello, this is JARVIS, your personal assistant!")
    elif voice == 2:  # Female voice
        engine.setProperty('voice', voices[1].id)
        speak("Hello, this is FRIDAY!")

# Function to fetch and speak the current time
def get_current_time():
    """Speaks the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}. It's time to get things done, or maybe procrastinate stylishly!")

# Function to fetch and speak the current date
def date():
    """Speaks the current date."""
    now = datetime.datetime.now()
    speak(f"Today's date is {now.day} {now.strftime('%B')} {now.year}. Mark your calendar for greatness—or naps!")    
    

def dynamic_greetings():
    """Generates dynamic, varied greetings based on context."""
    now = datetime.datetime.now()
    hour = now.hour
    day = now.strftime("%A")
    
    # Time-based greetings
    if 6 <= hour < 12:
        base_greeting = "Good morning, Sir! Let's conquer the day!"
    elif 12 <= hour < 18:
        base_greeting = "Good afternoon! The world is your playground today."
    elif 18 <= hour < 23:
        base_greeting = "Good evening, Sir! Let's make this evening legendary."
    else:
        base_greeting = "Burning the midnight oil again, Sir? Let's make it count!"

    # Day-based variations
    day_greetings = {
        "Monday": "It's Monday, Sir! Time to set the tone for the week.",
        "Friday": "TGIF, Sir! The weekend is almost here.",
        "Saturday": "Happy Saturday! Time to relax—or hustle harder.",
        "Sunday": "It's Sunday, Sir! A perfect day for planning or chilling."
    }
    day_greeting = day_greetings.get(day, "")

    # Random witty line
    random_lines = [
        "Let's make some magic happen today.",
        "Remember, Sir: Genius is 1% inspiration and 99% coffee.",
        "Success awaits, Sir! Or at least a really good meme.",
        "Today's a good day to be awesome, Sir.",
        "Let's aim for the stars—or at least avoid procrastination."
    ]
    random_line = random.choice(random_lines)

    # Combine everything
    full_greeting = f"{base_greeting} {day_greeting} {random_line}"
    speak(full_greeting)



# Function to take input via text (console)
def takeCommandCMD():
    """Takes a command input via console."""
    query = input("Please tell me how can I help you?\n")
    return query

# Function to take input via microphone
def takeCommandMic():
    """Listens to the user's voice and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 300
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-IN')
        print(f"You said: {query}")
    except sr.UnknownValueError:
        print("I didn't catch that. Could you please repeat? My ears are on a coffee break.")
        return "None"
    except sr.RequestError:
        print("Sorry, there seems to be an issue with the speech service. Blame the internet gremlins!")
        return "None"
    return query

# Function to send WhatsApp messages
def sendWAmsg(phone_no, message):
    """Sends a WhatsApp message to the specified number."""
    try:
        wb.open(f'https://web.whatsapp.com/send?phone={phone_no}&text={message}')
        sleep(10)  # Allow time for WhatsApp Web to load
        pyautogui.press('enter')  # Send the message
        speak("Message sent successfully. It's like email, but cooler!")
    except Exception as e:
        print(f"Error in sending WhatsApp message: {e}")
        speak("Unable to send the WhatsApp message. Maybe WhatsApp is on a break too!")

# Function to perform Google search
def searchgoogle():
    """Asks the user what to search and opens Google with the query."""
    speak("What should I search for? The answer to life, the universe, and everything?")
    query = takeCommandMic()
    wb.open(f'https://www.google.com/search?q={query}')
    speak(f"Here are the search results for {query}. Enjoy the rabbit hole!")

# Function to fetch and read news
def news():
    """Fetches and reads news headlines on a given topic."""
    try:
        newsapi = NewsApiClient(api_key='')  # Replace with your API key
        speak("What topic do you want to hear about? Cats, politics, or maybe cat politics?")
        topic = takeCommandMic()
        headlines = newsapi.get_top_headlines(q=topic, 
                                              language='en', 
                                              page_size=5)
        for idx, article in enumerate(headlines['articles']):
            speak(f"News {idx + 1}: {article['description']}")
        speak("That's all the news for now. Stay informed—or blissfully ignorant!")
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("I couldn't fetch the news. Maybe the newsroom is taking a coffee break!")

# Function to read text from the clipboard
def text2speech():
    """Reads text from the clipboard and speaks it."""
    text = clipboard.paste()
    if text:
        speak(text)
    else:
        speak("There's nothing copied to the clipboard. Copy something funny next time!")

# Function to flip a coin and add context
def flip_coin():
    speak("You seem indecisive. Let me help. What are the two options you're deciding between?")
    option1 = takeCommandMic()
    speak(f"And the second option?")
    option2 = takeCommandMic()
    result = random.choice([option1, option2])
    speak(f"I flipped the coin, and the result is {result}. No bets, no regrets!")
    speak(f"If it helps, here’s some advice: Choosing {result} could open up exciting possibilities.")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to remember something
def remember_that():
    """Allows the assistant to remember something for the user."""
    speak("What should I remember? Hopefully, it's not your password!")
    data = takeCommandMic()
    with open('data.txt', 'w') as file:
        file.write(data)
    speak(f"Got it! I'll remember that {data}. My memory is better than goldfish memory!")

# Function to recall remembered data
def recall_memory():
    """Recalls what the assistant was asked to remember."""
    try:
        with open('data.txt', 'r') as file:
            data = file.read()
        speak(f"You asked me to remember that {data}. Aren't I a genius?")
    except FileNotFoundError:
        speak("I don't have anything to remember yet. My slate is clean!")

# Function to play YouTube videos
def play_on_youtube():
    """Plays a video on YouTube based on user input."""
    speak("What do you want to play on YouTube? Hopefully, it's not a Rickroll!")
    video = takeCommandMic()
    kit.playonyt(video)
    speak(f"Playing {video} on YouTube. Enjoy the vibes!")

# Function to search Wikipedia
def search_wikipedia():
    """Searches Wikipedia for a query and speaks a summary."""
    speak("What should I search on Wikipedia? Give me something juicy!")
    query = takeCommandMic()
    try:
        result = wikipedia.summary(query, sentences=4)
        speak(f"According to Wikipedia: {result}")
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results for your query. Please be more specific, like Sherlock Holmes specific!")
    except Exception as e:
        speak("I couldn't find anything on Wikipedia for your query. Maybe try simpler words?")

# Function to open a website
def open_website():
    """Opens a website based on user input."""
    speak("Which website should I open? Make it interesting!")
    website = takeCommandMic().replace(" ", "")
    if not website.startswith("http"):
        website = f"http://{website}"
    wb.open(website)
    speak(f"Opening {website}. Don't blame me for the pop-ups!")
    
# Function to provide system information
def system_info():
    """Provides system information like CPU usage and battery status."""
    cpu_usage = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    speak(f"The CPU is currently at {cpu_usage} percent usage. It's working harder than me!")
    if battery:
        speak(f"The battery is at {battery.percent} percent. Keep it charged unless you're feeling daring!")
   
# Function to provide weather updates
def weather():
    """Provides interactive, context-aware weather updates."""
    speak("Please tell me the location for the weather update.")
    location = takeCommandMic()
    try:
        api_key = ''  # Replace with your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response['cod'] == 200:
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            
            # Contextual advice
            if temp < 10:
                advice = "It's freezing out there! Don't forget your jacket—or a hot chocolate."
            elif 10 <= temp < 20:
                advice = "It's a bit chilly. A sweater or light jacket should do the trick."
            elif 20 <= temp < 30:
                advice = "The weather's pleasant. A perfect day for a stroll—or conquering the world."
            else:
                advice = "It's scorching! Stay hydrated and wear something light—like your wit."
            
            if "rain" in desc.lower():
                advice += " Also, it's raining! Don't forget your umbrella."
            elif "snow" in desc.lower():
                advice += " It's snowing, Sir. Time for some snowball fights—or warm cocoa."
            elif "wind" in desc.lower():
                advice += " The wind's strong today. Hold onto your hat—or your dignity."
            
            # Final weather update
            speak(f"The current temperature in {location} is {temp} degrees Celsius with {desc}. {advice}")
        else:
            speak("I couldn't find the weather for that location. Maybe it's off the map!")
    except Exception as e:
        print(f"Error fetching weather: {e}")
        speak("I couldn't fetch the weather. Blame the weather gods—or the internet!")

"""Main execution block to control the assistant."""
if __name__ == "__main__":
    getvoices(1)  # Initialize with JARVIS voice
    wakeword = "jarvis"
    active = False
    last_active_time = None

    while True:
        if not active:
            print("Say the wake word to activate...")
            query = takeCommandMic().lower()
            if wakeword in query:
                active = True
                dynamic_greetings()  # Greet the user
                last_active_time = time.time()
        else:
            # print("Listening for commands...")
            query = takeCommandMic().lower()

            if 'go to sleep' in query:
                speak("Going to sleep now. Wake me up when you need me!")
                active = False
            elif query:
                last_active_time = time.time()  # Reset activity timer
                if 'time' in query:
                    get_current_time()
                elif 'date' in query:
                    date()
                elif 'message' in query:
                    # Example contact list for WhatsApp messaging
                    contacts = {'dad': '1010101010', 'mom': '2020202020'}
                    speak("Whom do you want to message? Your bestie or someone else?")
                    contact = takeCommandMic().lower()
                    if contact in contacts:
                        speak("What should I say? Make it memorable!")
                        message = takeCommandMic()
                        sendWAmsg(contacts[contact], message)
                    else:
                        speak("I don't have that contact saved. Add them to the list and let's chat again!")
                elif 'search' in query:
                    searchgoogle()
                elif 'news' in query:
                    news()
                elif 'read' in query:
                    text2speech()
                elif 'joke' in query:
                    speak(pyjokes.get_joke())
                elif 'flip' in query:
                    flip_coin()
                elif 'remember that' in query:
                    remember_that()
                elif 'do you remember' in query:
                    recall_memory()
                elif 'play' in query:
                    play_on_youtube()
                elif 'wikipedia' in query:
                    search_wikipedia()
                elif 'website' in query:
                    open_website()
                elif 'system' in query:
                    system_info()
                elif 'weather' in query:
                    weather()
                elif 'exit' in query:
                    speak("Goodbye, Sir! May your day be productive—or at least entertaining!")
                    break

            # Check for timeout (e.g., 5 minutes of inactivity)
            if time.time() - last_active_time > 300:
                speak("Im going to sleep due to inactivity. Wake me up when needed!")
                active = False

   
    