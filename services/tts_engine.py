# ==============================================================================
# File: services/tts_engine.py
# Description: Handles Text-to-Speech synthesis and playback using Edge-TTS.
# ==============================================================================
import asyncio
import edge_tts
import pygame
import tempfile
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class TTSEngine:
    """Handles Text-to-Speech synthesis and playback using Edge-TTS."""

    def __init__(self, voice: str):
        self.voice = voice
        pygame.mixer.init()

    async def speak(self, text: str, emotion: str = "neutral"):
        """Synthesizes text to speech with emotional modulation and plays it."""
        if not text:
            logger.warning("Speak function called with empty text.")
            return

        voice_params = self._get_emotional_voice_params(emotion)
        communicate = edge_tts.Communicate(
            text,
            self.voice,
            rate=voice_params['rate'],
            pitch=voice_params['pitch'],
            volume=voice_params['volume']
        )

        tmp_filename = ""
        try:
            # Using a context manager for the temporary file ensures it's handled correctly
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_filename = tmp_file.name
            
            await communicate.save(tmp_filename)

            pygame.mixer.music.load(tmp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"TTS Error for text '{text}': {e}", exc_info=True)
            # Fallback to console output if audio fails
            print(f"JARVIS (audio failed): {text}")
        finally:
            # Ensure the mixer is stopped and the file is unlinked
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            if tmp_filename and os.path.exists(tmp_filename):
                os.unlink(tmp_filename)

    def _get_emotional_voice_params(self, emotion: str) -> Dict[str, str]:
        """Returns voice parameters based on emotion."""
        params = {
            "excited": {"rate": "+20%", "pitch": "+40Hz", "volume": "+10%"},
            "calm": {"rate": "-10%", "pitch": "-20Hz", "volume": "-5%"},
            "concerned": {"rate": "-5%", "pitch": "-10Hz", "volume": "+0%"},
            "happy": {"rate": "+10%", "pitch": "+20Hz", "volume": "+5%"},
            "serious": {"rate": "-15%", "pitch": "-30Hz", "volume": "+0%"},
            "neutral": {"rate": "+0%", "pitch": "+0Hz", "volume": "+0%"}
        }
        return params.get(emotion, params["neutral"])
