import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path(__file__).parent.parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

async def seed_generic_products():
    """Seed database with generic no-brand gadgets"""
    
    print("🌱 Seeding generic gadgets...")
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Clear existing products
    await db.products.delete_many({})
    print("🗑️  Cleared existing products")
    
    # Generic no-brand gadgets (Temu-style)
    products = [
        {
            "id": str(uuid.uuid4()),
            "name": "Wireless Bluetooth Earbuds TWS-X9",
            "description": "Premium wireless earbuds with noise cancellation, 30-hour battery life, and IPX7 waterproof rating. Perfect for music, calls, and workouts. Universal compatibility with all devices.",
            "price": 24.99,
            "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80",
            "category": "Audio",
            "stock": 500,
            "featured": True,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Smart Fitness Watch - Activity Tracker",
            "description": "Multi-function smartwatch with heart rate monitor, sleep tracking, 50+ sport modes, and 7-day battery life. Water-resistant design with AMOLED display.",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1544117519-31a4b719223d?w=800&q=80",
            "category": "Wearables",
            "stock": 350,
            "featured": True,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fast Charging Power Bank 20000mAh",
            "description": "Ultra-high capacity portable charger with 3 USB ports and USB-C PD 65W. Charge multiple devices simultaneously. LED display shows remaining battery.",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80",
            "category": "Power Banks",
            "stock": 600,
            "featured": True,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Wireless Gaming Mouse RGB 6400 DPI",
            "description": "Ergonomic wireless gaming mouse with 7 programmable buttons, adjustable DPI up to 6400, and customizable RGB lighting. 40-hour battery life.",
            "price": 19.99,
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80",
            "category": "Gaming",
            "stock": 400,
            "featured": True,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LED Ring Light with Tripod Stand",
            "description": "Professional 10-inch LED ring light with adjustable brightness and color temperature. Includes extendable tripod and phone holder. Perfect for selfies, TikTok, and streaming.",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80",
            "category": "Photography",
            "stock": 300,
            "featured": True,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mini Portable Projector HD 1080P",
            "description": "Compact LED projector with 1080P resolution and 100-inch display. Built-in speaker, WiFi connectivity, and multiple input options. Perfect for home entertainment.",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800&q=80",
            "category": "Electronics",
            "stock": 200,
            "featured": False,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Wireless Car Phone Mount with Fast Charging",
            "description": "Auto-clamping car mount with 15W wireless charging. One-hand operation, 360° rotation, and secure grip for safe driving. Works with all phone sizes.",
            "price": 27.99,
            "image_url": "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=800&q=80",
            "category": "Accessories",
            "stock": 450,
            "featured": False,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bluetooth Speaker Waterproof IPX7",
            "description": "Portable wireless speaker with 360° sound, deep bass, and 24-hour playtime. Waterproof design perfect for outdoor adventures. Built-in microphone for hands-free calls.",
            "price": 32.99,
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80",
            "category": "Audio",
            "stock": 380,
            "featured": False,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "USB-C Hub 7-in-1 Multiport Adapter",
            "description": "Universal USB-C hub with HDMI 4K, 3x USB 3.0, SD card reader, and 100W PD charging. Slim aluminum design compatible with all USB-C devices.",
            "price": 22.99,
            "image_url": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80",
            "category": "Accessories",
            "stock": 550,
            "featured": False,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "HD Webcam 1080P with Microphone",
            "description": "Professional webcam for video calls, streaming, and online meetings. Auto-focus, wide-angle lens, and noise-canceling dual microphones. Plug and play setup.",
            "price": 36.99,
            "image_url": "https://images.unsplash.com/photo-1614624532983-4ce03382d63d?w=800&q=80",
            "category": "Electronics",
            "stock": 320,
            "featured": False,
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.products.insert_many(products)
    print(f"✅ {len(products)} generic gadgets added")
    
    client.close()
    print("✅ Database seeded successfully with no-brand gadgets!")

if __name__ == "__main__":
    asyncio.run(seed_generic_products())
