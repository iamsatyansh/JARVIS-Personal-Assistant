# ==============================================================================
# File: core/config.py
# ==============================================================================
load_dotenv()

@dataclass
class VoiceSettings:
    """Voice and TTS related settings."""
    voice: str = os.getenv("ASSISTANT_VOICE", "en-US-AriaNeural")
    emotion_modulation: bool = True

@dataclass
class SpeechSettings:
    """Speech recognition settings."""
    energy_threshold: int = 400
    pause_threshold: float = 0.8
    phrase_time_limit: int = 10
    timeout: float = 5.0

@dataclass
class BehaviorSettings:
    """Assistant behavior settings."""
    auto_sleep_timeout: int = 300
    context_memory_size: int = 20
    health_check_interval: int = 60
    metrics_interval: int = 300

@dataclass
class JarvisConfig:
    """Enhanced configuration manager."""
    voice_settings: VoiceSettings = field(default_factory=VoiceSettings)
    speech_settings: SpeechSettings = field(default_factory=SpeechSettings)
    behavior: BehaviorSettings = field(default_factory=BehaviorSettings)
    
    api_keys: Dict[str, str] = field(default_factory=lambda: {
        "openweather": os.getenv("OPENWEATHER_API_KEY"),
        "news": os.getenv("NEWS_API_KEY"),
    })
    
    wake_words: List[str] = field(default_factory=lambda: 
        [w.strip() for w in os.getenv("ASSISTANT_WAKE_WORDS", "jarvis").split(',')]
    )
    
    default_location: str = os.getenv("DEFAULT_LOCATION", "Ludhiana")
    database_path: str = os.getenv("DATABASE_PATH", "data/jarvis_memory.db")

    def __post_init__(self):
        if not self.api_keys["openweather"]:
            print("Warning: OPENWEATHER_API_KEY is not set. Weather features will be disabled.")
        if not self.api_keys["news"]:
            print("Warning: NEWS_API_KEY is not set. News features will be disabled.")
