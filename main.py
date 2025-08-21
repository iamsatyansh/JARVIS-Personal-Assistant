
# ==============================================================================
# File: main.py
# Description: Main entry point for the Advanced JARVIS AI Assistant.
#              Initializes all components and starts the application.
# ==============================================================================
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
