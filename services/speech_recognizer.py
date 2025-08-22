# ==============================================================================
# File: services/speech_recognizer.py
# ==============================================================================
class SpeechRecognizer:
    """Enhanced speech recognition service."""
    def __init__(self, settings: SpeechSettings):
        self.settings = settings
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer.energy_threshold = settings.energy_threshold
        self.recognizer.pause_threshold = settings.pause_threshold

    async def initialize(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._calibrate)

    def _calibrate(self):
        with self.microphone as source:
            logging.info("Calibrating for ambient noise, please be quiet...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logging.info("Calibration complete.")

    async def listen(self) -> Optional[str]:
        loop = asyncio.get_running_loop()
        audio = await loop.run_in_executor(None, self._listen_blocking)
        if audio:
            text = await loop.run_in_executor(None, self._recognize_blocking, audio)
            return text
        return None

    def _listen_blocking(self):
        with self.microphone as source:
            try:
                print("Listening...")
                return self.recognizer.listen(
                    source, timeout=self.settings.timeout, phrase_time_limit=self.settings.phrase_time_limit
                )
            except sr.WaitTimeoutError:
                return None

    def _recognize_blocking(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    async def close(self):
        pass
