# ==============================================================================
# File: jarvis.py
# Description: The core class for the JARVIS AI assistant, handling the main
#              event loop, command processing, and intent routing.
# ==============================================================================
import asyncio
import logging
import speech_recognition as sr
import webbrowser
import datetime
import random
import time
from collections import deque

import pywhatkit as kit
import wikipedia
import requests
import psutil
import pyjokes
from newsapi import NewsApiClient

from config import JarvisConfig
from database import DatabaseManager
from services.tts_engine import TTSEngine
from services.intent_parser import IntentParser

logger = logging.getLogger(__name__)

class AdvancedJARVIS:
    """The core class for the JARVIS AI assistant."""

    def __init__(self, config: JarvisConfig, db_manager: DatabaseManager, tts_engine: TTSEngine, intent_parser: IntentParser):
        self.config = config
        self.db_manager = db_manager
        self.tts_engine = tts_engine
        self.intent_parser = intent_parser
        
        self.is_active = False
        self.last_activity_time = time.time()
        self.conversation_context = deque(maxlen=config.context_memory_size)
        
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = config.energy_threshold
        self.recognizer.pause_threshold = config.pause_threshold
        
        self.news_client = NewsApiClient(api_key=config.api_keys['news']) if config.api_keys['news'] else None
        
        # Intent handler mapping for clean routing
        self.intent_handlers = {
            "time_query": self.handle_time_request,
            "date_query": self.handle_date_request,
            "weather_query": self.handle_weather_request,
            "search_query": self.handle_search_request,
            "play_media": self.handle_media_request,
            "news_query": self.handle_news_request,
            "system_query": self.handle_system_info,
            "joke_request": self.handle_joke_request,
            "memory_store": self.handle_memory_store,
            "memory_recall": self.handle_memory_recall,
            "sleep_command": self.go_to_sleep,
            "conversation": self.handle_conversation,
        }

    async def run(self):
        """The main asynchronous loop for the assistant."""
        await self.tts_engine.speak("JARVIS systems are online. Standing by.", emotion="serious")
        
        loop = asyncio.get_running_loop()
        
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                # Run the blocking I/O in a separate thread to not block the event loop
                text = await self._listen_for_audio(loop)
                if text:
                    self.last_activity_time = time.time()
                    if not self.is_active:
                        if any(wake_word.strip() in text for wake_word in self.config.wake_words):
                            await self.wake_up()
                    else:
                        await self.process_command(text)
                
                # Auto-sleep logic
                if self.is_active and (time.time() - self.last_activity_time > self.config.auto_sleep_timeout):
                    await self.go_to_sleep(silent=False)
                    
            except Exception as e:
                logger.critical(f"An unexpected error occurred in the main loop: {e}", exc_info=True)
                await asyncio.sleep(1) # Prevent rapid-fire errors

    async def _listen_for_audio(self, loop) -> str:
        """Listens for audio in a background thread and returns the recognized text."""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Run the blocking listen() call in a thread pool
                audio = await loop.run_in_executor(
                    None,  # Uses the default thread pool
                    lambda: self.recognizer.listen(source, phrase_time_limit=self.config.phrase_time_limit)
                )

            # Run the blocking recognize() call in a thread pool
            text = await loop.run_in_executor(None, lambda: self.recognizer.recognize_google(audio).lower())
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            # This is common, so we don't log it as an error
            return ""
        except sr.RequestError as e:
            logger.error(f"Google Speech Recognition request failed: {e}")
            return ""
        except Exception as e:
            logger.error(f"An unexpected error occurred in the listening process: {e}")
            return ""

    async def process_command(self, command: str):
        """Processes a command by parsing intent and routing to the correct handler."""
        self.conversation_context.append({"role": "user", "content": command})
        intent, entities = self.intent_parser.parse(command)
        
        handler = self.intent_handlers.get(intent)
        if handler:
            await handler(entities)
        else:
            logger.warning(f"No handler found for intent: {intent}")
            await self.tts_engine.speak("I'm not sure how to handle that request.")

    # --- Wake/Sleep Functions ---
    
    async def wake_up(self):
        """Activates the assistant."""
        self.is_active = True
        logger.info("Wake word detected. JARVIS is active.")
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning, Sir."
        elif 12 <= hour < 18:
            greeting = "Good afternoon, Sir."
        else:
            greeting = "Good evening, Sir."
        await self.tts_engine.speak(f"{greeting} How may I assist you?", emotion="happy")
    
    async def go_to_sleep(self, entities=None, silent=True):
        """Deactivates the assistant."""
        self.is_active = False
        logger.info("Entering sleep mode.")
        if not silent:
            await self.tts_engine.speak("Going to sleep now. Call me if you need anything.", emotion="calm")

    # --- Intent Handlers ---

    async def handle_time_request(self, entities):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        await self.tts_engine.speak(f"The current time is {current_time}.")

    async def handle_date_request(self, entities):
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        await self.tts_engine.speak(f"Today is {current_date}.")

    async def handle_weather_request(self, entities):
        api_key = self.config.api_keys.get("openweather")
        if not api_key:
            await self.tts_engine.speak("The OpenWeatherMap API key is not configured.", emotion="concerned")
            return
            
        location = entities.get('location', 'Phillaur') # Default location
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url).json()
            if response.get("cod") != 200:
                error_message = response.get("message", "an unknown error occurred")
                logger.error(f"Weather API error for {location}: {error_message}")
                await self.tts_engine.speak(f"Sorry, I couldn't get the weather for {location}.")
                return
            
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            await self.tts_engine.speak(f"The weather in {location} is {temp} degrees Celsius with {desc}.")
        except requests.RequestException as e:
            logger.error(f"Weather request failed: {e}")
            await self.tts_engine.speak("I'm having trouble connecting to the weather service.")

    async def handle_search_request(self, entities):
        query = entities.get('query')
        if not query:
            await self.tts_engine.speak("What would you like me to search for?")
            return
            
        await self.tts_engine.speak(f"Searching for {query}.")
        try:
            summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
            await self.tts_engine.speak(f"According to Wikipedia: {summary}")
        except wikipedia.exceptions.PageError:
            await self.tts_engine.speak("I couldn't find a direct match on Wikipedia, but I'll open a web search for you.")
        except wikipedia.exceptions.DisambiguationError:
            await self.tts_engine.speak("That topic is ambiguous. Opening a web search for you.")
        
        webbrowser.open(f'https://www.google.com/search?q={query}')

    async def handle_media_request(self, entities):
        content = entities.get('query')
        if not content:
            await self.tts_engine.speak("What would you like me to play?")
            return
        await self.tts_engine.speak(f"Playing {content} on YouTube.")
        try:
            kit.playonyt(content)
        except Exception as e:
            logger.error(f"Failed to play on YouTube: {e}")
            await self.tts_engine.speak("Sorry, I encountered an error trying to play that on YouTube.")

    async def handle_news_request(self, entities):
        if not self.news_client:
            await self.tts_engine.speak("The News API is not configured.", emotion="concerned")
            return

        await self.tts_engine.speak("Fetching the latest headlines.")
        try:
            headlines = self.news_client.get_top_headlines(country='in', page_size=3)
            articles = headlines.get('articles', [])
            if not articles:
                await self.tts_engine.speak("I couldn't find any top headlines at the moment.")
                return

            for article in articles:
                await self.tts_engine.speak(article['title'], emotion="serious")
        except Exception as e:
            logger.error(f"News request failed: {e}")
            await self.tts_engine.speak("I'm having trouble fetching the news.")
    
    async def handle_system_info(self, entities):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        report = f"System status: CPU at {cpu_percent} percent. Memory at {memory.percent} percent."
        await self.tts_engine.speak(report, emotion="serious")

    async def handle_joke_request(self, entities):
        try:
            joke = pyjokes.get_joke(language='en', category='all')
            await self.tts_engine.speak(joke, emotion="happy")
        except Exception as e:
            logger.error(f"Failed to get a joke: {e}")
            await self.tts_engine.speak("I wanted to tell you a joke, but I seem to have forgotten the punchline.")

    async def handle_memory_store(self, entities):
        content = entities.get('query')
        if not content:
            await self.tts_engine.speak("What should I remember for you?")
            return
        
        self.db_manager.store_memory(content)
        await self.tts_engine.speak(f"I've made a note of that: {content}")

    async def handle_memory_recall(self, entities):
        query = entities.get('query')
        if not query:
            await self.tts_engine.speak("What would you like me to recall?")
            return
        
        memories = self.db_manager.recall_memories(query)
        if not memories:
            await self.tts_engine.speak(f"I don't have any memories about {query}.")
            return
        
        await self.tts_engine.speak(f"Here's what I remember about {query}:")
        for memory in memories:
            await self.tts_engine.speak(memory)

    async def handle_conversation(self, entities):
        # This can be expanded with a more sophisticated NLP model or rule-based system
        responses = [
            "That's interesting. Please tell me more.",
            "I see. How can I help with that?",
            "Understood. What's the next step?",
        ]
        await self.tts_engine.speak(random.choice(responses))
