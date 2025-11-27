import feedparser
import hashlib
from datetime import datetime
from database import Database
import re

class RSSMonitor:
    def __init__(self, db):
        self.db = db
    
    def check_feed(self, feed_url, feed_id):
        """Check RSS feed for new posts"""
        new_posts = []
        
        try:
            # Parse RSS feed
            feed = feedparser. parse(feed_url)
            
            # Check if feed is valid
            if feed.bozo and not feed.entries:
                print(f"⚠️ Invalid or empty feed: {feed_url}")
                return new_posts
            
            # Process each entry
            for entry in feed.entries:
                # Generate unique ID for post
                post_id = self. generate_post_id(entry)
                
                # Check if post already exists
                if not self.db.post_exists(feed_id, post_id):
                    # Extract post data
                    post_data = self.extract_post_data(entry)
                    post_data['post_id'] = post_id
                    
                    # Add to database
                    self.db.add_post(feed_id, post_id)
                    
                    # Add to new posts list
                    new_posts.append(post_data)
            
            return new_posts
            
        except Exception as e:
            print(f"❌ Error checking feed {feed_url}: {str(e)}")
            return new_posts
    
    def generate_post_id(self, entry):
        """Generate unique ID for post"""
        # Try to use GUID or ID from feed
        if hasattr(entry, 'id'):
            return hashlib.md5(entry.id.encode()).hexdigest()
        
        # Fallback to link
        if hasattr(entry, 'link'):
            return hashlib.md5(entry.link.encode()). hexdigest()
        
        # Fallback to title + published date
        unique_string = entry.get('title', '') + str(entry.get('published', ''))
        return hashlib.md5(unique_string.encode()). hexdigest()
    
    def extract_post_data(self, entry):
        """Extract relevant data from RSS entry"""
        post_data = {
            'title': self.clean_html(entry.get('title', 'No Title')),
            'link': entry.get('link', ''),
            'author': None,
            'summary': None,
            'published_date': None,
            'image': None
        }
        
        # Extract author
        if hasattr(entry, 'author'):
            post_data['author'] = entry.author
        elif hasattr(entry, 'author_detail') and entry.author_detail. get('name'):
            post_data['author'] = entry.author_detail['name']
        elif hasattr(entry, 'authors') and entry.authors:
            post_data['author'] = entry.authors[0]. get('name', '')
        
        # Extract summary/description
        if hasattr(entry, 'summary'):
            post_data['summary'] = self.clean_html(entry.summary)
        elif hasattr(entry, 'description'):
            post_data['summary'] = self.clean_html(entry.description)
        
        # Extract published date
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                post_data['published_date'] = datetime(*entry.published_parsed[:6])
            except:
                pass
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            try:
                post_data['published_date'] = datetime(*entry.updated_parsed[:6])
            except:
                pass
        
        # Extract image
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            post_data['image'] = entry.media_thumbnail[0].get('url')
        elif hasattr(entry, 'media_content') and entry.media_content:
            post_data['image'] = entry. media_content[0].get('url')
        elif hasattr(entry, 'links'):
            for link in entry.links:
                if link.get('type', '').startswith('image/'):
                    post_data['image'] = link.get('href')
                    break
        
        return post_data
    
    def clean_html(self, text):
        """Remove HTML tags from text"""
        if not text:
            return ''
        
        # Remove HTML tags
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text