import operator
import os
import time
from notion_client import Client
import yfinance as yf
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load from environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validate required environment variables
required_vars = {
    "NOTION_TOKEN": NOTION_TOKEN,
    "DATABASE_ID": DATABASE_ID,
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
    "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID
}

missing_vars = [name for name, value in required_vars.items() if not value]
if missing_vars:
    print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
    exit(1)

# Connect to Notion
notion = Client(auth=NOTION_TOKEN)

# Operator mapping for conditions
ops = {
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
}

def send_telegram_message(message):
    """Send a message via Telegram bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Telegram message sent: {message[:50]}...")
        else:
            print(f"❌ Failed to send Telegram message: {response.text}")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")

def parse_condition(cond_str):
    """Parse condition strings like '<= 100' or '≤ 100'"""
    cond_str = cond_str.replace('≤', '<=').replace('≥', '>=')
    
    for symbol in ops.keys():
        if cond_str.strip().startswith(symbol):
            return symbol, float(cond_str.strip()[len(symbol):])
    raise ValueError(f"Could not parse condition: {cond_str}")

def debug_database_properties():
    """Debug function to see database structure"""
    try:
        results = notion.databases.query(database_id=DATABASE_ID)
        print(f"Found {len(results['results'])} rows in database")
        
        if results["results"]:
            first_row = results["results"][0]
            print("\nAvailable properties in first row:")
            for prop_name in first_row["properties"].keys():
                print(f"  - {prop_name}")
    except Exception as e:
        print(f"Error querying database: {e}")

def fetch_rows():
    """Fetch and parse rows from Notion database"""
    try:
        results = notion.databases.query(database_id=DATABASE_ID)
        rows = []
        
        for r in results["results"]:
            props = r["properties"]
            
            # Try to get ticker
            ticker = None
            for ticker_name in ["Ticker", "ticker", "Stock", "Symbol"]:
                if ticker_name in props and props[ticker_name]["title"]:
                    ticker = props[ticker_name]["title"][0]["plain_text"]
                    ticker = ticker.replace('$', '').strip()
                    break
            
            # Try to get condition
            condition = None
            for cond_name in ["Price Target", "Condition", "condition", "Alert", "Trigger"]:
                if cond_name in props and props[cond_name]["rich_text"]:
                    condition = props[cond_name]["rich_text"][0]["plain_text"]
                    break
            
            # Try to get context
            context = ""
            for ctx_name in ["Message", "Context", "context", "Notes", "Description"]:
                if ctx_name in props and props[ctx_name]["rich_text"]:
                    context = props[ctx_name]["rich_text"][0]["plain_text"]
                    break
            
            if ticker and condition:
                rows.append((ticker, condition, context))
            else:
                print(f"Skipping row - ticker: {ticker}, condition: {condition}")
        
        return rows
    except Exception as e:
        print(f"Error fetching rows: {e}")
        return []

def check_conditions():
    """Main logic to check stock conditions and send alerts"""
    rows = fetch_rows()
    
    if not rows:
        print("No valid rows found in database")
        return
    
    for ticker, condition, context in rows:
        try:
            # Get current stock price
            stock_data = yf.Ticker(ticker).history(period="1d")
            if stock_data.empty:
                print(f"❌ No data found for {ticker}")
                continue
                
            price = stock_data["Close"].iloc[-1]
            op_symbol, target = parse_condition(condition)
            
            if ops[op_symbol](price, target):
                alert_message = f"🚨 <b>STOCK ALERT</b>\n\n📈 <b>{ticker}</b> price <b>${price:.2f}</b> meets condition <b>{condition}</b>\n\n💭 Context: {context}"
                print(f"🚨 ALERT: {ticker} ${price:.2f} meets condition {condition}")
                send_telegram_message(alert_message)
            else:
                print(f"✅ {ticker} price ${price:.2f} does NOT meet condition {condition}")
                
        except Exception as e:
            print(f"❌ Error with {ticker}: {e}")

def main():
    """Main loop for continuous monitoring"""
    print("🚀 Starting Stock Alert Bot...")
    print("=== Initial Database Check ===")
    debug_database_properties()
    
    # Check interval in seconds (5 minutes = 300 seconds)
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
    
    while True:
        try:
            print(f"\n=== Checking Conditions at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
            check_conditions()
            print(f"💤 Sleeping for {CHECK_INTERVAL // 60} minutes...")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n👋 Bot stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            print("⏳ Waiting 60 seconds before retry...")
            time.sleep(60)

if __name__ == "__main__":
    main()
