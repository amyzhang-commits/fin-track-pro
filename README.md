# Stock Alert Bot

A Python bot that monitors stock prices via Yahoo Finance and sends Telegram alerts when target prices are met, using Notion as the database for stock watchlists.

## Features

- 📊 Real-time stock price monitoring via Yahoo Finance API
- 📱 Telegram notifications when price targets are hit
- 🗄️ Notion database integration for managing watchlists
- ☁️ Deploy to Railway for 24/7 monitoring
- 🔄 Automatic price checking every 5 minutes

## How It Works

1. **Notion Database**: Store stock symbols, price conditions (e.g., ">= 150"), and context notes
2. **Price Monitoring**: Bot checks current prices against your conditions every 5 minutes
3. **Telegram Alerts**: Get notified instantly when a stock hits your target price

## Setup

### 1. Notion Integration
- Create a Notion integration at https://www.notion.so/my-integrations
- Share your stock database with the integration
- Note your integration token and database ID

### 2. Telegram Bot
- Create a bot with @BotFather on Telegram
- Get your bot token and chat ID

### 3. Environment Variables
```bash
NOTION_TOKEN=your_notion_integration_token
DATABASE_ID=your_notion_database_id
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
CHECK_INTERVAL=300  # seconds between checks (optional)
```

### 4. Notion Database Structure
Your Notion database should have these properties:
- **Ticker** (Title): Stock symbol (e.g., "AAPL")
- **Price Target** (Text): Condition like ">= 150" or "<= 100"
- **Message** (Text): Context note for the alert

## Deployment

### Local Development
```bash
# Using UV (recommended)
uv add notion-client yfinance requests python-dotenv
uv run mvp2.py

# Or with pip
pip install -r requirements.txt
python mvp2.py
```

### Railway (24/7 Cloud Hosting)
1. Push to GitHub
2. Connect Railway to your repo
3. Set environment variables in Railway dashboard
4. Deploy automatically!

## Files

- `mvp2.py` - Main bot script with continuous monitoring
- `requirements.txt` - Python dependencies
- `debug_notion.py` - Helper to debug Notion database access
- `get_chat_id.py` - Helper to get your Telegram chat ID

## Example Alert

```
🚨 STOCK ALERT

📈 AAPL price $152.30 meets condition >= 150

💭 Context: Good entry point for long position
```

---

Built for monitoring dad's stock portfolio! 📈👨‍💼
