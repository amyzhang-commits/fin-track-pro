import requests
import json

TELEGRAM_BOT_TOKEN = "8118036157:AAHKhrOh4Qb2geIL9qe9g9tJKf5ZaRrWh1A"

def get_bot_info():
    """Check bot info"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        bot_info = response.json()
        print("🤖 Bot Info:")
        print(f"  Name: {bot_info['result']['first_name']}")
        print(f"  Username: @{bot_info['result']['username']}")
        print(f"  ID: {bot_info['result']['id']}")
    else:
        print(f"❌ Error getting bot info: {response.text}")

def get_chat_updates():
    """Get recent messages/chats"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    
    if response.status_code == 200:
        updates = response.json()
        print(f"\n📨 Found {len(updates['result'])} recent updates:")
        
        if not updates['result']:
            print("  No messages yet. Have your dad send /start to the bot!")
            return
        
        for update in updates['result']:
            if 'message' in update:
                msg = update['message']
                chat = msg['chat']
                user = msg['from']
                
                print(f"\n💬 Message from:")
                print(f"  User: {user.get('first_name', '')} {user.get('last_name', '')}")
                print(f"  Username: @{user.get('username', 'no_username')}")
                print(f"  Chat ID: {chat['id']} ⭐️ <- This is what you need!")
                print(f"  Message: {msg.get('text', 'no_text')}")
                
    else:
        print(f"❌ Error getting updates: {response.text}")

if __name__ == "__main__":
    print("=== TELEGRAM BOT CHAT ID FINDER ===")
    get_bot_info()
    get_chat_updates()
    
    print("\n📋 Instructions:")
    print("1. Make sure your dad found the RIGHT bot (check username above)")
    print("2. Have him send /start or any message to the bot")
    print("3. Run this script again to see his chat ID")
