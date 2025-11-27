import discord
from discord.ext import commands, tasks
import asyncio
import os
import glob
from database import Database
from rss_monitor import RSSMonitor

class DiscordBot:
    def __init__(self, token):
        intents = discord.Intents. default()
        intents.message_content = True
        intents.guilds = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.token = token
        self.db = Database()
        self.rss_monitor = RSSMonitor(self.db)
        self.guild_id = None
        self.created_channels = set()  # Track created channels
        
        # Setup events
        @self.bot.event
        async def on_ready():
            print(f'✅ Bot logged in as {self.bot.user}')
            if not self.check_feeds. is_running():
                self. check_feeds.start()
            if not self.monitor_new_feeds.is_running():
                self.monitor_new_feeds.start()
            
            # Create channels for existing feeds on startup
            await self.create_channels_for_existing_feeds()
        
        @tasks.loop(minutes=5)
        async def check_feeds():
            """Check all RSS feeds every 5 minutes"""
            await self.process_feeds()
        
        @tasks.loop(seconds=2)
        async def monitor_new_feeds():
            """Monitor for new feed additions and create channels immediately"""
            await self.check_for_new_feeds()
        
        self.check_feeds = check_feeds
        self.monitor_new_feeds = monitor_new_feeds
    
    async def create_channels_for_existing_feeds(self):
        """Create channels for all existing feeds on bot startup"""
        if not self.bot.guilds:
            print("⚠️ Bot is not in any guild yet")
            return
        
        guild = self.bot.guilds[0]
        feeds = self.db.get_all_feeds()
        
        for feed in feeds:
            channel = await self.get_or_create_channel(guild, feed['channel_name'])
            if channel:
                self.created_channels.add(feed['channel_name'])
    
    async def check_for_new_feeds(self):
        """Check for flag files indicating new feeds to create channels for"""
        if not self.bot.guilds:
            return
        
        guild = self. bot.guilds[0]
        
        # Look for flag files
        flag_files = glob.glob("create_channel_*.flag")
        
        for flag_file in flag_files:
            try:
                # Read channel name from flag file
                with open(flag_file, 'r') as f:
                    channel_name = f.read(). strip()
                
                # Create channel if not already created
                if channel_name not in self.created_channels:
                    channel = await self.get_or_create_channel(guild, channel_name)
                    if channel:
                        self.created_channels.add(channel_name)
                        print(f"✅ Immediately created channel for new feed: {channel_name}")
                
                # Remove flag file
                os.remove(flag_file)
                
            except Exception as e:
                print(f"❌ Error processing flag file {flag_file}: {str(e)}")
                # Try to remove the flag file anyway
                try:
                    os.remove(flag_file)
                except:
                    pass
    
    async def process_feeds(self):
        """Process all RSS feeds and post updates"""
        if not self.bot.guilds:
            print("⚠️ Bot is not in any guild yet")
            return
        
        guild = self.bot.guilds[0]  # Use first guild
        feeds = self.db.get_all_feeds()
        
        for feed in feeds:
            try:
                # Get or create channel
                channel = await self.get_or_create_channel(guild, feed['channel_name'])
                
                if channel:
                    # Add to created channels set
                    self.created_channels.add(feed['channel_name'])
                    
                    # Check for new posts
                    new_posts = self.rss_monitor.check_feed(feed['url'], feed['id'])
                    
                    # Send new posts to Discord
                    for post in new_posts:
                        await self.send_post_embed(channel, post, feed['title'])
                
            except Exception as e:
                print(f"❌ Error processing feed {feed['title']}: {str(e)}")
    
    async def get_or_create_channel(self, guild, channel_name):
        """Get existing channel or create new one"""
        # Look for existing channel
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if existing_channel:
            return existing_channel
        
        # Create new channel
        try:
            new_channel = await guild.create_text_channel(
                name=channel_name,
                topic=f"RSS feed updates for {channel_name}"
            )
            print(f"✅ Created channel: {channel_name}")
            return new_channel
        except discord.Forbidden:
            print(f"❌ No permission to create channel: {channel_name}")
            return None
        except Exception as e:
            print(f"❌ Error creating channel {channel_name}: {str(e)}")
            return None
    
    async def send_post_embed(self, channel, post, feed_title):
        """Send RSS post as Discord embed"""
        if not channel:
            return
        
        try:
            # Create embed
            embed = discord. Embed(
                title=post['title'],
                url=post['link'],
                description=post.get('summary', '')[:500] + ('...' if len(post.get('summary', '')) > 500 else ''),
                color=0x00AAFF,
                timestamp=post.get('published_date')
            )
            
            # Add author if available
            if post.get('author'):
                embed.add_field(name="👤 Author", value=post['author'], inline=True)
            
            # Add source
            embed.set_footer(text=f"Source: {feed_title}")
            
            # Add thumbnail if available
            if post.get('image'):
                embed.set_thumbnail(url=post['image'])
            
            await channel.send(embed=embed)
            print(f"✅ Posted: {post['title'][:50]}...")
            
        except discord.Forbidden:
            print(f"❌ No permission to send message in {channel.name}")
        except Exception as e:
            print(f"❌ Error sending embed: {str(e)}")
    
    def run(self):
        """Start the bot"""
        try:
            self.bot.run(self.token)
        except Exception as e:
            print(f"❌ Error starting bot: {str(e)}")

# For running the bot standalone
if __name__ == "__main__":
    from config import DISCORD_TOKEN
    bot = DiscordBot(DISCORD_TOKEN)
    bot.run()