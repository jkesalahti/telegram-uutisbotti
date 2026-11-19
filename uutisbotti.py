import feedparser
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

lahteet = {
    "Kauppalehti": "https://feeds.kauppalehti.fi/rss/main",
    "Yle" : "https://yle.fi/rss/uutiset/paauutiset"

}


def hae_uutiset(haku, maara=3):
    """Hakee uutiset yhdestä aiheesta."""

    viesti = "Päivän uutiskooste\n\n"
    url = (
        f"https://news.google.com/rss/search?"
        f"q={haku}&hl=fi&gl=FI&ceid=FI:fi"
        )

    feed = feedparser.parse(url)

    return feed.entries[:maara]

def muodosta_viesti(aiheet):
    """Rakentaa Telegram-viestin."""
    
    viesti = "📰 Päivän uutiskooste\n\n"
    
    for otsikko, haku in aiheet.items():   
        viesti += f"{otsikko}\n\n"

        uutiset = hae_uutiset(haku)

        for uutinen in uutiset:
            viesti += f"• {uutinen.title}\n"
            viesti += f"{uutinen.link}\n\n"

    viesti += "\n"

    return viesti

def laheta_viesti(teksti):
    """Lähettaa veistin Telegramiin."""
    
    response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json = {
        "chat_id" : CHAT_ID,
        "text": teksti,
        "disable_web_page_preview" : True
    }
)

def main():
    aiheet = {
        "🤖 Tekoäly": "tekoäly",
        "💰 Sijoittaminen": "sijoittaminen",
        "🪙Talous": "talous",
        "Suomi": "suomi"
    }

    viesti = muodosta_viesti(aiheet)
    laheta_viesti(viesti)


if __name__ == "__main__":
    main()