import threading
import time
from bot import DiscordBot
from config import DISCORD_TOKEN

def run_bot():
    """Run Discord bot in separate thread"""
    bot = DiscordBot(DISCORD_TOKEN)
    bot.run()

if __name__ == "__main__":
    # Start Discord bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("🤖 Discord bot started in background")
    print("🌐 Starting Streamlit app...")
    print("💡 Run: streamlit run app.py")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")