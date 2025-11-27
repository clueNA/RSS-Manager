import streamlit as st
import json
import os
from database import Database
import threading
import time
import asyncio

# Initialize database
db = Database()

# Page config
st.set_page_config(page_title="RSS Feed Manager", page_icon="📡", layout="wide")

st.title("📡 RSS Feed Manager")
st.markdown("---")

# Function to trigger channel creation
def trigger_channel_creation(feed_id, channel_name):
    """Signal the bot to create a channel for new feed"""
    try:
        # Create a flag file that the bot will monitor
        flag_file = f"create_channel_{feed_id}. flag"
        with open(flag_file, 'w') as f:
            f.write(channel_name)
        return True
    except Exception as e:
        print(f"Error creating flag: {e}")
        return False

# Add RSS Feed Section
st.header("Add New RSS Feed")

col1, col2 = st. columns([3, 1])

with col1:
    rss_url = st.text_input("RSS Feed URL", placeholder="https://example.com/feed. rss")

with col2:
    st.write("")
    st.write("")
    add_button = st.button("➕ Add Feed", use_container_width=True)

if add_button:
    if rss_url:
        result = db.add_feed(rss_url)
        if result['success']:
            # Trigger immediate channel creation
            trigger_channel_creation(result['feed_id'], result['channel_name'])
            st.success(f"✅ Feed added successfully! Creating channel: {result['channel_name']}")
            time.sleep(1)
            st.rerun()
        else:
            st. error(f"❌ Error: {result['message']}")
    else:
        st.warning("⚠️ Please enter an RSS feed URL")

st.markdown("---")

# Display Active Feeds
st.header("Active RSS Feeds")

feeds = db.get_all_feeds()

if feeds:
    for feed in feeds:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st. write(f"**{feed['title']}**")
            st.caption(feed['url'])
        
        with col2:
            st.write(f"📺 Channel: `{feed['channel_name']}`")
            st.caption(f"Posts tracked: {feed['posts_count']}")
        
        with col3:
            if st.button("🗑️ Remove", key=f"remove_{feed['id']}"):
                db.remove_feed(feed['id'])
                st.success("Feed removed!")
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
else:
    st.info("📭 No RSS feeds added yet.  Add your first feed above!")

# Footer
st.markdown("---")
st.caption("💡 The Discord bot will automatically create channels and post updates when new articles are published.")