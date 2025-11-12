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

# Product templates for each category
ELECTRONICS_PRODUCTS = [
    {
        "base_name": "Wireless Bluetooth Earbuds",
        "description": "Premium TWS earbuds with active noise cancellation, 30-hour battery life, and IPX7 waterproof rating",
        "variants": ["Pro", "Max", "Ultra", "Plus", "Elite", "Premium", "Advanced", "Sport", "Gaming", "Studio"]
    },
    {
        "base_name": "Smart Watch",
        "description": "Fitness tracker with heart rate monitor, sleep tracking, GPS, and 7-day battery life",
        "variants": ["Pro", "Sport", "Fitness", "Health", "Active", "Plus", "Elite", "Runner", "Athlete", "Training"]
    },
    {
        "base_name": "Portable Bluetooth Speaker",
        "description": "Waterproof portable speaker with 360° surround sound and 24-hour playtime",
        "variants": ["Mini", "Pro", "Max", "Ultra", "Mega", "Plus", "XL", "Boom", "Bass", "Party"]
    },
    {
        "base_name": "Wireless Headphones",
        "description": "Over-ear wireless headphones with studio-quality sound, 40-hour battery, and comfort padding",
        "variants": ["Pro", "Studio", "DJ", "Music", "Premium", "Elite", "Plus", "Max", "Ultra", "Hi-Fi"]
    },
    {
        "base_name": "USB-C Fast Charger",
        "description": "65W fast charging adapter with multiple ports and smart charging technology",
        "variants": ["20W", "30W", "45W", "65W", "100W", "Dual", "Triple", "Quad", "Travel", "Desktop"]
    },
    {
        "base_name": "Power Bank",
        "description": "High-capacity portable charger with fast charging and multiple USB ports",
        "variants": ["10000mAh", "20000mAh", "30000mAh", "Mini", "Pro", "Solar", "Wireless", "Slim", "Heavy Duty", "Quick Charge"]
    },
    {
        "base_name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with adjustable DPI, rechargeable battery, and silent clicks",
        "variants": ["Gaming", "Office", "Travel", "Vertical", "Pro", "RGB", "Silent", "Ambidextrous", "Compact", "Precision"]
    },
    {
        "base_name": "Mechanical Keyboard",
        "description": "RGB mechanical gaming keyboard with hot-swappable switches and aluminum frame",
        "variants": ["60%", "TKL", "Full Size", "Gaming", "RGB", "Wireless", "Compact", "Pro", "Elite", "Custom"]
    },
    {
        "base_name": "USB Webcam",
        "description": "1080p HD webcam with auto-focus, built-in microphone, and wide-angle lens",
        "variants": ["1080p", "2K", "4K", "Pro", "Business", "Streaming", "Conference", "Auto-Focus", "Wide Angle", "Low Light"]
    },
    {
        "base_name": "Phone Case",
        "description": "Protective smartphone case with shock absorption and raised edges",
        "variants": ["Slim", "Rugged", "Clear", "Leather", "Silicone", "Magnetic", "Wallet", "Armor", "Designer", "Ultra Thin"]
    },
    {
        "base_name": "Screen Protector",
        "description": "Tempered glass screen protector with oleophobic coating and bubble-free installation",
        "variants": ["Tempered Glass", "Privacy", "Anti-Glare", "Blue Light", "Matte", "HD Clear", "Curved", "Full Coverage", "2-Pack", "3-Pack"]
    },
    {
        "base_name": "USB Flash Drive",
        "description": "High-speed USB 3.0 flash drive with metal casing and compact design",
        "variants": ["32GB", "64GB", "128GB", "256GB", "512GB", "Type-C", "OTG", "Encrypted", "Waterproof", "Keychain"]
    },
    {
        "base_name": "HDMI Cable",
        "description": "High-speed HDMI cable supporting 4K@60Hz, HDR, and Ethernet channel",
        "variants": ["1m", "2m", "3m", "5m", "10m", "Flat", "Braided", "Gold-Plated", "Ultra HD", "8K Ready"]
    },
    {
        "base_name": "Laptop Stand",
        "description": "Adjustable aluminum laptop stand with cooling ventilation and ergonomic height",
        "variants": ["Portable", "Fixed", "Adjustable", "Cooling", "Wood", "Aluminum", "Foldable", "Desktop", "Mobile", "Pro"]
    },
    {
        "base_name": "Tablet Stylus Pen",
        "description": "Precision stylus pen with palm rejection, pressure sensitivity, and long battery life",
        "variants": ["Basic", "Pro", "Apple Compatible", "Universal", "Rechargeable", "Fine Tip", "Artist", "Note Taking", "Digital Art", "Smart"]
    }
]

