import sqlite3
import json
import feedparser
import re
from datetime import datetime

class Database:
    def __init__(self, db_file='rss_feeds.db'):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3. connect(self.db_file)
        cursor = conn.cursor()
        
        # Create feeds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feeds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                channel_name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create posts table (to track seen posts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feed_id INTEGER NOT NULL,
                post_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (feed_id) REFERENCES feeds (id) ON DELETE CASCADE,
                UNIQUE(feed_id, post_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def sanitize_channel_name(self, name):
        """Sanitize name for Discord channel (lowercase, alphanumeric, hyphens)"""
        # Convert to lowercase
        name = name. lower()
        
        # Replace spaces and special characters with hyphens
        name = re.sub(r'[^a-z0-9]+', '-', name)
        
        # Remove leading/trailing hyphens
        name = name.strip('-')
        
        # Limit length (Discord max is 100 chars)
        name = name[:100]
        
        # Ensure it's not empty
        if not name:
            name = 'rss-feed'
        
        return name
    
    def get_feed_title(self, url):
        """Get feed title from RSS feed"""
        try:
            feed = feedparser.parse(url)
            if feed.feed and hasattr(feed.feed, 'title'):
                return feed.feed.title
            return url
        except:
            return url
    
    def add_feed(self, url):
        """Add new RSS feed"""
        try:
            # Validate URL
            if not url.startswith('http'):
                return {'success': False, 'message': 'Invalid URL format'}
            
            # Try to parse the feed to validate
            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                return {'success': False, 'message': 'Invalid RSS feed or feed is empty'}
            
            # Get feed title
            feed_title = feed.feed.get('title', url) if feed.feed else url
            
            # Generate channel name
            channel_name = self.sanitize_channel_name(feed_title)
            
            # Add to database
            conn = sqlite3. connect(self.db_file)
            cursor = conn.cursor()
            
            # Check if channel name already exists
            cursor.execute('SELECT id FROM feeds WHERE channel_name = ? ', (channel_name,))
            if cursor.fetchone():
                # Append number to make it unique
                counter = 1
                new_channel_name = f"{channel_name}-{counter}"
                while True:
                    cursor.execute('SELECT id FROM feeds WHERE channel_name = ? ', (new_channel_name,))
                    if not cursor. fetchone():
                        channel_name = new_channel_name
                        break
                    counter += 1
                    new_channel_name = f"{channel_name}-{counter}"
            
            cursor.execute('''
                INSERT INTO feeds (url, title, channel_name) 
                VALUES (?, ?, ?)
            ''', (url, feed_title, channel_name))
            
            feed_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'channel_name': channel_name, 'feed_id': feed_id}
            
        except sqlite3.IntegrityError:
            return {'success': False, 'message': 'Feed already exists'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def remove_feed(self, feed_id):
        """Remove RSS feed"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM feeds WHERE id = ?', (feed_id,))
        cursor.execute('DELETE FROM posts WHERE feed_id = ?', (feed_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_feeds(self):
        """Get all RSS feeds"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.id, f.url, f.title, f.channel_name, 
                   COUNT(p.id) as posts_count
            FROM feeds f
            LEFT JOIN posts p ON f.id = p.feed_id
            GROUP BY f.id
        ''')
        
        feeds = []
        for row in cursor.fetchall():
            feeds. append({
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'channel_name': row[3],
                'posts_count': row[4]
            })
        
        conn.close()
        return feeds
    
    def add_post(self, feed_id, post_id):
        """Add post to database (mark as seen)"""
        try:
            conn = sqlite3. connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO posts (feed_id, post_id) 
                VALUES (?, ?)
            ''', (feed_id, post_id))
            
            conn.commit()
            conn. close()
            return True
        except sqlite3.IntegrityError:
            # Post already exists
            return False
        except Exception as e:
            print(f"❌ Error adding post: {str(e)}")
            return False
    
    def post_exists(self, feed_id, post_id):
        """Check if post has been seen before"""
        conn = sqlite3. connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM posts 
            WHERE feed_id = ?  AND post_id = ?
        ''', (feed_id, post_id))
        
        exists = cursor.fetchone() is not None
        conn.close()
        
        return exists