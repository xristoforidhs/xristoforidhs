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

# Better product images mapped by product type
PRODUCT_IMAGE_MAPPING = {
    # Electronics
    "Wireless Bluetooth Earbuds": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop",
    "Smart Watch": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=400&fit=crop",
    "Portable Bluetooth Speaker": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop",
    "Over-Ear Wireless Headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
    "USB-C Fast Charger": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=400&h=400&fit=crop",
    "Power Bank": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=400&h=400&fit=crop",
    "Wireless Gaming Mouse": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop",
    "RGB Mechanical Keyboard": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop",
    "1080p HD Webcam": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
    "Protective Phone Case": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop",
    "Tempered Glass Screen": "https://images.unsplash.com/photo-1574920162023-547365f44-6?w=400&h=400&fit=crop",
    "USB 3.0 Flash Drive": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop",
    "4K HDMI Cable": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400&h=400&fit=crop",
    "Adjustable Laptop Stand": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
    "Precision Stylus Pen": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop",
    
    # Home & Living
    "LED Desk Lamp": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=400&h=400&fit=crop",
    "HEPA Air Purifier": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=400&h=400&fit=crop",
    "Essential Oil Diffuser": "https://images.unsplash.com/photo-1538688423619-a81d3f23454b?w=400&h=400&fit=crop",
    "Programmable Coffee Maker": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop",
    "Cordless Vacuum Cleaner": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=400&h=400&fit=crop",
    "Stackable Storage Bins": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop",
    "Modern Wall Clock": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop",
    "Decorative Throw Pillows": "https://images.unsplash.com/photo-1616594266579-0c581e054f00?w=400&h=400&fit=crop",
    "Luxury Bath Towel": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=400&fit=crop",
    "Kitchen Knife Set": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop",
    "Bamboo Cutting Board": "https://images.unsplash.com/photo-1617104551722-3f933a4e8b00?w=400&h=400&fit=crop",
    "Airtight Food Storage": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400&h=400&fit=crop",
    "Microfiber Bedding Set": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=400&fit=crop",
    "Soft Area Rug": "https://images.unsplash.com/photo-1615873968403-89e068629265?w=400&h=400&fit=crop",
    "Ceramic Plant Pot": "https://images.unsplash.com/photo-1501959915551-4e8d30928317?w=400&h=400&fit=crop",
}

async def fix_product_images():
    """Fix product images to be more relevant"""
    print("🖼️  Fixing product images...")
    
    products = await db.products.find({}, {"_id": 0}).to_list(10000)
    
    updated_count = 0
    for product in products:
        # Find matching image based on product name
        matched_image = None
        product_name = product.get('name', '')
        
        for key, image_url in PRODUCT_IMAGE_MAPPING.items():
            if key.lower() in product_name.lower():
                matched_image = image_url
                break
        
        if matched_image and matched_image != product.get('image_url'):
            await db.products.update_one(
                {"id": product['id']},
                {"$set": {"image_url": matched_image}}
            )
            updated_count += 1
    
    print(f"✅ Updated {updated_count} product images")

if __name__ == "__main__":
    asyncio.run(fix_product_images())