![RSS-Manager](https://socialify.git.ci/clueNA/RSS-Manager/image?font=Raleway&language=1&name=1&owner=1&pattern=Transparent&stargazers=1&theme=Dark)
# 📡 RSS Feed to Discord Integration

Automatically post RSS feed updates to Discord channels with a Streamlit feed management interface.

## 🌟 Features

### Core Features
- ✅ **Streamlit Web Interface** - Clean, simple UI to manage all RSS feeds
- ✅ **Single Discord Bot** - One bot handles all feeds and channels
- ✅ **Instant Channel Creation** - Channels are created immediately when you add a feed (within 2 seconds)
- ✅ **Automatic Feed Monitoring** - Checks all RSS feeds every 5 minutes for new content
- ✅ **Rich Discord Embeds** - Beautiful embedded messages with:
  - Article title (required)
  - Direct link to article (required)
  - Author name (if available)
  - Article summary/description
  - Publication date
  - Thumbnail image (if available)
  - Source attribution
- ✅ **Multiple RSS Feeds** - Handle unlimited RSS feeds simultaneously
- ✅ **Feed-Specific Channels** - Each feed gets its own dedicated Discord channel
- ✅ **Smart Routing** - New articles only post to their respective feed channel

### Technical Features
- ✅ **Duplicate Prevention** - Uses MD5 hashing to track and prevent duplicate posts
- ✅ **Sanitized Channel Names** - Automatically converts feed titles to valid Discord channel names
  - Lowercase conversion
  - Special character removal
  - Unique naming (adds numbers if conflicts exist)
  - Max 100 character limit
- ✅ **Error Handling**
  - Validates RSS feeds before adding
  - Handles invalid/malformed feeds gracefully
  - Network error recovery
  - Permission error handling
  - Logs errors without crashing
- ✅ **SQLite Database** - Persistent storage for feeds and seen posts
- ✅ **HTML Cleaning** - Removes HTML tags from RSS content
- ✅ **Flexible Feed Support** - Works with various RSS/Atom feed formats

### User Experience
- 🎨 Simple one-field input interface
- 📊 Live feed list with statistics
- 🗑️ Easy feed removal
- 📺 Channel name preview before creation
- ⚡ Real-time updates
- 💾 Persistent data across restarts

---

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Discord Bot Setup](#discord-bot-setup)
- [Configuration](#configuration)
- [Deployment](#deployment)
  - [Local Development](#local-development)
  - [Linux Server Deployment](#linux-server-deployment)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Deployment](#cloud-deployment)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Example RSS Feeds](#example-rss-feeds)
- [FAQ](#faq)

---

## 🔧 Requirements

- Python 3.8 or higher
- Discord account with server admin permissions
- Server or computer to run the bot 24/7
- Internet connection

---

## 📥 Installation

### 1. Clone or Download the Project

```bash
# Create project directory
mkdir rss-discord-bot
cd rss-discord-bot

# Copy all project files to this directory
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `discord.py` - Discord bot framework
- `streamlit` - Web interface framework
- `feedparser` - RSS/Atom feed parser
- `python-dotenv` - Environment variable management
- `aiohttp` - Async HTTP client

---

## 🤖 Discord Bot Setup

### Step 1: Create Discord Application

1. Go to [Discord Developer Portal](https://discord. com/developers/applications)
2. Click **"New Application"**
3. Enter a name (e.g., "RSS Feed Bot")
4. Click **"Create"**

### Step 2: Create Bot User

1. In your application, go to **"Bot"** section in the left sidebar
2. Click **"Add Bot"**
3.  Click **"Yes, do it!"** to confirm
4. Under the bot's username, click **"Reset Token"**
5. Click **"Yes, do it!"** and copy the token
6. **⚠️ IMPORTANT:** Save this token securely - you'll need it for configuration

### Step 3: Configure Bot Permissions

1. Still in the **"Bot"** section, scroll to **"Privileged Gateway Intents"**
2. Enable these intents:
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent** (optional but recommended)
   - ✅ **Presence Intent** (optional)

### Step 4: Generate Invite Link

1. Go to **"OAuth2"** → **"URL Generator"** in the left sidebar
2. Under **"Scopes"**, select:
   - ✅ `bot`
3. Under **"Bot Permissions"**, select:
   - ✅ **Manage Channels** (required - to create channels)
   - ✅ **Send Messages** (required - to post updates)
   - ✅ **Embed Links** (required - for rich embeds)
   - ✅ **Read Message History** (optional)
   - ✅ **View Channels** (required)
4. Copy the **Generated URL** at the bottom
5.  Paste the URL in your browser and select your Discord server
6. Click **"Authorize"**

Your bot should now appear offline in your Discord server!

---

## ⚙️ Configuration

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Edit Configuration

Open `.env` in a text editor and configure:

```env
# REQUIRED: Your Discord Bot Token
DISCORD_TOKEN=your_actual_bot_token_here

# OPTIONAL: RSS check interval in minutes (default: 5)
RSS_CHECK_INTERVAL=5

# OPTIONAL: Database file location (default: rss_feeds.db)
DATABASE_FILE=rss_feeds. db
```

**⚠️ Security Warning:** Never share your `. env` file or bot token publicly! 

---

## 📖 Usage

### Adding an RSS Feed

1. Open Streamlit interface (default: `http://localhost:8501`)
2. Enter RSS feed URL in the input field
3. Click **"➕ Add Feed"**
4. Bot will immediately create a Discord channel (within 2 seconds)
5.  Feed monitoring starts automatically

### Viewing Active Feeds

- All active feeds are displayed below the input field
- Shows feed title, URL, channel name, and post count
- Click **"🗑️ Remove"** to delete a feed

### Managing Feeds

- **Remove Feed:** Click the remove button next to any feed
- **View Statistics:** See how many posts have been tracked per feed
- **Channel Names:** Automatically generated from feed titles

### Discord Channels

- Channels are created automatically with sanitized names
- Each channel only receives posts from its associated feed
- Channel topic shows the feed source
- Embeds include clickable links, authors, and summaries

---

## 📁 Project Structure

```
rss-discord-bot/
│
├── app.py                  # Streamlit web interface
│   ├── Input field for RSS URLs
│   ├── Add/remove feed functionality
│   ├── Display active feeds list
│   └── Trigger immediate channel creation
│
├── bot.py                  # Discord bot main logic
│   ├── Bot initialization
│   ├── Event handlers (on_ready)
│   ├── Channel creation (immediate + periodic)
│   ├── Feed monitoring (every 5 min)
│   ├── New feed detection (every 2 sec)
│   └── Embed message sending
│
├── rss_monitor.py          # RSS feed parsing and monitoring
│   ├── Feed parsing with feedparser
│   ├── Post data extraction
│   ├── Duplicate detection (MD5 hash)
│   ├── HTML cleaning
│   └── Error handling
│
├── database. py             # SQLite database operations
│   ├── Database initialization
│   ├── Feed CRUD operations
│   ├── Post tracking
│   ├── Channel name sanitization
│   └── Feed validation
│
├── config.py               # Configuration management
│   ├── Load environment variables
│   ├── Discord token
│   ├── Check interval settings
│   └── Database path
│
├── main.py                 # Combined launcher (optional)
│   └── Run bot + Streamlit together
│
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (YOU CREATE THIS)
├── . env.example            # Environment template
├── run.sh                  # Bash startup script
├── README.md               # This file
└── rss_feeds.db           # SQLite database (auto-created)
```

---

## ⚙️ How It Works

### Feed Addition Flow

```
1. User enters RSS URL in Streamlit
2. Streamlit validates feed with feedparser
3. Database stores feed info
4.  Streamlit creates flag file (create_channel_X.flag)
5. Bot detects flag file within 2 seconds
6. Bot creates Discord channel
7. Bot removes flag file
8. User sees success message
```

### Feed Monitoring Flow

```
1. Bot checks all feeds every 5 minutes
2.  For each feed:
   a. Parse RSS feed with feedparser
   b. Extract entries (posts/articles)
   c. Generate MD5 hash for each entry
   d. Check if hash exists in database
   e. If new:
      - Extract title, link, author, summary
      - Add hash to database
      - Send Discord embed to feed's channel
```

### Channel Naming Process

```
1. Extract feed title from RSS
2. Convert to lowercase
3. Replace special chars with hyphens
4. Remove leading/trailing hyphens
5. Truncate to 100 characters
6. Check for conflicts
7. If conflict, append -1, -2, etc.
8.  Return sanitized name
```

### Duplicate Prevention

```
1. Generate unique ID from post:
   - Try RSS entry. id (GUID)
   - Fallback to entry.link
   - Fallback to title + date
2. Hash ID with MD5
3. Check database for hash
4. Skip if exists, post if new
5. Store hash after posting
```

---

## 🎨 Customization

### Change Feed Check Interval

Edit `. env`:
```env
RSS_CHECK_INTERVAL=10  # Check every 10 minutes
```

Or edit `bot.py`:
```python
@tasks.loop(minutes=10)  # Change from 5 to 10
async def check_feeds():
```

### Modify Embed Appearance

Edit `bot.py` in the `send_post_embed` method:

```python
# Change embed color
embed = discord.Embed(
    title=post['title'],
    url=post['link'],
    color=0xFF5733,  # Change this hex color
    timestamp=post. get('published_date')
)

# Add more fields
embed.add_field(name="📅 Published", value=".. .", inline=True)

# Change footer
embed.set_footer(text=f"📡 {feed_title}", icon_url="...")
```

### Change New Feed Detection Speed

Edit `bot.py`:
```python
@tasks.loop(seconds=5)  # Change from 2 to 5 seconds
async def monitor_new_feeds():
```

### Add Feed Categories

Modify channel creation to use categories:

```python
# In bot.py - get_or_create_channel method
category = discord.utils.get(guild.categories, name="RSS Feeds")
if not category:
    category = await guild.create_category("RSS Feeds")

new_channel = await guild.create_text_channel(
    name=channel_name,
    category=category,  # Add this
    topic=f"RSS feed updates for {channel_name}"
)
```

### Custom Feed Names

Edit `database.py` - modify `sanitize_channel_name`:

```python
def sanitize_channel_name(self, name):
    # Add custom prefix
    name = f"rss-{name}"
    # ...  rest of function
```

---

## 🔍 Troubleshooting

### Bot Not Starting

**Error:** `discord.errors.LoginFailure: Improper token has been passed`

**Solution:**
- Check `. env` file has correct `DISCORD_TOKEN`
- Regenerate token in Discord Developer Portal
- Ensure no extra spaces in token

---

**Error:** `ModuleNotFoundError: No module named 'discord'`

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Bot Online But Not Posting

**Check 1:** Bot permissions
- Ensure bot has "Manage Channels" and "Send Messages" permissions
- Right-click bot in Discord → Role settings

**Check 2:** Feed validity
```bash
python3
>>> import feedparser
>>> feed = feedparser.parse('YOUR_RSS_URL')
>>> print(len(feed.entries))  # Should be > 0
```

**Check 3:** Check bot logs
```bash
# Look for error messages when bot processes feeds
```

---

### Channel Not Created Immediately

**Solution 1:** Check flag files
```bash
ls -la create_channel_*. flag
# If files exist but channel not created, check bot permissions
```

**Solution 2:** Check bot task status
```python
# In bot.py, add logging:
print(f"Monitor task running: {self.monitor_new_feeds.is_running()}")
```

---

### Duplicate Posts

**Solution:** Clear database and restart
```bash
# Backup first
cp rss_feeds.db rss_feeds.db.backup

# Delete database
rm rss_feeds.db

# Restart bot - will recreate database
python3 bot.py
```

---

### Streamlit Not Accessible

**From server:**
```bash
# Check if running
ps aux | grep streamlit

# Check port
netstat -tuln | grep 8501

# Check firewall
sudo ufw status
sudo ufw allow 8501/tcp
```

**From local machine:**
```bash
# Test connection
curl http://YOUR_SERVER_IP:8501

# Use SSH tunnel if firewall blocks
ssh -L 8501:localhost:8501 user@server-ip
```

---

### RSS Feed Not Updating

**Check 1:** Feed still exists
- Visit RSS URL in browser
- Some sites change/remove RSS feeds

**Check 2:** Feed format
```python
import feedparser
feed = feedparser.parse('URL')
print(feed.bozo)  # Should be False or 0
print(feed.entries[0])  # Check structure
```

**Check 3:** Bot check interval
- Default is 5 minutes
- New posts won't appear instantly

---

### Database Locked Error

**Error:** `sqlite3.OperationalError: database is locked`

**Solution:**
```bash
# Stop all processes accessing database
pkill -f bot.py
pkill -f streamlit

# Restart services
```

---

## 📡 Example RSS Feeds

Test the bot with these popular RSS feeds:

### News
- **BBC News:** `http://feeds.bbci.co.uk/news/rss.xml`
- **CNN Top Stories:** `http://rss.cnn.com/rss/cnn_topstories.rss`
- **Reuters:** `https://www.reutersagency.com/feed/`

### Technology
- **TechCrunch:** `https://techcrunch.com/feed/`
- **The Verge:** `https://www.theverge.com/rss/index.xml`
- **Ars Technica:** `https://feeds.arstechnica.com/arstechnica/index`
- **Hacker News:** `https://news.ycombinator.com/rss`

### Security
- **Krebs on Security:** `https://krebsonsecurity.com/feed/`
- **Schneier on Security:** `https://www.schneier.com/feed/atom/`
- **Threatpost:** `https://threatpost. com/feed/`

### Development
- **GitHub Blog:** `https://github.blog/feed/`
- **Dev.to:** `https://dev. to/feed/`
- **CSS-Tricks:** `https://css-tricks.com/feed/`

### Reddit
- **r/programming:** `https://www.reddit. com/r/programming/. rss`
- **r/technology:** `https://www.reddit.com/r/technology/.rss`
- Any subreddit: `https://www.reddit.com/r/SUBREDDIT_NAME/. rss`

### YouTube Channels
Format: `https://www.youtube. com/feeds/videos.xml? channel_id=CHANNEL_ID`

---

## ❓ FAQ

### How many feeds can I monitor? 

No hard limit! The bot can handle hundreds of feeds.  Performance depends on your server resources and Discord API rate limits.

### How often are feeds checked?

Default: Every 5 minutes.  Configurable in `.env` with `RSS_CHECK_INTERVAL`. 

### Can I use multiple Discord servers?

Currently designed for one server. Modify `bot.py` to support multiple guilds by tracking `guild_id` per feed.

### Will old posts be reposted?

No. The bot only posts NEW articles published after the feed is added.  Uses MD5 hashing to prevent duplicates.

### Can I delete Discord channels manually?

Yes, but the bot will recreate them on next check. Remove the feed from Streamlit first.

### Does it work with Atom feeds?

Yes!  `feedparser` supports RSS 1.0, RSS 2.0, and Atom feeds.

### What happens if RSS feed goes down?

Bot logs error and skips that feed. Other feeds continue working normally.

### Can I host this for free?

Yes! Options:
- **Railway.app** - Free tier includes 500 hours/month
- **Google Cloud** - Free tier with e2-micro instance
- **AWS** - Free tier for 12 months (t2.micro)
- **Oracle Cloud** - Always free tier


### Can I customize the bot's name/avatar?

Yes! In Discord Developer Portal → Bot section:
- Change username
- Upload avatar image


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Support

Having issues? Check:
1. This README troubleshooting section
2.  Verify all setup steps completed
3. Check bot permissions in Discord
4. Review console logs for errors

---