HOME_LIVING_PRODUCTS = [
    {
        "base_name": "LED Desk Lamp",
        "description": "Adjustable LED desk lamp with multiple brightness levels, USB charging port, and eye-care technology",
        "variants": ["Touch Control", "Dimmable", "RGB", "Wireless Charging", "Architect", "Clamp", "Minimalist", "Smart", "Color Changing", "Reading"]
    },
    {
        "base_name": "Air Purifier",
        "description": "HEPA air purifier with activated carbon filter, removing 99.97% of airborne particles",
        "variants": ["Mini", "Desktop", "Room", "Large Room", "Smart", "HEPA", "UV-C", "Quiet", "Night Light", "Allergen"]
    },
    {
        "base_name": "Essential Oil Diffuser",
        "description": "Ultrasonic aromatherapy diffuser with LED lights, timer, and auto shut-off",
        "variants": ["Wood Grain", "Glass", "Ceramic", "Smart", "Large Capacity", "Portable", "Color Changing", "Humidifier", "Quiet", "Designer"]
    },
    {
        "base_name": "Coffee Maker",
        "description": "Programmable coffee maker with thermal carafe, brew strength control, and auto-start",
        "variants": ["Single Serve", "12 Cup", "French Press", "Pour Over", "Espresso", "Drip", "Cold Brew", "Grind and Brew", "Thermal", "Smart"]
    },
    {
        "base_name": "Vacuum Cleaner",
        "description": "Powerful cordless vacuum with HEPA filtration, multiple attachments, and long battery life",
        "variants": ["Handheld", "Stick", "Robot", "Wet/Dry", "Cordless", "Bagless", "HEPA", "Pet Hair", "Lightweight", "Pro"]
    },
    {
        "base_name": "Storage Bins",
        "description": "Stackable storage bins with lids, perfect for organizing closets, pantry, and garage",
        "variants": ["Small", "Medium", "Large", "Clear", "Fabric", "Plastic", "Collapsible", "Wheeled", "Stackable", "Set of 4"]
    },
    {
        "base_name": "Wall Clock",
        "description": "Modern wall clock with silent non-ticking movement and easy-to-read numbers",
        "variants": ["Modern", "Vintage", "Digital", "Analog", "Large", "Minimalist", "Wood", "Metal", "Silent", "Decorative"]
    },
    {
        "base_name": "Throw Pillows",
        "description": "Decorative throw pillows with soft fabric, hidden zipper, and machine washable covers",
        "variants": ["Set of 2", "Set of 4", "Velvet", "Linen", "Cotton", "Geometric", "Bohemian", "Modern", "Lumbar", "Outdoor"]
    },
    {
        "base_name": "Bath Towel Set",
        "description": "Luxury cotton bath towel set with high absorbency and quick-dry technology",
        "variants": ["2-Piece", "4-Piece", "6-Piece", "Egyptian Cotton", "Bamboo", "Microfiber", "Spa Quality", "Ultra Soft", "Quick Dry", "Premium"]
    },
    {
        "base_name": "Kitchen Knife Set",
        "description": "Professional stainless steel knife set with ergonomic handles and wooden block",
        "variants": ["5-Piece", "8-Piece", "12-Piece", "Chef's", "Ceramic", "Japanese", "German", "Damascus", "Block Set", "Magnetic Strip"]
    },
    {
        "base_name": "Cutting Board",
        "description": "Durable cutting board with juice groove, non-slip feet, and knife-friendly surface",
        "variants": ["Bamboo", "Wood", "Plastic", "Glass", "Large", "Set of 3", "Reversible", "With Handle", "Antimicrobial", "Extra Large"]
    },
    {
        "base_name": "Food Storage Containers",
        "description": "Airtight food storage containers with leak-proof lids, BPA-free and microwave safe",
        "variants": ["Glass", "Plastic", "Set of 10", "Set of 20", "Meal Prep", "Stackable", "Square", "Round", "With Dividers", "Color Coded"]
    },
    {
        "base_name": "Bedding Set",
        "description": "Complete bedding set including comforter, sheets, and pillowcases with soft microfiber",
        "variants": ["Queen", "King", "Twin", "Full", "California King", "Duvet Cover", "Cotton", "Microfiber", "Luxury", "Hotel Quality"]
    },
    {
        "base_name": "Area Rug",
        "description": "Soft area rug with non-slip backing, stain-resistant and easy to clean",
        "variants": ["3x5", "5x7", "8x10", "Runner", "Round", "Modern", "Traditional", "Shag", "Low Pile", "Washable"]
    },
    {
        "base_name": "Plant Pot",
        "description": "Decorative plant pot with drainage hole and matching saucer",
        "variants": ["Small", "Medium", "Large", "Ceramic", "Terracotta", "Modern", "Hanging", "Self-Watering", "Set of 3", "Indoor/Outdoor"]
    }
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
    "Fantastic! Looks great and works even better.",
    "Best purchase I've made in a while. Highly satisfied!",
    "Decent product for the price. Does the job.",
    "Good product overall. Minor issues but acceptable.",
    "Works as advertised. Happy with the purchase.",
    "Nice product. Quick delivery and well packaged.",
    "Pretty good. Met my expectations.",
    "Solid product. No complaints so far.",
    "It's okay. Gets the job done.",
    "Good enough for the price. Would recommend.",
    "Fair quality. Does what it's supposed to do.",
    "Acceptable product. Nothing special but works fine."
]

