# ==============================================================================
# File: services/*_service.py (Weather, News, Media, System)
# ==============================================================================
class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, location: str):
        if not self.api_key: raise ServiceUnavailableError("Weather API key not set.")
        params = {"q": location, "appid": self.api_key, "units": "metric"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    raise ServiceUnavailableError(f"Weather API returned status {response.status}")
                data = await response.json()
                return {
                    "location": data["name"],
                    "temperature": round(data["main"]["temp"]),
                    "description": data["weather"][0]["description"],
                }

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/top-headlines"

    async def get_top_headlines(self, count=3):
        if not self.api_key: raise ServiceUnavailableError("News API key not set.")
        params = {'country': 'us', 'apiKey': self.api_key, 'pageSize': count}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    raise ServiceUnavailableError(f"News API returned status {response.status}")
                data = await response.json()
                return data.get("articles", [])

class MediaService:
    async def play_on_youtube(self, query: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._play_blocking, query)

    def _play_blocking(self, query: str):
        logging.info(f"Opening YouTube search for '{query}' in browser.")
        webbrowser.open(f'https://www.youtube.com/results?search_query={query}')

    async def search_web(self, query: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._search_blocking, query)

    def _search_blocking(self, query: str):
        logging.info(f"Opening web search for '{query}' in browser.")
        webbrowser.open(f'https://www.google.com/search?q={query}')

class SystemService:
    async def get_system_info(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_info_blocking)

    def _get_info_blocking(self):
        return {"cpu": psutil.cpu_percent(), "memory": psutil.virtual_memory().percent}
