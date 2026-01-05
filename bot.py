import os
import datetime
import requests

# ====== CONFIG ======
# These must be set as GitHub Secrets (recommended)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "").strip()  # e.g. @JJExpressOfertas

# Optional: number of links per store (keep small to avoid spam)
MAX_LINKS_PER_STORE = 4

AMAZON_DEALS = [
    ("Amazon Deals (General)", "https://www.amazon.com/deals"),
    ("Amazon Gold Box", "https://www.amazon.com/gp/goldbox"),
    ("Amazon Best Sellers", "https://www.amazon.com/Best-Sellers/zgbs"),
    ("Amazon Electronics Deals", "https://www.amazon.com/deals?departments=electronics"),
]

EBAY_DEALS = [
    ("eBay Deals", "https://www.ebay.com/deals"),
    ("eBay Tech Deals", "https://www.ebay.com/deals/tech"),
    ("eBay Refurbished", "https://www.ebay.com/e/_electronics/ebay-refurbished"),
    ("eBay Daily Deals Search", "https://www.ebay.com/sch/i.html?_nkw=deal&_sop=12"),
]

WALMART_DEALS = [
    ("Walmart Deals", "https://www.walmart.com/deals"),
    ("Walmart Clearance", "https://www.walmart.com/browse/0?facet=fulfillment_method_in_store%3AIn-store%7Cretailer_type%3AWalmart%7Cspecial_offers%3AClearance"),
    ("Walmart Electronics Deals", "https://www.walmart.com/deals/electronics"),
    ("Walmart Home Deals", "https://www.walmart.com/deals/home"),
]


def send_message(text: str) -> None:
    if not BOT_TOKEN or not CHANNEL_ID:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID env vars.")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": False,
        "parse_mode": "HTML",
    }
    r = requests.post(url, json=payload, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"Telegram API error: {r.status_code} {r.text}")


def format_block(title: str, links: list[tuple[str, str]], max_links: int) -> str:
    lines = [f"<b>{title}</b>"]
    for name, link in links[:max_links]:
        lines.append(f"• <a href=\"{link}\">{name}</a>")
    return "\n".join(lines)


def main() -> None:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    header = f"🔥 <b>OFERTAS DEL DÍA – JJ EXPRESS</b>\n📅 {today}\n\n" \
             f"Compra en USA y tráelo con nosotros 📦\n"

    parts = [
        format_block("🟧 Amazon", AMAZON_DEALS, MAX_LINKS_PER_STORE),
        format_block("🟦 eBay", EBAY_DEALS, MAX_LINKS_PER_STORE),
        format_block("🟩 Walmart", WALMART_DEALS, MAX_LINKS_PER_STORE),
        "\n📲 Para cotizar o pedir: escríbenos por WhatsApp/Instagram (mismos canales).",
    ]

    msg = header + "\n\n" + "\n\n".join(parts)
    send_message(msg)


if __name__ == "__main__":
    main()
