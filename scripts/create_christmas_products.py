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

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Christmas product templates
CHRISTMAS_PRODUCTS = [
    ("Christmas LED String Lights", "Warm white LED string lights perfect for decorating your home during the holiday season"),
    ("Santa Claus Costume Set", "Complete Santa costume with hat, beard, jacket, pants, belt and boot covers"),
    ("Christmas Tree Ornament Set", "Beautiful glass ornaments in various colors and designs to decorate your Christmas tree"),
    ("Holiday Door Wreath", "Festive Christmas wreath with pine cones, berries and red ribbon for your front door"),
    ("Christmas Snow Globe", "Musical snow globe with Christmas scene inside, plays holiday melodies"),
    ("Reindeer Garden Decoration", "Light-up reindeer decoration for your garden or yard during Christmas"),
    ("Christmas Candle Set", "Scented Christmas candles with pine, cinnamon and vanilla fragrances"),
    ("Holiday Table Runner", "Festive table runner with Christmas patterns for your dining table"),
    ("Christmas Cookie Cutters", "Set of holiday-themed cookie cutters in various Christmas shapes"),
    ("Santa Hat for Adults", "Classic red Santa hat with white fur trim and pompom"),
    ("Christmas Stockings Set", "Traditional Christmas stockings to hang by the fireplace"),
    ("Holiday Throw Pillow", "Decorative Christmas pillow with festive designs and sayings"),
    ("Christmas Tree Topper", "Beautiful star or angel tree topper to crown your Christmas tree"),
    ("Holiday Mug Set", "Christmas-themed mugs perfect for hot cocoa and holiday drinks"),
    ("Christmas Advent Calendar", "24-day advent calendar with small gifts and treats"),
    ("Holiday Sweater Ugly Christmas", "Funny ugly Christmas sweater with festive patterns"),
    ("Christmas Village Set", "Miniature Christmas village houses with LED lights"),
    ("Holiday Garland Decoration", "Pine garland with lights and ornaments for decorating"),
    ("Christmas Tree Skirt", "Decorative skirt to place under your Christmas tree"),
    ("Holiday Gift Wrap Set", "Beautiful Christmas wrapping paper with ribbons and tags"),
    ("Christmas Nutcracker Decoration", "Traditional wooden nutcracker soldier decoration"),
    ("Holiday Window Clings", "Removable Christmas window decorations and stickers"),
    ("Christmas Tree Lights", "Multi-color LED lights for decorating your Christmas tree"),
    ("Holiday Centerpiece", "Festive Christmas centerpiece with candles and decorations"),
    ("Christmas Pajama Set", "Cozy Christmas-themed pajamas for the whole family"),
    ("Holiday Cookie Jar", "Christmas-themed cookie jar to store your holiday treats"),
    ("Christmas Wall Decals", "Removable Christmas wall stickers and decorations"),
    ("Holiday Placemats Set", "Christmas-themed placemats for your holiday dining table"),
    ("Christmas Music Box", "Musical Christmas decoration that plays holiday songs"),
    ("Holiday Salt and Pepper Shakers", "Christmas-themed salt and pepper shaker set")
]

CHRISTMAS_IMAGES = [
    "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=400&h=400&fit=crop",  # Christmas lights
    "https://images.unsplash.com/photo-1544273677-6e2e8e4eba88?w=400&h=400&fit=crop",    # Santa costume
    "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",  # Christmas ornaments
    "https://images.unsplash.com/photo-1544273677-5c7e2c2d05a7?w=400&h=400&fit=crop",    # Christmas wreath
    "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop",  # Christmas decorations
    "https://images.unsplash.com/photo-1543589077-47d81606c1bf?w=400&h=400&fit=crop",    # Christmas reindeer
    "https://images.unsplash.com/photo-1512389098783-66b81f86e199?w=400&h=400&fit=crop",  # Christmas candles
    "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=400&h=400&fit=crop",    # Christmas table
    "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",  # Christmas cookies
    "https://images.unsplash.com/photo-1512909444218-3c2aa16ab6b6?w=400&h=400&fit=crop",  # Santa hat
    "https://images.unsplash.com/photo-1544273677-2272bddc8ff6?w=400&h=400&fit=crop",    # Christmas stockings
    "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",  # Christmas pillows
    "https://images.unsplash.com/photo-1544273677-fa5850ab9a0b?w=400&h=400&fit=crop",    # Christmas tree topper
    "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop",  # Christmas mugs
    "https://images.unsplash.com/photo-1543589077-47d81606c1bf?w=400&h=400&fit=crop",    # Advent calendar
    "https://images.unsplash.com/photo-1544273677-c433b8c2e2e9?w=400&h=400&fit=crop",    # Christmas sweater
    "https://images.unsplash.com/photo-1512317049220-d3c6fcaf6681?w=400&h=400&fit=crop",  # Christmas village
    "https://images.unsplash.com/photo-1544273677-abc8a3bb4a84?w=400&h=400&fit=crop",    # Christmas garland
    "https://images.unsplash.com/photo-1544273677-2272bddc8ff6?w=400&h=400&fit=crop",    # Christmas tree skirt
    "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=400&fit=crop",  # Gift wrap
]

