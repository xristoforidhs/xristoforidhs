#!/usr/bin/env python3
"""
PRODUCTION DATABASE SEEDER
Run this to populate production with 3000 products
"""

import asyncio
import random
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Use production MongoDB URL
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'gadget_store')

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

print(f"🔗 Connecting to: {DB_NAME}")

# Import the product templates
ELECTRONICS_TEMPLATES = [
    {
        "base": "Wireless Bluetooth Earbuds",
        "variants": ["Pro", "Ultra", "Premium", "Sport", "Studio", "Elite", "Max", "Plus"],
        "features": [
            "with active noise cancellation and 30-hour battery life",
            "with deep bass and crystal clear sound quality",
            "with IPX7 waterproof rating for workouts",
        ],
        "images": [
            "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800",
            "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=800",
        ],
        "base_cost_range": (8.99, 24.99)
    },
    {
        "base": "Smart Watch Fitness Tracker",
        "variants": ["Pro", "Active", "Sport", "Health", "Fit", "Advanced"],
        "features": [
            "with heart rate monitor and GPS tracking",
            "with sleep tracking and 7-day battery",
            "with blood oxygen monitoring",
        ],
        "images": [
            "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800",
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",
        ],
        "base_cost_range": (12.99, 29.99)
    },
    {
        "base": "Portable Bluetooth Speaker",
        "variants": ["Waterproof", "Outdoor", "Mini", "Mega", "Bass", "RGB"],
        "features": [
            "with 360° surround sound and 24-hour battery",
            "with IPX7 waterproof and shockproof design",
            "with RGB LED lights sync with music",
        ],
        "images": [
            "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800",
            "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800",
        ],
        "base_cost_range": (9.99, 34.99)
    },
]

HOME_TEMPLATES = [
    {
        "base": "Electric Kettle",
        "variants": ["Glass", "Stainless Steel", "Temperature Control", "Fast Boil"],
        "features": [
            "with temperature control 5 presets",
            "with keep warm function",
            "with auto shut-off protection",
        ],
        "images": ["https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800"],
        "base_cost_range": (14.99, 34.99)
    },
    {
        "base": "Air Purifier",
        "variants": ["HEPA", "Smart", "Quiet", "Large Room"],
        "features": [
            "with True HEPA filter removes 99.97% allergens",
            "with smart air quality sensor",
            "with ultra-quiet sleep mode",
        ],
        "images": ["https://images.unsplash.com/photo-1606768666853-403c90a981ad?w=800"],
        "base_cost_range": (29.99, 69.99)
    },
]

CHRISTMAS_TEMPLATES = [
    {
        "base": "Christmas LED Lights",
        "variants": ["String", "Icicle", "Net", "Curtain", "Outdoor"],
        "features": [
            "with 8 lighting modes and remote control",
            "waterproof for indoor and outdoor use",
            "with memory function and timer",
        ],
        "images": ["https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800"],
        "base_cost_range": (6.99, 24.99)
    },
    {
        "base": "Christmas Tree",
        "variants": ["Pre-Lit", "Flocked", "Slim", "Full"],
        "features": [
            "with pre-installed LED lights",
            "easy assembly with color-coded branches",
            "with metal stand included",
        ],
        "images": ["https://images.unsplash.com/photo-1544289890-f54ac1dd2789?w=800"],
        "base_cost_range": (29.99, 99.99)
    },
]

def generate_product(template, num, category):
    variant = random.choice(template["variants"])
    feature = random.choice(template["features"])
    image = random.choice(template["images"])
    cost = round(random.uniform(*template["base_cost_range"]), 2)
    price = round(cost * 1.25, 2)  # 25% markup = 20% profit
    
    return {
        "id": f"prod_{random.randint(100000, 999999)}",
        "name": f"{template['base']} {variant} V{num}",
        "description": f"Premium {template['base'].lower()} {feature}. High-quality construction. Perfect for daily use and makes excellent gift.",
        "price": price,
        "cost_price": cost,
        "image_url": image,
        "category": category,
        "stock": random.randint(50, 300),
        "rating": round(random.uniform(4.2, 4.9), 1),
        "review_count": random.randint(5, 12),
        "featured": random.random() < 0.1,
        "daily_offer": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

def generate_review(product_id):
    reviews_text = [
        "Excellent product! Exactly as described. Very happy!",
        "Great quality for the price. Works perfectly!",
        "Love it! Better than expected. Fast shipping!",
        "Perfect! Just what I needed. Will buy again.",
        "Amazing quality! Very satisfied. Recommended!",
    ]
    
    return {
        "id": f"review_{product_id}_{random.randint(1000, 9999)}",
        "product_id": product_id,
        "user_id": f"user_{random.randint(1000, 9999)}",
        "user_name": f"Customer {random.randint(100, 999)}",
        "rating": random.choices([3, 4, 5], weights=[5, 30, 65])[0],
        "comment": random.choice(reviews_text),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

async def seed_production():
    print("🚀 SEEDING PRODUCTION DATABASE")
    print("=" * 60)
    
    # Clear existing
    print("🗑️  Clearing old data...")
    await db.products.delete_many({})
    await db.reviews.delete_many({})
    print("✅ Cleared\n")
    
    all_products = []
    all_reviews = []
    
    # Generate 1000 Electronics
    print("📱 Generating 1000 Electronics...")
    for i in range(1, 1001):
        template = random.choice(ELECTRONICS_TEMPLATES)
        product = generate_product(template, i, "Electronics")
        all_products.append(product)
        
        # Generate reviews
        for _ in range(random.randint(5, 10)):
            all_reviews.append(generate_review(product["id"]))
        
        if i % 200 == 0:
            print(f"   {i}/1000...")
    
    # Generate 1000 Home & Living
    print("🏠 Generating 1000 Home & Living...")
    for i in range(1, 1001):
        template = random.choice(HOME_TEMPLATES)
        product = generate_product(template, i, "Home & Living")
        all_products.append(product)
        
        for _ in range(random.randint(5, 10)):
            all_reviews.append(generate_review(product["id"]))
        
        if i % 200 == 0:
            print(f"   {i}/1000...")
    
    # Generate 1000 Christmas
    print("🎄 Generating 1000 Christmas...")
    for i in range(1, 1001):
        template = random.choice(CHRISTMAS_TEMPLATES)
        product = generate_product(template, i, "Christmas")
        all_products.append(product)
        
        for _ in range(random.randint(5, 10)):
            all_reviews.append(generate_review(product["id"]))
        
        if i % 200 == 0:
            print(f"   {i}/1000...")
    
    # Insert all
    print(f"\n💾 Inserting {len(all_products)} products...")
    await db.products.insert_many(all_products)
    
    print(f"⭐ Inserting {len(all_reviews)} reviews...")
    await db.reviews.insert_many(all_reviews)
    
    # Verify
    count = await db.products.count_documents({})
    electronics = await db.products.count_documents({"category": "Electronics"})
    home = await db.products.count_documents({"category": "Home & Living"})
    christmas = await db.products.count_documents({"category": "Christmas"})
    
    print("\n" + "=" * 60)
    print("🎉 PRODUCTION SEEDING COMPLETE!")
    print(f"   Total Products: {count}")
    print(f"   Electronics: {electronics}")
    print(f"   Home & Living: {home}")
    print(f"   Christmas: {christmas}")
    print(f"   Total Reviews: {len(all_reviews)}")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_production())
