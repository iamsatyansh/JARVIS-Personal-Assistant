# ==============================================================================
# File: config.py
# Description: Loads and holds the configuration for the JARVIS assistant
#              from environment variables.
# ==============================================================================
import os
from dataclasses import dataclass, field
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

@dataclass
class JarvisConfig:
    """Loads and holds the configuration for the JARVIS assistant."""
    voice: str = os.getenv("ASSISTANT_VOICE", "en-US-AriaNeural")
    wake_words: List[str] = field(default_factory=lambda: os.getenv("ASSISTANT_WAKE_WORDS", "jarvis").split(','))
    
    # API Keys loaded from environment
    api_keys: Dict[str, str] = field(default_factory=lambda: {
        "openweather": os.getenv("OPENWEATHER_API_KEY"),
        "news": os.getenv("NEWS_API_KEY"),
    })

    # Speech Recognition settings
    energy_threshold: int = 400
    pause_threshold: float = 0.8
    phrase_time_limit: int = 7

    # Assistant Behavior
    auto_sleep_timeout: int = 300  # 5 minutes
    context_memory_size: int = 20

    def __post_init__(self):
        """Validates configuration after initialization."""
        if not self.api_keys["openweather"]:
            print("Warning: OPENWEATHER_API_KEY is not set in the .env file. Weather functionality will be disabled.")
        if not self.api_keys["news"]:
            print("Warning: NEWS_API_KEY is not set in the .env file. News functionality will be disabled.")
