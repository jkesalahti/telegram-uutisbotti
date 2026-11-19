import feedparser
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

feed = feedparser.parse(
    "https://news.google.com/rss/search?q=artificial+intelligence"
)

viesti = "📰 Päivän uutiset\n\n"

for uutinen in feed.entries[:5]:
    viesti += f"• {uutinen.title}\n"
    viesti += f"{uutinen.link}\n\n"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json = {
        "chat_id" : CHAT_ID,
        "text": viesti,
        "disable_web_page_preview" : True
    }
)
