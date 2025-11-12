#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid
from datetime import datetime
import random

# Load environment variables
load_dotenv('/app/backend/.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Real product images from Unsplash
ELECTRONICS_IMAGES = [
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",  # Headphones
    "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb",  # Headphones 2
    "https://images.unsplash.com/photo-1484704849700-f032a568e944",  # Headphones 3
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12",  # Smart Watch
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30",  # Watch
    "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1",  # Headphones 4
    "https://images.unsplash.com/photo-1590658268037-6bf12165a8df",  # Earbuds
    "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7",  # Speaker
    "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1",  # Keyboard
    "https://images.unsplash.com/photo-1587829741301-dc798b83add3",  # Wireless Mouse
    "https://images.unsplash.com/photo-1527814050087-3793815479db",  # Laptop
    "https://images.unsplash.com/photo-1518770660439-4636190af475",  # Tech
    "https://images.unsplash.com/photo-1593642532400-2682810df593",  # Laptop 2
    "https://images.unsplash.com/photo-1498049794561-7780e7231661",  # Computer
    "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a",  # Power Bank
    "https://images.unsplash.com/photo-1611532736597-de2d4265fba3",  # Wireless Charger
    "https://images.unsplash.com/photo-1583394838336-acd977736f90",  # Headphones 5
    "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae",  # USB Cable
    "https://images.unsplash.com/photo-1574920162023-547365f44-6",  # Phone
    "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",  # Phone Case
]

HOME_LIVING_IMAGES = [
    "https://images.unsplash.com/photo-1524758631624-e2822e304c36",  # Lamp
    "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15",  # Home Decor
    "https://images.unsplash.com/photo-1556911220-bff31c812dba",  # Kitchen
    "https://images.unsplash.com/photo-1556909212-d5b604d0c90d",  # Kitchen 2
    "https://images.unsplash.com/photo-1484101403633-562f891dc89a",  # Desk Lamp
    "https://images.unsplash.com/photo-1538688423619-a81d3f23454b",  # Diffuser
    "https://images.unsplash.com/photo-1585704032915-c3400ca199e7",  # Vacuum
    "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace",  # Coffee Maker
    "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",  # Coffee
    "https://images.unsplash.com/photo-1501959915551-4e8d30928317",  # Plants
    "https://images.unsplash.com/photo-1616594266579-0c581e054f00",  # Pillow
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af",  # Towels
    "https://images.unsplash.com/photo-1558317374-067fb5f30001",  # Kitchen Tools
    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136",  # Storage
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",  # Clock
    "https://images.unsplash.com/photo-1615873968403-89e068629265",  # Rug
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af",  # Bedding
    "https://images.unsplash.com/photo-1617104551722-3f933a4e8b00",  # Cutting Board
    "https://images.unsplash.com/photo-1584622650111-993a426fbf0a",  # Containers
    "https://images.unsplash.com/photo-1556909212-d5b604d0c90d",  # Kitchen Items
]

# Product templates for Electronics
ELECTRONICS_PRODUCTS = [
    ("Wireless Bluetooth Earbuds Pro", "Premium TWS earbuds with active noise cancellation, 30-hour battery life, and IPX7 waterproof rating"),
    ("Smart Watch Fitness Tracker", "Fitness tracker with heart rate monitor, sleep tracking, GPS, and 7-day battery life"),
    ("Portable Bluetooth Speaker", "Waterproof portable speaker with 360° surround sound and 24-hour playtime"),
    ("Over-Ear Wireless Headphones", "Over-ear wireless headphones with studio-quality sound, 40-hour battery, and comfort padding"),
    ("USB-C Fast Charger 65W", "65W fast charging adapter with multiple ports and smart charging technology"),
    ("Power Bank 20000mAh", "High-capacity portable charger with fast charging and multiple USB ports"),
    ("Wireless Gaming Mouse", "Ergonomic wireless mouse with adjustable DPI, rechargeable battery, and silent clicks"),
    ("RGB Mechanical Keyboard", "RGB mechanical gaming keyboard with hot-swappable switches and aluminum frame"),
    ("1080p HD Webcam", "1080p HD webcam with auto-focus, built-in microphone, and wide-angle lens"),
    ("Protective Phone Case", "Protective smartphone case with shock absorption and raised edges"),
    ("Tempered Glass Screen Protector", "Tempered glass screen protector with oleophobic coating and bubble-free installation"),
    ("USB 3.0 Flash Drive 128GB", "High-speed USB 3.0 flash drive with metal casing and compact design"),
    ("4K HDMI Cable", "High-speed HDMI cable supporting 4K@60Hz, HDR, and Ethernet channel"),
    ("Adjustable Laptop Stand", "Adjustable aluminum laptop stand with cooling ventilation and ergonomic height"),
    ("Precision Stylus Pen", "Precision stylus pen with palm rejection, pressure sensitivity, and long battery life"),
]

# Product templates for Home & Living
HOME_LIVING_PRODUCTS = [
    ("LED Desk Lamp", "Adjustable LED desk lamp with multiple brightness levels, USB charging port, and eye-care technology"),
    ("HEPA Air Purifier", "HEPA air purifier with activated carbon filter, removing 99.97% of airborne particles"),
    ("Essential Oil Diffuser", "Ultrasonic aromatherapy diffuser with LED lights, timer, and auto shut-off"),
    ("Programmable Coffee Maker", "Programmable coffee maker with thermal carafe, brew strength control, and auto-start"),
    ("Cordless Vacuum Cleaner", "Powerful cordless vacuum with HEPA filtration, multiple attachments, and long battery life"),
    ("Stackable Storage Bins Set", "Stackable storage bins with lids, perfect for organizing closets, pantry, and garage"),
    ("Modern Wall Clock", "Modern wall clock with silent non-ticking movement and easy-to-read numbers"),
    ("Decorative Throw Pillows", "Decorative throw pillows with soft fabric, hidden zipper, and machine washable covers"),
    ("Luxury Bath Towel Set", "Luxury cotton bath towel set with high absorbency and quick-dry technology"),
    ("Kitchen Knife Set Professional", "Professional stainless steel knife set with ergonomic handles and wooden block"),
    ("Bamboo Cutting Board", "Durable cutting board with juice groove, non-slip feet, and knife-friendly surface"),
    ("Airtight Food Storage Containers", "Airtight food storage containers with leak-proof lids, BPA-free and microwave safe"),
    ("Microfiber Bedding Set", "Complete bedding set including comforter, sheets, and pillowcases with soft microfiber"),
    ("Soft Area Rug", "Soft area rug with non-slip backing, stain-resistant and easy to clean"),
    ("Ceramic Plant Pot", "Decorative plant pot with drainage hole and matching saucer"),
]

# Review templates
REVIEW_TEMPLATES = [
    "Amazing quality! Exceeded my expectations. Highly recommend!",
    "Good value for money. Does exactly what it says.",
    "Very satisfied with this purchase. Fast shipping too!",
    "Perfect! Just what I needed. Will buy again.",
    "Great product. Good quality and works perfectly.",
    "Excellent! Better than I expected. Five stars!",
    "Really happy with this. Worth every penny.",
    "Top quality product. Very impressed!",
]

REVIEWER_NAMES = [
    "John Smith", "Emma Johnson", "Michael Brown", "Sophia Davis", "William Wilson",
    "Olivia Martinez", "James Anderson", "Ava Taylor", "Robert Thomas", "Isabella Garcia",
]

async def generate_products():
    """Generate 1000+ products with real images"""
    print("🚀 Starting massive store seed with real images...")
    
    # Clear existing data
    await db.products.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing products and reviews")
    
    products = []
    
    # Generate Electronics products (525)
    print("📱 Generating Electronics products...")
    for i in range(35):  # 35 iterations
        for idx, (name, desc) in enumerate(ELECTRONICS_PRODUCTS):
            price = round(random.uniform(15.0, 299.0), 2)
            cost_price = round(price / 2.2, 2)
            
            product = {
                "id": str(uuid.uuid4()),
                "name": f"{name} V{i+1}",
                "description": desc,
                "price": price,
                "cost_price": cost_price,
                "image_url": ELECTRONICS_IMAGES[idx % len(ELECTRONICS_IMAGES)] + f"?w=400&h=400&fit=crop&q=80&auto=format",
                "images": [],
                "category": "Electronics",
                "subcategory": name.split()[0],
                "stock": random.randint(50, 500),
                "featured": random.random() < 0.05,
                "daily_offer": random.random() < 0.03,
                "rating": round(random.uniform(3.8, 5.0), 1),
                "review_count": random.randint(8, 150),
                "supplier": "cj_dropshipping",
                "created_at": datetime.now().isoformat()
            }
            products.append(product)
    
    print(f"✅ Generated {len(products)} Electronics products")
    
    # Generate Home & Living products (525)
    print("🏠 Generating Home & Living products...")
    home_start = len(products)
    for i in range(35):  # 35 iterations
        for idx, (name, desc) in enumerate(HOME_LIVING_PRODUCTS):
            price = round(random.uniform(12.0, 199.0), 2)
            cost_price = round(price / 2.2, 2)
            
            product = {
                "id": str(uuid.uuid4()),
                "name": f"{name} V{i+1}",
                "description": desc,
                "price": price,
                "cost_price": cost_price,
                "image_url": HOME_LIVING_IMAGES[idx % len(HOME_LIVING_IMAGES)] + f"?w=400&h=400&fit=crop&q=80&auto=format",
                "images": [],
                "category": "Home & Living",
                "subcategory": name.split()[0],
                "stock": random.randint(50, 500),
                "featured": random.random() < 0.05,
                "daily_offer": random.random() < 0.03,
                "rating": round(random.uniform(3.8, 5.0), 1),
                "review_count": random.randint(8, 150),
                "supplier": "cj_dropshipping",
                "created_at": datetime.now().isoformat()
            }
            products.append(product)
    
    home_count = len(products) - home_start
    print(f"✅ Generated {home_count} Home & Living products")
    
    # Insert all products
    if products:
        await db.products.insert_many(products)
        print(f"💾 Inserted {len(products)} products into database")
    
    # Generate reviews
    print("💬 Generating reviews...")
    reviews = []
    sample_products = random.sample(products, min(400, len(products)))
    
    for product in sample_products:
        num_reviews = random.randint(5, 12)
        for _ in range(num_reviews):
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_id": None,
                "user_name": random.choice(REVIEWER_NAMES),
                "rating": random.randint(4, 5),
                "comment": random.choice(REVIEW_TEMPLATES),
                "verified_purchase": random.random() < 0.85,
                "helpful_count": random.randint(0, 45),
                "created_at": datetime.now().isoformat()
            }
            reviews.append(review)
    
    if reviews:
        await db.reviews.insert_many(reviews)
        print(f"✅ Added {len(reviews)} reviews")
    
    print("\n🎉 Massive store seed complete!")
    print(f"📦 Total: {len(products)} products")
    print(f"📱 Electronics: {len(products) - home_count} products")
    print(f"🏠 Home & Living: {home_count} products")
    print(f"💬 Total: {len(reviews)} reviews")

if __name__ == "__main__":
    asyncio.run(generate_products())