REVIEW_TEMPLATES = [
    "Perfect for Christmas! Great quality and fast shipping.",
    "Love this Christmas decoration! Exactly what I was looking for.",
    "Amazing Christmas product! My family loves it.",
    "Great value for money. Perfect for the holidays!",
    "Beautiful Christmas item. Highly recommend!",
    "Excellent quality Christmas decoration. Very satisfied!",
    "Perfect Christmas gift! Arrived quickly and well packaged.",
    "Love this holiday item! Makes my home feel festive."
]

REVIEWER_NAMES = [
    "Maria K.", "John D.", "Sarah M.", "Mike R.", "Anna L.",
    "David P.", "Emma W.", "Chris B.", "Lisa H.", "Tom S."
]

async def create_christmas_products():
    """Create 300+ Christmas products"""
    print("🎄 Creating Christmas products...")
    
    products = []
    
    # Generate 300+ Christmas products (10 variations per template)
    for i in range(10):  # 10 iterations
        for idx, (name, description) in enumerate(CHRISTMAS_PRODUCTS):
            price = round(random.uniform(9.99, 89.99), 2)
            cost_price = round(price / 2.5, 2)  # Good profit margin
            
            product = {
                "id": str(uuid.uuid4()),
                "name": f"{name} {['Classic', 'Premium', 'Deluxe', 'Traditional', 'Modern', 'Festive', 'Holiday', 'Special', 'Elegant', 'Luxury'][i]}",
                "description": f"{description} - Perfect for making your Christmas celebrations extra special!",
                "price": price,
                "cost_price": cost_price,
                "image_url": CHRISTMAS_IMAGES[idx % len(CHRISTMAS_IMAGES)],
                "images": [],
                "category": "Christmas",
                "subcategory": "Christmas Decorations",
                "stock": random.randint(20, 200),
                "featured": True,  # All Christmas items are featured
                "daily_offer": random.random() < 0.15,  # 15% chance of daily offer
                "rating": round(random.uniform(4.2, 5.0), 1),
                "review_count": random.randint(15, 180),
                "supplier": "christmas_supplier",
                "created_at": datetime.now().isoformat()
            }
            products.append(product)
    
    # Insert Christmas products
    if products:
        await db.products.insert_many(products)
        print(f"✅ Created {len(products)} Christmas products")
    
    # Generate reviews for Christmas products
    print("💬 Generating Christmas reviews...")
    reviews = []
    sample_products = random.sample(products, min(200, len(products)))
    
    for product in sample_products:
        num_reviews = random.randint(8, 20)
        for _ in range(num_reviews):
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_id": None,
                "user_name": random.choice(REVIEWER_NAMES),
                "rating": random.randint(4, 5),
                "comment": random.choice(REVIEW_TEMPLATES),
                "verified_purchase": random.random() < 0.9,
                "helpful_count": random.randint(1, 25),
                "created_at": datetime.now().isoformat()
            }
            reviews.append(review)
    
    if reviews:
        await db.reviews.insert_many(reviews)
        print(f"✅ Added {len(reviews)} Christmas reviews")
    
    print(f"🎄 Christmas store ready with {len(products)} products!")

if __name__ == "__main__":
    asyncio.run(create_christmas_products())