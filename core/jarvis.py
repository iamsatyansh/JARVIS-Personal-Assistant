class AdvancedJARVIS:
    """Enhanced JARVIS AI assistant orchestrator."""
    def __init__(self, config: JarvisConfig, db_manager: DatabaseManager, tts_engine: TTSEngine, 
                 speech_recognizer: SpeechRecognizer, intent_parser: IntentParser, health_monitor: HealthMonitor):
        self.config = config
        self.db_manager = db_manager
        self.tts_engine = tts_engine
        self.speech_recognizer = speech_recognizer
        self.intent_parser = intent_parser
        self.health_monitor = health_monitor
        self.is_active = False
        self.is_running = True
        self.last_activity_time = time.time()
        self.conversation_service = ConversationService(config)
        self.metrics = MetricsCollector()
        
        self.weather_service = WeatherService(config.api_keys.get("openweather"))
        self.news_service = NewsService(config.api_keys.get("news"))
        self.media_service = MediaService()
        self.system_service = SystemService()
        
        self.circuit_breakers = {
            "weather": CircuitBreaker(expected_exception=ServiceUnavailableError),
            "news": CircuitBreaker(expected_exception=ServiceUnavailableError),
        }

        self.intent_handlers = {
            "time_query": self._handle_time_request, "date_query": self._handle_date_request,
            "weather_query": self._handle_weather_request, "search_query": self._handle_search_request,
            "play_media": self._handle_media_request, "news_query": self._handle_news_request,
            "system_query": self._handle_system_info, "joke_request": self._handle_joke_request,
            "sleep_command": self._go_to_sleep, "conversation": self._handle_conversation,
            "health_check": self._handle_health_check,
        }

    async def run(self):
        await self.speech_recognizer.initialize()
        await self._speak(*await self.conversation_service.generate_response("wake_up"))
        
        background_tasks = [asyncio.create_task(self._health_check_loop())]

        try:
            while self.is_running:
                command = await self.speech_recognizer.listen()
                if command:
                    await self._process_command(command)
                await self._check_auto_sleep()
        finally:
            for task in background_tasks:
                task.cancel()
            await asyncio.gather(*background_tasks, return_exceptions=True)

    async def _process_command(self, command: str):
        self.last_activity_time = time.time()
        if not self.is_active:
            if any(word in command for word in self.config.wake_words):
                await self._wake_up()
            return

        start_time = time.time()
        intent, entities = await self.intent_parser.parse(command)
        handler = self.intent_handlers.get(intent)
        
        if handler:
            await handler(entities)
            self.metrics.record_command_processing(intent, time.time() - start_time, True)
        else:
            logging.warning(f"No handler for intent: {intent}")
            await self._speak(*await self.conversation_service.generate_response("error"))
            self.metrics.record_command_processing(intent, time.time() - start_time, False)

    async def _speak(self, text: str, emotion: str):
        try:
            await self.tts_engine.speak(text, emotion)
        except Exception as e:
            logging.error(f"TTS engine failed: {e}")
            print(f"JARVIS (audio failed): {text}")

    async def _wake_up(self):
        self.is_active = True
        self.last_activity_time = time.time()
        await self._speak(*await self.conversation_service.generate_response("wake_up"))

    async def _go_to_sleep(self, entities=None):
        self.is_active = False
        await self._speak(*await self.conversation_service.generate_response("sleep"))

    async def _check_auto_sleep(self):
        if self.is_active and (time.time() - self.last_activity_time > self.config.behavior.auto_sleep_timeout):
            await self._go_to_sleep()

    async def _health_check_loop(self):
        while self.is_running:
            await self.health_monitor.check_system_health()
            await asyncio.sleep(self.config.behavior.health_check_interval)
            
    async def _handle_time_request(self, entities):
        now = datetime.now()
        await self._speak(*await self.conversation_service.generate_response("time", {"time": now.strftime("%I:%M %p")}))

    async def _handle_date_request(self, entities):
        now = datetime.now()
        await self._speak(*await self.conversation_service.generate_response("date", {"date": now.strftime("%A, %B %d, %Y")}))

    async def _handle_weather_request(self, entities):
        location = entities.get('location', self.config.default_location)
        try:
            weather_data = await self.circuit_breakers["weather"].call(self.weather_service.get_weather, location)
            await self._speak(*await self.conversation_service.generate_response("weather", weather_data))
        except (ServiceUnavailableError, CircuitBreakerOpenError) as e:
            logging.error(e)
            await self._speak("The weather service is currently unavailable, sir. Please try again later.", "concerned")

    async def _handle_news_request(self, entities):
        await self._speak(*await self.conversation_service.generate_response("news"))
        try:
            articles = await self.circuit_breakers["news"].call(self.news_service.get_top_headlines)
            for article in articles:
                await self._speak(article['title'], "serious")
        except (ServiceUnavailableError, CircuitBreakerOpenError) as e:
            logging.error(e)
            await self._speak("I'm unable to fetch the news at this moment, sir.", "concerned")

    async def _handle_search_request(self, entities):
        query = entities.get('query')
        if not query: return
        await self._speak(f"Searching for {query}, one moment.", "professional")
        await self.media_service.search_web(query)

    async def _handle_media_request(self, entities):
        query = entities.get('query')
        if not query: return
        await self._speak(f"Of course, playing {query} for you now.", "happy")
        await self.media_service.play_on_youtube(query)

    async def _handle_joke_request(self, entities):
        joke = pyjokes.get_joke()
        await self._speak(*await self.conversation_service.generate_response("joke", {"joke": joke}))

    async def _handle_conversation(self, entities):
        await self._speak(*await self.conversation_service.generate_response("conversation"))

    async def _handle_health_check(self, entities):
        health = await self.system_service.get_system_info()
        response = f"All systems are functioning within normal parameters, sir. CPU is at {health['cpu']}% and memory is at {health['memory']}%."
        await self._speak(response, "professional")

    async def _handle_system_info(self, entities):
        await self._handle_health_check(entities)

    async def shutdown(self):
        self.is_running = False
        if self.is_active:
            await self._speak("JARVIS shutting down. Goodbye, sir.", "calm")
        await self.tts_engine.close()
        await self.speech_recognizer.close()