REVIEWER_NAMES = [
    "John Smith", "Emma Johnson", "Michael Brown", "Sophia Davis", "William Wilson",
    "Olivia Martinez", "James Anderson", "Ava Taylor", "Robert Thomas", "Isabella Garcia",
    "David Rodriguez", "Mia Hernandez", "Joseph Lopez", "Charlotte Gonzalez", "Daniel Perez",
    "Amelia Sanchez", "Matthew Ramirez", "Harper Torres", "Christopher Flores", "Evelyn Rivera"
]

async def generate_products():
    """Generate 1000+ products"""
    print("🚀 Starting massive store seed...")
    
    # Clear existing data
    await db.products.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing products and reviews")
    
    products = []
    product_count = 0
    
    # Generate Electronics products (500+)
    print("📱 Generating Electronics products...")
    for i in range(35):  # 35 iterations * 15 templates = 525 products
        for template in ELECTRONICS_PRODUCTS:
            for variant in template["variants"]:
                price = round(random.uniform(15.0, 299.0), 2)
                cost_price = round(price / 2.2, 2)  # Ensure good profit margin
                
                product = {
                    "id": str(uuid.uuid4()),
                    "name": f"{template['base_name']} {variant} v{i+1}",
                    "description": template["description"],
                    "price": price,
                    "cost_price": cost_price,
                    "image_url": f"https://images.unsplash.com/photo-{1500000000000 + random.randint(0, 999999999)}",
                    "images": [],
                    "category": "Electronics",
                    "subcategory": template["base_name"],
                    "stock": random.randint(50, 500),
                    "featured": random.random() < 0.05,
                    "daily_offer": random.random() < 0.03,
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "review_count": random.randint(5, 200),
                    "supplier": "cj_dropshipping",
                    "created_at": datetime.now().isoformat()
                }
                products.append(product)
                product_count += 1
                
                if product_count >= 525:
                    break
            if product_count >= 525:
                break
        if product_count >= 525:
            break
    
    print(f"✅ Generated {product_count} Electronics products")
    
    # Generate Home & Living products (500+)
    print("🏠 Generating Home & Living products...")
    home_count = 0
    for i in range(35):  # 35 iterations * 15 templates = 525 products
        for template in HOME_LIVING_PRODUCTS:
            for variant in template["variants"]:
                price = round(random.uniform(12.0, 199.0), 2)
                cost_price = round(price / 2.2, 2)
                
                product = {
                    "id": str(uuid.uuid4()),
                    "name": f"{template['base_name']} {variant} v{i+1}",
                    "description": template["description"],
                    "price": price,
                    "cost_price": cost_price,
                    "image_url": f"https://images.unsplash.com/photo-{1600000000000 + random.randint(0, 999999999)}",
                    "images": [],
                    "category": "Home & Living",
                    "subcategory": template["base_name"],
                    "stock": random.randint(50, 500),
                    "featured": random.random() < 0.05,
                    "daily_offer": random.random() < 0.03,
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "review_count": random.randint(5, 200),
                    "supplier": "cj_dropshipping",
                    "created_at": datetime.now().isoformat()
                }
                products.append(product)
                home_count += 1
                
                if home_count >= 525:
                    break
            if home_count >= 525:
                break
        if home_count >= 525:
            break
    
    print(f"✅ Generated {home_count} Home & Living products")
    
    # Insert all products
    if products:
        await db.products.insert_many(products)
        print(f"💾 Inserted {len(products)} products into database")
    
    # Generate reviews for random products (sample)
    print("💬 Generating reviews...")
    reviews = []
    sample_products = random.sample(products, min(300, len(products)))  # Reviews for 300 products
    
    for product in sample_products:
        num_reviews = random.randint(3, 15)
        for _ in range(num_reviews):
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_id": None,
                "user_name": random.choice(REVIEWER_NAMES),
                "rating": random.randint(3, 5),
                "comment": random.choice(REVIEW_TEMPLATES),
                "verified_purchase": random.random() < 0.8,
                "helpful_count": random.randint(0, 50),
                "created_at": datetime.now().isoformat()
            }
            reviews.append(review)
    
    if reviews:
        await db.reviews.insert_many(reviews)
        print(f"✅ Added {len(reviews)} reviews")
    
    print("\n🎉 Massive store seed complete!")
    print(f"📦 Total: {len(products)} products")
    print(f"💬 Total: {len(reviews)} reviews")
    print(f"📁 Categories: Electronics ({product_count}), Home & Living ({home_count})")

if __name__ == "__main__":
    asyncio.run(generate_products())
