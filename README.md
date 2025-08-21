# Advanced JARVIS AI Assistant (Refactored)

This project is a refactored version of a Python-based voice assistant named JARVIS. The new architecture follows modern software engineering principles, ensuring the application is modular, scalable, maintainable, and robust.

## Key Features

- **Voice-Activated**: Listens for a wake word ("Jarvis") to start interactions.
- **Neural Text-to-Speech**: Uses Microsoft Edge's high-quality neural voices for natural-sounding responses.
- **Intent Recognition**: Parses natural language commands to understand user intent.
- **Modular Services**: Includes handlers for:
  - Telling the time and date.
  - Fetching real-time weather information.
  - Searching the web and Wikipedia.
  - Playing music on YouTube.
  - Reading top news headlines.
  - Providing system status (CPU/Memory).
  - Telling jokes.
  - Storing and recalling memories.
- **Professional Architecture**:
  - **Separation of Concerns**: Code is organized into logical modules (`config`, `database`, `services`, `utils`).
  - **Asynchronous Core**: Built on `asyncio` for efficient I/O operations.
  - **Externalized Configuration**: API keys and settings are managed in a `.env` file, not hardcoded.
  - **Dependency Injection**: Core components are decoupled and passed into the main class.
  - **Robust Logging**: Centralized logging for easier debugging.

## Project Structure

```
.
├── .env                  # Local environment variables (API keys, etc.) - DO NOT COMMIT
├── config.py             # Configuration loader class
├── database.py           # SQLite database manager
├── jarvis.py             # Core assistant class with main logic
├── main.py               # Main entry point to run the application
├── README.md             # This file
├── requirements.txt      # Project dependencies
├── services/
│   ├── __init__.py
│   ├── intent_parser.py  # Module for parsing user commands
│   └── tts_engine.py     # Text-to-Speech engine module
└── utils/
    ├── __init__.py
    └── logger.py         # Logging setup utility
```

## Setup and Installation

### 1. Prerequisites

- Python 3.8 or higher.
- `pip` for package installation.
- For Linux systems, you may need to install `portaudio` for `PyAudio`:
  ```bash
  sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
  ```
- For Windows/macOS, `PyAudio` should install its own dependencies.

### 2. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root of the project directory. This file will hold your secret API keys and custom configurations.

Copy the following content into your `.env` file and replace the placeholder values with your actual keys.

```ini
# .env

# --- API Keys ---
# Get a free key from [https://openweathermap.org/](https://openweathermap.org/)
OPENWEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY"
# Get a free key from [https://newsapi.org/](https://newsapi.org/)
NEWS_API_KEY="YOUR_NEWS_API_KEY"

# --- Assistant Configuration ---
# You can find other voice options for Edge TTS online
ASSISTANT_VOICE="en-US-AriaNeural"
# Comma-separated list of wake words
ASSISTANT_WAKE_WORDS="jarvis,hey jarvis,okay jarvis"
```

### 5. Running the Assistant

Once the setup is complete, you can run the assistant from your terminal:

```bash
python main.py
```

The application will initialize, and you will see a "Listening..." message in the console. Say one of the wake words (e.g., "Jarvis") to activate the assistant and start giving commands.

## How to Use

- **Activation**: Say "Jarvis" or "Hey Jarvis".
- **Commands**: After the greeting, speak your command naturally.
  - "What time is it?"
  - "What is today's date?"
  - "What's the weather in London?"
  - "Search for the history of Python programming."
  - "Play the latest song by Queen."
  - "Tell me a joke."
  - "Remember that my favorite color is blue."
  - "What did I say about my favorite color?"
- **Deactivation**: Say "Goodbye" or "Go to sleep". The assistant will also go to sleep automatically after 5 minutes of inactivity.
