# ==============================================================================
# File: services/intent_parser.py
# Description: Parses user commands to determine intent and extract entities
#              using a rule-based regex approach.
# ==============================================================================
import re
from typing import Tuple, Dict, Any

class IntentParser:
    """Parses user commands to determine intent and extract entities using regex."""

    def __init__(self):
        # Patterns are ordered from more specific to more general
        self.patterns = {
            "search_query": r'\b(search for|google|find|look up)\b(.+)',
            "play_media": r'\b(play)\b(.+)',
            "memory_store": r'\b(remember that|remember|save|store|note)\b(.+)',
            "memory_recall": r'\b(what did i say about|recall|do you remember)\b(.+)',
            "time_query": r'\b(time|clock)\b',
            "date_query": r'\b(date|day|today)\b',
            "weather_query": r'\b(weather|temperature|forecast)\b',
            "news_query": r'\b(news|headlines)\b',
            "system_query": r'\b(system|cpu|battery|performance|status)\b',
            "joke_request": r'\b(joke|funny|laugh)\b',
            "sleep_command": r'\b(sleep|goodbye|bye|exit|stop listening)\b',
        }

    def parse(self, command: str) -> Tuple[str, Dict[str, Any]]:
        """Analyzes a command to find the best matching intent and its entities."""
        command = command.lower().strip()
        for intent, pattern in self.patterns.items():
            match = re.search(pattern, command)
            if match:
                entities = self._extract_entities(intent, match, command)
                return intent, entities
        
        # If no specific intent is matched, it's a general conversation
        return "conversation", {"original_command": command}

    def _extract_entities(self, intent: str, match: re.Match, command: str) -> Dict[str, Any]:
        """Extracts named entities based on the matched intent."""
        entities = {}
        if intent == "weather_query":
            # Simple location extractor; can be improved with NLP libraries
            location_match = re.search(r'\b(in|for)\b\s+([a-z\s]+)', command)
            if location_match:
                entities['location'] = location_match.group(2).strip()
        # These patterns have a capturing group for the main content/query
        elif intent in ["search_query", "play_media", "memory_store", "memory_recall"]:
            entities['query'] = match.group(2).strip()
            
        return entities
