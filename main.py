
# ==============================================================================
# File: main.py
# Description: Main entry point for the Advanced JARVIS AI Assistant.
#              Initializes all components and starts the application.
# ==============================================================================

class JarvisApplication:
    """Main application orchestrator."""
    def __init__(self):
        self.jarvis: Optional[AdvancedJARVIS] = None
        self.db_manager: Optional[DatabaseManager] = None

    async def initialize(self):
        setup_logging()
        config = JarvisConfig()
        
        self.db_manager = DatabaseManager(config.database_path)
        tts_engine = TTSEngine(config.voice_settings)
        speech_recognizer = SpeechRecognizer(config.speech_settings)
        intent_parser = IntentParser()
        health_monitor = HealthMonitor()
        
        self.jarvis = AdvancedJARVIS(
            config, self.db_manager, tts_engine, speech_recognizer, intent_parser, health_monitor
        )

    async def run(self):
        if not self.jarvis:
            raise JarvisError("Application not initialized.")
        
        loop = asyncio.get_running_loop()
        for sig in [signal.SIGINT, signal.SIGTERM]:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))
        
        await self.jarvis.run()

    async def shutdown(self):
        logging.info("Initiating graceful shutdown...")
        if self.jarvis:
            await self.jarvis.shutdown()
        if self.db_manager:
            await self.db_manager.close()
        logging.info("Shutdown complete.")

async def main_entry():
    """Main entry point with setup instructions."""
    print("--- JARVIS AI Assistant Setup ---")
    print("1. Create a file named '.env' in the same directory.")
    print("2. Add your API keys to the .env file, for example:")
    print('   OPENWEATHER_API_KEY="your_key_here"')
    print('   NEWS_API_KEY="your_key_here"')
    print("3. Install required packages: pip install -r requirements.txt")
    print("   (A requirements.txt file should be created with the content below)")
    print("---------------------------------")
    
    app = JarvisApplication()
    try:
        await app.initialize()
        await app.run()
    except JarvisError as e:
        logging.critical(f"A critical JARVIS error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"An unexpected fatal error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    # This block is the entry point of the script.
    # It sets up the asynchronous event loop and starts the application.
    try:
        # asyncio.run() creates a new event loop and runs the main_entry coroutine.
        asyncio.run(main_entry())
    except KeyboardInterrupt:
        # This catches Ctrl+C to allow for a clean exit message.
        print("\nShutdown signal received. Exiting.")
    except Exception as e:
        # This is a final catch-all for any unexpected errors during startup.
        print(f"A fatal error occurred during application startup: {e}")
        sys.exit(1)


''' ----------- or use this ----------
import asyncio
import logging
import sys

from config import JarvisConfig
from database import DatabaseManager
from services.tts_engine import TTSEngine
from services.intent_parser import IntentParser
from jarvis import AdvancedJARVIS
from utils.logger import setup_logging

async def main():
    """Initializes and runs the JARVIS assistant application."""
    # 1. Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting JARVIS application...")

    # 2. Load Configuration
    try:
        config = JarvisConfig()
    except Exception as e:
        logger.critical(f"Failed to load configuration: {e}")
        sys.exit(1)

    # 3. Initialize Core Components
    db_manager = None
    try:
        db_manager = DatabaseManager()
        tts_engine = TTSEngine(voice=config.voice)
        intent_parser = IntentParser()

        # 4. Initialize JARVIS with injected dependencies
        jarvis = AdvancedJARVIS(config, db_manager, tts_engine, intent_parser)

        # 5. Run the main assistant loop
        await jarvis.run()

    except Exception as e:
        logger.critical(f"A fatal error occurred during initialization or runtime: {e}", exc_info=True)
    finally:
        if db_manager:
            db_manager.close()
        logger.info("JARVIS application has shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown signal received. Exiting gracefully.")
    except Exception as e:
        print(f"An unexpected error forced the application to stop: {e}")
        '''
