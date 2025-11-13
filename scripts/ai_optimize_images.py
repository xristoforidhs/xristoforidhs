#!/usr/bin/env python3
import asyncio
import os
import random
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# AI-curated high-quality product images
PRODUCT_IMAGES_DATABASE = {
    # Electronics - High quality tech images
    "earbuds": [
        "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=300&h=300&fit=crop&q=80"
    ],
    "headphones": [
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=300&h=300&fit=crop&q=80"
    ],
    "watch": [
        "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=300&h=300&fit=crop&q=80"
    ],
    "speaker": [
        "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=300&fit=crop&q=80"
    ],
    "charger": [
        "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1593642532400-2682810df593?w=300&h=300&fit=crop&q=80"
    ],
    "mouse": [
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1527814050087-3793815479db?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1615663947168-576834e7e7ba?w=300&h=300&fit=crop&q=80"
    ],
    "keyboard": [
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&h=300&fit=crop&q=80"
    ],
    "phone": [
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1574920162023-547365f44-6?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=300&h=300&fit=crop&q=80"
    ],
    
    # Home & Living - Lifestyle images
    "lamp": [
        "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300&h=300&fit=crop&q=80"
    ],
    "candle": [
        "https://images.unsplash.com/photo-1512389098783-66b81f86e199?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1602442443969-30f7f83fa18d?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=300&h=300&fit=crop&q=80"
    ],
    "coffee": [
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1559564045-374a3c77f7b3?w=300&h=300&fit=crop&q=80"
    ],
    "pillow": [
        "https://images.unsplash.com/photo-1616594266579-0c581e054f00?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&q=80"
    ],
    "towel": [
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&q=80"
    ],
    "storage": [
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1493663284031-b7e3aaa4b768?w=300&h=300&fit=crop&q=80"
    ],
    "plant": [
        "https://images.unsplash.com/photo-1501959915551-4e8d30928317?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=300&h=300&fit=crop&q=80"
    ],
    
    # Christmas - Festive images
    "christmas": [
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=300&h=300&fit=crop&q=80"
    ],
    "santa": [
        "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1512909444218-3c2aa16ab6b6?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1543589077-47d81606c1bf?w=300&h=300&fit=crop&q=80"
    ],
    "ornament": [
        "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1544273677-fa5850ab9a0b?w=300&h=300&fit=crop&q=80",
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=300&fit=crop&q=80"
    ]
}

def ai_match_product_image(product_name, category):
    """AI-powered image matching based on product name and category"""
    name_lower = product_name.lower()
    category_lower = category.lower()
    
    # Smart keyword matching
    keywords_found = []
    
    # Check for exact matches first
    for keyword, images in PRODUCT_IMAGES_DATABASE.items():
        if keyword in name_lower:
            keywords_found.append((keyword, len(keyword)))  # Longer matches preferred
    
    # If no exact match, use category-based matching
    if not keywords_found:
        if "electronics" in category_lower:
            if any(word in name_lower for word in ["wireless", "bluetooth"]):
                keywords_found.append(("earbuds", 5))
            elif "power" in name_lower or "charger" in name_lower:
                keywords_found.append(("charger", 5))
            elif "mouse" in name_lower:
                keywords_found.append(("mouse", 5))
            elif "keyboard" in name_lower:
                keywords_found.append(("keyboard", 5))
            else:
                keywords_found.append(("headphones", 3))  # Default electronics
        
        elif "home" in category_lower or "living" in category_lower:
            if "lamp" in name_lower or "light" in name_lower:
                keywords_found.append(("lamp", 5))
            elif "coffee" in name_lower:
                keywords_found.append(("coffee", 5))
            elif "pillow" in name_lower:
                keywords_found.append(("pillow", 5))
            elif "towel" in name_lower:
                keywords_found.append(("towel", 5))
            elif "storage" in name_lower or "container" in name_lower:
                keywords_found.append(("storage", 5))
            else:
                keywords_found.append(("plant", 3))  # Default home
        
        elif "christmas" in category_lower:
            if "santa" in name_lower:
                keywords_found.append(("santa", 5))
            elif "ornament" in name_lower or "decoration" in name_lower:
                keywords_found.append(("ornament", 5))
            else:
                keywords_found.append(("christmas", 3))  # Default christmas
    
    # Select best match
    if keywords_found:
        # Sort by match length (longer = better)
        keywords_found.sort(key=lambda x: x[1], reverse=True)
        best_keyword = keywords_found[0][0]
        
        # Return random image from matched category
        if best_keyword in PRODUCT_IMAGES_DATABASE:
            return random.choice(PRODUCT_IMAGES_DATABASE[best_keyword])
    
    # Fallback
    return "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=300&h=300&fit=crop&q=80"

async def ai_optimize_all_product_images():
    """AI-powered optimization of all product images"""
    print("🤖 AI Image Optimization Starting...")
    
    products = await db.products.find({}, {"_id": 0}).to_list(10000)
    
    updated_count = 0
    for product in products:
        product_name = product.get('name', '')
        category = product.get('category', '')
        
        # Get AI-matched image
        optimal_image = ai_match_product_image(product_name, category)
        
        # Update if different
        if optimal_image != product.get('image_url'):
            await db.products.update_one(
                {"id": product['id']},
                {"$set": {"image_url": optimal_image}}
            )
            updated_count += 1
            
            if updated_count <= 10:  # Show first 10 updates
                print(f"✅ {product_name[:40]}... → Optimized image")
    
    print(f"🤖 AI Optimization Complete: {updated_count} product images updated")

if __name__ == "__main__":
    asyncio.run(ai_optimize_all_product_images())