import os

def getenv(name, default=None):
    return os.getenv(name, default)

# Telegram Core
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
STRING_SESSION = getenv("STRING_SESSION")

# API
YTDLP_API = getenv("YTDLP_API")
YTDLP_KEY = getenv("YTDLP_KEY")

# Bot Info
BOT_NAME = getenv("BOT_NAME", "Captain Music")
OWNER_USERNAME = getenv("OWNER_USERNAME", "captainpapaj1")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "your_support_group")

# Images
START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/34xlvu.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/34xlvu.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://files.catbox.moe/34xlvu.jpg")
QUEUE_IMG_URL = getenv("QUEUE_IMG_URL", "https://files.catbox.moe/34xlvu.jpg")
