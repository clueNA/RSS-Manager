import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os. getenv('DISCORD_TOKEN', '')

# RSS Check Interval (in minutes)
RSS_CHECK_INTERVAL = int(os.getenv('RSS_CHECK_INTERVAL', '5'))

# Database file
DATABASE_FILE = os.getenv('DATABASE_FILE', 'rss_feeds.db')