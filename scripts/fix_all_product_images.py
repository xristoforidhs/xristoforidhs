#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Better product images by category
ELECTRONICS_IMAGES_MAPPING = {
    "wireless bluetooth earbuds": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop",
    "earbuds": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop",
    "headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
    "smart watch": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=400&fit=crop",
    "watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
    "speaker": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop",
    "bluetooth speaker": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop",
    "charger": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=400&h=400&fit=crop",
    "power bank": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=400&h=400&fit=crop",
    "mouse": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
    "keyboard": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop",
    "webcam": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
    "phone case": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop",
    "screen protector": "https://images.unsplash.com/photo-1574920162023-547365f44-6?w=400&h=400&fit=crop",
    "flash drive": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop",
    "hdmi cable": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400&h=400&fit=crop",
    "laptop stand": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
    "stylus": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop"
}

HOME_LIVING_IMAGES_MAPPING = {
    "lamp": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=400&h=400&fit=crop",
    "desk lamp": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=400&h=400&fit=crop",
    "air purifier": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=400&h=400&fit=crop",
    "diffuser": "https://images.unsplash.com/photo-1538688423619-a81d3f23454b?w=400&h=400&fit=crop",
    "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop",
    "coffee maker": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=400&h=400&fit=crop",
    "vacuum": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=400&h=400&fit=crop",
    "storage": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop",
    "bins": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop",
    "clock": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop",
    "pillow": "https://images.unsplash.com/photo-1616594266579-0c581e054f00?w=400&h=400&fit=crop",
    "towel": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=400&fit=crop",
    "knife": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop",
    "cutting board": "https://images.unsplash.com/photo-1617104551722-3f933a4e8b00?w=400&h=400&fit=crop",
    "container": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400&h=400&fit=crop",
    "bedding": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=400&fit=crop",
    "rug": "https://images.unsplash.com/photo-1615873968403-89e068629265?w=400&h=400&fit=crop",
    "plant": "https://images.unsplash.com/photo-1501959915551-4e8d30928317?w=400&h=400&fit=crop",
    "pot": "https://images.unsplash.com/photo-1501959915551-4e8d30928317?w=400&h=400&fit=crop"
}

CHRISTMAS_IMAGES_MAPPING = {
    "christmas lights": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop",
    "lights": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop",
    "santa": "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=400&h=400&fit=crop",
    "ornament": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",
    "wreath": "https://images.unsplash.com/photo-1544273677-5c7e2c2d05a7?w=400&h=400&fit=crop",
    "snow globe": "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop",
    "reindeer": "https://images.unsplash.com/photo-1543589077-47d81606c1bf?w=400&h=400&fit=crop",
    "candle": "https://images.unsplash.com/photo-1512389098783-66b81f86e199?w=400&h=400&fit=crop",
    "table": "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=400&h=400&fit=crop",
    "cookie": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",
    "hat": "https://images.unsplash.com/photo-1512909444218-3c2aa16ab6b6?w=400&h=400&fit=crop",
    "stocking": "https://images.unsplash.com/photo-1544273677-2272bddc8ff6?w=400&h=400&fit=crop",
    "tree": "https://images.unsplash.com/photo-1544273677-fa5850ab9a0b?w=400&h=400&fit=crop",
    "mug": "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop",
    "advent": "https://images.unsplash.com/photo-1543589077-47d81606c1bf?w=400&h=400&fit=crop",
    "sweater": "https://images.unsplash.com/photo-1544273677-c433b8c2e2e9?w=400&h=400&fit=crop",
    "village": "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop",
    "garland": "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=400&h=400&fit=crop",
    "gift": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",
    "nutcracker": "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop"
}

async def fix_all_product_images():
    """Fix all product images to match their names better"""
    print("🖼️  Fixing ALL product images...")
    
    # Get all products
    products = await db.products.find({}, {"_id": 0}).to_list(10000)
    
    updated_count = 0
    for product in products:
        product_name = product.get('name', '').lower()
        category = product.get('category', '')
        new_image = None
        
        # Choose mapping based on category
        if category == "Electronics":
            mapping = ELECTRONICS_IMAGES_MAPPING
        elif category == "Home & Living":
            mapping = HOME_LIVING_IMAGES_MAPPING
        elif category == "Christmas":
            mapping = CHRISTMAS_IMAGES_MAPPING
        else:
            continue
        
        # Find best matching image
        for keyword, image_url in mapping.items():
            if keyword in product_name:
                new_image = image_url
                break
        
        # Update if we found a better image
        if new_image and new_image != product.get('image_url'):
            await db.products.update_one(
                {"id": product['id']},
                {"$set": {"image_url": new_image}}
            )
            updated_count += 1
            print(f"Updated: {product['name'][:50]}... -> {keyword}")
    
    print(f"✅ Updated {updated_count} product images")

if __name__ == "__main__":
    asyncio.run(fix_all_product_images())