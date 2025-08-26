from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)

print("🔍 Testing Notion Integration...")
print(f"Token starts with: {NOTION_TOKEN[:10]}...")

# Try to list all pages/databases the integration can see
try:
    # Search for databases
    results = notion.search(filter={"property": "object", "value": "database"})
    
    print(f"\n📊 Found {len(results['results'])} accessible databases:")
    
    for db in results['results']:
        print(f"  • ID: {db['id']}")
        print(f"    Title: {db.get('title', [{}])[0].get('plain_text', 'No title') if db.get('title') else 'No title'}")
        print(f"    URL: {db.get('url', 'No URL')}")
        print()
        
    if not results['results']:
        print("❌ No databases found! Your integration might not be connected to any databases.")
        print("\nTry:")
        print("1. Go to your Notion database")
        print("2. Click ... menu → Add connections")
        print("3. Find your integration and connect it")
        
except Exception as e:
    print(f"❌ Error: {e}")

