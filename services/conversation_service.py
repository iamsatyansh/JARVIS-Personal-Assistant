# ==============================================================================
# File: services/conversation_service.py
# ==============================================================================
class ConversationService:
    """Generates human-like, dynamic conversational responses."""
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.templates = {
            "wake_up": ["Systems online. At your service, sir.", "I am here. How may I assist?", "All systems nominal. Ready for your command."],
            "sleep": ["Entering standby mode. Call me if you need anything.", "Acknowledged. Powering down to standby.", "Until next time, sir."],
            "time": ["The current time is {time}, sir.", "It is currently {time}.", "According to my chronometer, the time is {time}."],
            "date": ["Today's date is {date}.", "We are at {date}, sir."],
            "weather": ["The current forecast for {location} indicates {description} with a temperature of {temperature}° Celsius.", "Right now in {location}, it's {temperature}° Celsius with {description}."],
            "news": ["Pulling up the latest headlines for you, sir.", "Here are the top stories at this hour."],
            "joke": ["Of course. Here is one I find amusing: {joke}", "Certainly. {joke}"],
            "confirmation": ["Acknowledged.", "Understood, sir.", "Of course.", "Consider it done."],
            "error": ["My apologies, sir, but I seem to have encountered an internal error.", "I've run into a complication. I'll log the details for diagnostics."],
            "conversation": ["That's an interesting thought, sir.", "I will take that into consideration.", "Is there anything I can assist you with regarding that?"]
        }

    async def generate_response(self, intent: str, data: dict = None) -> tuple:
        templates = self.templates.get(intent, self.templates["conversation"])
        template = random.choice(templates)
        
        emotion_map = {
            "wake_up": "professional", "sleep": "calm", "time": "professional",
            "date": "professional", "weather": "professional", "news": "serious",
            "joke": "happy", "confirmation": "professional", "error": "concerned",
            "conversation": "calm"
        }
        emotion = emotion_map.get(intent, "professional")

        return template.format(**data) if data else template, emotion
