#!/usr/bin/env python3
"""
Seed production database by calling the backend API endpoint
This creates a special admin endpoint to bulk insert products
"""

import asyncio
import aiohttp
import random
from datetime import datetime, timezone

PRODUCTION_API = "https://mytechgadgets.site/api"

# Simple product templates for quick generation
def generate_simple_products():
    products = []
    categories = {
        "Electronics": 1000,
        "Home & Living": 1000,
        "Christmas": 1000
    }
    
    base_names = {
        "Electronics": ["Wireless Earbuds", "Smart Watch", "Bluetooth Speaker", "USB Charger", "Power Bank"],
        "Home & Living": ["Electric Kettle", "Air Purifier", "Storage Container", "Cutting Board", "Dish Rack"],
        "Christmas": ["LED Lights", "Christmas Tree", "Ornaments", "Wreath", "Stockings"]
    }
    
    images = {
        "Electronics": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
        "Home & Living": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800",
        "Christmas": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800"
    }
    
    for category, count in categories.items():
        for i in range(1, count + 1):
            name = random.choice(base_names[category])
            cost = round(random.uniform(10, 50), 2)
            price = round(cost * 1.25, 2)
            
            product = {
                "id": f"prod_{category[:3]}_{i}_{random.randint(1000, 9999)}",
                "name": f"{name} Premium V{i}",
                "description": f"High-quality {name.lower()} with premium features. Perfect for daily use. Fast shipping available.",
                "price": price,
                "cost_price": cost,
                "image_url": images[category],
                "category": category,
                "stock": random.randint(50, 300),
                "rating": round(random.uniform(4.2, 4.9), 1),
                "review_count": random.randint(5, 12),
                "featured": False,
                "daily_offer": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            products.append(product)
    
    return products

async def seed_via_backend():
    print("🚀 Seeding production via backend API...")
    print("=" * 60)
    
    # Generate products
    print("📦 Generating 3000 products...")
    products = generate_simple_products()
    print(f"✅ Generated {len(products)} products")
    
    # Send to backend to insert directly
    print("\n📤 Sending to production backend...")
    
    # Create a bulk insert payload
    payload = {
        "products": products,
        "action": "bulk_insert",
        "clear_existing": True
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Try POST to a seed endpoint
            async with session.post(
                f"{PRODUCTION_API}/admin/seed-products",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=300)
            ) as resp:
                print(f"Response status: {resp.status}")
                if resp.status in [200, 201]:
                    result = await resp.json()
                    print(f"✅ Success: {result}")
                else:
                    text = await resp.text()
                    print(f"❌ Failed: {text}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    await seed_via_backend()

if __name__ == "__main__":
    asyncio.run(main())
