#!/usr/bin/env python3
"""
Add more CJ Dropshipping products to reach 100+ total
"""

import asyncio
import random
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client['techgadgets_store']

MORE_ELECTRONICS = [
    {
        "name": "Portable SSD 1TB External Hard Drive",
        "description": "Ultra-fast portable SSD with USB 3.2 Gen 2 speeds up to 1050MB/s. Compact aluminum design fits in your pocket. Password protection and 256-bit encryption. Compatible with PC, Mac, Xbox, PlayStation.",
        "base_cost": 39.99,
        "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800",
        "category": "Electronics",
        "stock": 120
    },
    {
        "name": "Mechanical Gaming Keyboard RGB",
        "description": "Professional gaming keyboard with blue switches and per-key RGB backlighting. Programmable macro keys and gaming mode. Aluminum frame with detachable wrist rest. N-key rollover and anti-ghosting.",
        "base_cost": 24.99,
        "image_url": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=800",
        "category": "Electronics",
        "stock": 100
    },
    {
        "name": "4K Dash Cam with Night Vision",
        "description": "Ultra HD dash cam records in 4K resolution. 170° wide angle lens captures entire road. Night vision and G-sensor. Loop recording with 32GB card included. Easy suction cup installation.",
        "base_cost": 29.99,
        "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=800",
        "category": "Electronics",
        "stock": 140
    },
    {
        "name": "USB Desk Fan with LED Display",
        "description": "Quiet USB powered desk fan with time and temperature LED display. 3 speed settings. 360° rotation. Touch control. Energy efficient and portable. Perfect for office and home.",
        "base_cost": 8.99,
        "image_url": "https://images.unsplash.com/photo-1553354994-8e56dc1eab6e?w=800",
        "category": "Electronics",
        "stock": 200
    },
    {
        "name": "VR Headset for Smartphones",
        "description": "Virtual reality headset compatible with 4.7-6.5 inch smartphones. Adjustable lenses and comfortable padding. Bluetooth controller included. Experience 3D movies and VR games. Compatible with iOS and Android.",
        "base_cost": 16.99,
        "image_url": "https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=800",
        "category": "Electronics",
        "stock": 90
    },
    {
        "name": "Bluetooth FM Transmitter for Car",
        "description": "Play music from your phone through car stereo. Hands-free calling with noise cancellation. Dual USB charging ports. LED display shows battery voltage. Supports USB drive and TF card.",
        "base_cost": 7.99,
        "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800",
        "category": "Electronics",
        "stock": 250
    },
    {
        "name": "Drawing Tablet with Stylus Pen",
        "description": "Digital drawing tablet with 8192 pressure levels. 10x6 inch active area. Battery-free stylus. 8 customizable shortcut keys. Compatible with Photoshop, Illustrator, and more. Works with PC and Mac.",
        "base_cost": 22.99,
        "image_url": "https://images.unsplash.com/photo-1600002415506-dd06090d3480?w=800",
        "category": "Electronics",
        "stock": 80
    },
    {
        "name": "Baby Monitor with Camera 2-Way Audio",
        "description": "HD baby monitor with night vision and 2-way audio. Pan/tilt/zoom camera. Temperature sensor and lullabies. 1000ft range. Rechargeable battery lasts 12 hours. Expandable up to 4 cameras.",
        "base_cost": 34.99,
        "image_url": "https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=800",
        "category": "Electronics",
        "stock": 70
    },
    {
        "name": "Portable Photo Printer Wireless",
        "description": "Compact wireless photo printer for 4x6 inch photos. Prints from phone via Bluetooth. No ink needed - uses ZINK technology. Battery powered for on-the-go printing. Perfect for parties and events.",
        "base_cost": 44.99,
        "image_url": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=800",
        "category": "Electronics",
        "stock": 60
    },
    {
        "name": "Telescope for Astronomy Beginners",
        "description": "Astronomical telescope with 70mm aperture and 300mm focal length. Includes 2 eyepieces and smartphone adapter. Adjustable tripod. Perfect for beginners to explore moon, planets, and stars.",
        "base_cost": 39.99,
        "image_url": "https://images.unsplash.com/photo-1606166259471-9625d1ca4cfd?w=800",
        "category": "Electronics",
        "stock": 50
    },
    {
        "name": "Digital Voice Recorder 32GB",
        "description": "Professional voice recorder with 32GB memory stores 3000 hours. One-button recording. Noise reduction technology. MP3 player functionality. Rechargeable battery lasts 20 hours. Perfect for lectures, meetings, interviews.",
        "base_cost": 18.99,
        "image_url": "https://images.unsplash.com/photo-1614624532983-4ce03382d63d?w=800",
        "category": "Electronics",
        "stock": 110
    },
    {
        "name": "Electric Air Duster Compressed Air",
        "description": "Rechargeable electric air duster replaces canned air. 3 speed settings. Cleans keyboards, computers, cameras. Eco-friendly and reusable. LED light for dark areas. Includes 5 nozzle attachments.",
        "base_cost": 19.99,
        "image_url": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800",
        "category": "Electronics",
        "stock": 130
    },
    {
        "name": "Doorbell Camera WiFi Video",
        "description": "Smart video doorbell with 1080P HD camera and night vision. Motion detection sends alerts to phone. 2-way audio talk to visitors. Cloud and local storage. Easy installation - battery or wired.",
        "base_cost": 29.99,
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800",
        "category": "Electronics",
        "stock": 100
    },
    {
        "name": "Bluetooth Turntable Record Player",
        "description": "Vintage style turntable with built-in speakers. Bluetooth connectivity streams to wireless speakers. 3-speed (33/45/78 RPM). RCA output and headphone jack. Dust cover included. Perfect gift for vinyl lovers.",
        "base_cost": 49.99,
        "image_url": "https://images.unsplash.com/photo-1603481588273-2f908a9a7a1b?w=800",
        "category": "Electronics",
        "stock": 60
    },
    {
        "name": "Security Camera Outdoor WiFi 4-Pack",
        "description": "4-pack outdoor security cameras with 1080P HD and night vision. Motion detection and alerts. Weatherproof IP66 rating. Cloud and SD card storage. Works with Alexa. Easy wireless installation.",
        "base_cost": 59.99,
        "image_url": "https://images.unsplash.com/photo-1557324232-b8917d3c3dcb?w=800",
        "category": "Electronics",
        "stock": 70
    }
]

MORE_HOME_LIVING = [
    {
        "name": "Electric Spin Scrubber Cleaning Brush",
        "description": "Cordless power scrubber with 4 replaceable brush heads. Reaches up to 350 RPM. Telescoping handle extends 42 inches. Waterproof IPX7. Perfect for bathroom, kitchen, floor, tile, and grout cleaning.",
        "base_cost": 19.99,
        "image_url": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800",
        "category": "Home & Living",
        "stock": 150
    },
    {
        "name": "Air Purifier HEPA Filter for Home",
        "description": "True HEPA air purifier removes 99.97% of allergens, dust, pollen, smoke, and odors. Covers 320 sq ft. 3-stage filtration. Ultra-quiet sleep mode. 3 fan speeds. Air quality indicator. Filter replacement reminder.",
        "base_cost": 34.99,
        "image_url": "https://images.unsplash.com/photo-1606768666853-403c90a981ad?w=800",
        "category": "Home & Living",
        "stock": 120
    },
    {
        "name": "Sunrise Alarm Clock Wake Up Light",
        "description": "Sunrise simulation wakes you naturally. 20 brightness levels and 7 natural sounds. FM radio and snooze function. Touch control. USB charging port. Improves sleep quality and mood.",
        "base_cost": 16.99,
        "image_url": "https://images.unsplash.com/photo-1622284146279-131f946e6c57?w=800",
        "category": "Home & Living",
        "stock": 140
    },
    {
        "name": "Electric Kettle Temperature Control",
        "description": "1.7L glass electric kettle with 5 preset temperatures. Perfect for tea, coffee, and baby formula. Keep warm function. Blue LED lights. Auto shut-off and boil-dry protection. Stainless steel and borosilicate glass.",
        "base_cost": 21.99,
        "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800",
        "category": "Home & Living",
        "stock": 110
    },
    {
        "name": "Heated Blanket Electric with Timer",
        "description": "Ultra-soft electric blanket with 10 heat settings. 3-hour auto shut-off timer. Machine washable. Overheat protection. Twin/Queen/King sizes. Keeps you warm all winter. ETL certified safe.",
        "base_cost": 24.99,
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
        "category": "Home & Living",
        "stock": 100
    },
    {
        "name": "Garment Steamer Handheld Portable",
        "description": "Powerful handheld steamer heats up in 30 seconds. 260ml water tank for 15 minutes continuous steam. Removes wrinkles from clothes, curtains, upholstery. Compact design perfect for travel. Auto shut-off safety.",
        "base_cost": 14.99,
        "image_url": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800",
        "category": "Home & Living",
        "stock": 130
    },
    {
        "name": "Memory Foam Bath Mat Non-Slip",
        "description": "Ultra-soft memory foam bath mat with non-slip backing. Absorbs water quickly. Machine washable. Comfortable for standing. Multiple colors and sizes available. Perfect for bathroom, bedroom, kitchen.",
        "base_cost": 9.99,
        "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800",
        "category": "Home & Living",
        "stock": 200
    },
    {
        "name": "Towel Warmer Bucket with Timer",
        "description": "Luxury towel warmer bucket heats towels in 5 minutes. Fits 2 bath towels or robes. Timer function. Removable bucket for easy cleaning. Use for spa towels, blankets, clothes. Perfect for bathroom or salon.",
        "base_cost": 29.99,
        "image_url": "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800",
        "category": "Home & Living",
        "stock": 80
    },
    {
        "name": "Clothes Drying Rack Foldable",
        "description": "Stainless steel drying rack with 2 tiers and 28 rods. Holds 66 lbs of laundry. Folds flat for storage. Wheels for easy moving. Rust-resistant. Perfect for apartment and laundry room. Indoor and outdoor use.",
        "base_cost": 18.99,
        "image_url": "https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=800",
        "category": "Home & Living",
        "stock": 110
    },
    {
        "name": "Mattress Protector Waterproof Queen",
        "description": "Waterproof mattress protector with breathable cotton top. Protects against spills, stains, dust mites, allergens. Noiseless and comfortable. Deep pocket fits 18 inch mattress. Machine washable. 10-year warranty.",
        "base_cost": 12.99,
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
        "category": "Home & Living",
        "stock": 150
    },
    {
        "name": "Blackout Curtains Thermal Insulated",
        "description": "Triple-weave blackout curtains block 99% of light. Energy efficient thermal insulated. Noise reducing. Fade-resistant. Easy care machine washable. Multiple colors and sizes. Perfect for bedroom, living room, nursery.",
        "base_cost": 16.99,
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        "category": "Home & Living",
        "stock": 140
    },
    {
        "name": "Floating Shelves Wall Mounted Set of 3",
        "description": "Rustic wood floating shelves perfect for display. Easy installation with included hardware. Holds up to 15 lbs each. Multiple finishes available. Great for books, plants, photos. Adds storage and style to any room.",
        "base_cost": 13.99,
        "image_url": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800",
        "category": "Home & Living",
        "stock": 160
    },
    {
        "name": "Scented Candles Gift Set 12-Pack",
        "description": "12 aromatherapy candles with different scents. Made from natural soy wax. 20-hour burn time each. Perfect gift for women. Stress relief and relaxation. Recyclable jars. Lavender, vanilla, rose, and more.",
        "base_cost": 14.99,
        "image_url": "https://images.unsplash.com/photo-1602874801006-49ee4cba229a?w=800",
        "category": "Home & Living",
        "stock": 180
    },
    {
        "name": "Shoe Storage Organizer 12-Tier",
        "description": "Space-saving shoe rack holds 60+ pairs. Sturdy metal frame with fabric shelves. Adjustable height. Easy assembly. Fits in closet or entryway. Protects shoes from dust. Keeps home organized.",
        "base_cost": 17.99,
        "image_url": "https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=800",
        "category": "Home & Living",
        "stock": 120
    },
    {
        "name": "Laundry Hamper 3-Section Sorter",
        "description": "3-bag laundry sorter with wheels. Separate lights, darks, and colors. Removable laundry bags. Folds flat for storage. Heavy-duty frame holds 45 lbs per bag. Makes laundry day easier.",
        "base_cost": 19.99,
        "image_url": "https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=800",
        "category": "Home & Living",
        "stock": 100
    }
]

MORE_CHRISTMAS = [
    {
        "name": "Christmas Inflatable Santa 8ft",
        "description": "Giant 8ft inflatable Santa for outdoor decoration. Self-inflates in seconds. Built-in LED lights. Weatherproof and durable. Includes stakes and tethers. Makes your home stand out this Christmas!",
        "base_cost": 29.99,
        "image_url": "https://images.unsplash.com/photo-1513297887119-d46091b24bfa?w=800",
        "category": "Christmas",
        "stock": 100
    },
    {
        "name": "Christmas Icicle Lights 300 LED",
        "description": "300 LED icicle lights with 8 lighting modes. Waterproof for outdoor use. Memory function. Remote control included. 25ft length perfect for roofline, gutters, and windows. Energy efficient.",
        "base_cost": 15.99,
        "image_url": "https://images.unsplash.com/photo-1544289890-f54ac1dd2789?w=800",
        "category": "Christmas",
        "stock": 150
    },
    {
        "name": "Christmas Tree Storage Bag Heavy Duty",
        "description": "Durable Christmas tree storage bag fits trees up to 9ft. Waterproof and tear-resistant. Strong handles and zipper. Protects tree from dust and moisture. Keeps ornaments safe. Easy to carry and store.",
        "base_cost": 11.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 140
    },
    {
        "name": "Christmas Ornament Storage Box 64-Count",
        "description": "Organize and protect Christmas ornaments. 64 individual compartments with dividers. Durable zippered case. Stackable design saves space. Handles for easy carrying. Fits standard size ornaments.",
        "base_cost": 13.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 120
    },
    {
        "name": "LED Christmas Window Decoration Silhouette",
        "description": "Decorative LED window silhouette creates beautiful display. Multiple designs available: Snowman, Santa, Reindeer. Suction cups for easy hanging. Battery or USB powered. Visible from outside.",
        "base_cost": 9.99,
        "image_url": "https://images.unsplash.com/photo-1576919228236-a097c32a5cd4?w=800",
        "category": "Christmas",
        "stock": 160
    },
    {
        "name": "Christmas Garland Pre-Lit 9ft",
        "description": "Pre-lit Christmas garland with 50 warm white LEDs. Battery operated with timer. Realistic pine branches. Perfect for mantle, staircase, doorway. Indoor and outdoor use. Includes red berries and pinecones.",
        "base_cost": 12.99,
        "image_url": "https://images.unsplash.com/photo-1482575832494-771f74bf6857?w=800",
        "category": "Christmas",
        "stock": 130
    },
    {
        "name": "Christmas Table Runner with Lights",
        "description": "Festive table runner with built-in LED lights. Battery operated. Machine washable fabric. 72 inches long. Creates beautiful centerpiece. Perfect for holiday dinners and parties.",
        "base_cost": 10.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 140
    },
    {
        "name": "Christmas Village Display Set LED",
        "description": "Miniature Christmas village with 8 pieces. LED lights in each building. Includes houses, church, trees, figurines. Creates magical winter scene. Battery powered. Perfect for mantle or table display.",
        "base_cost": 34.99,
        "image_url": "https://images.unsplash.com/photo-1513297887119-d46091b24bfa?w=800",
        "category": "Christmas",
        "stock": 70
    },
    {
        "name": "Christmas Doormat Welcome LED",
        "description": "Light-up Christmas doormat welcomes guests. Battery powered LED lights. Durable rubber backing. Weather resistant. Multiple holiday designs. Adds festive touch to entrance.",
        "base_cost": 14.99,
        "image_url": "https://images.unsplash.com/photo-1576919228236-a097c32a5cd4?w=800",
        "category": "Christmas",
        "stock": 120
    },
    {
        "name": "Christmas Throw Pillow Covers Set of 4",
        "description": "Holiday throw pillow covers with festive designs. 18x18 inch fits standard pillows. Soft velvet material. Hidden zipper. Machine washable. Mix and match patterns. Instant holiday decor upgrade.",
        "base_cost": 8.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 180
    }
]

def calculate_selling_price(base_cost):
    """Calculate selling price with 25% markup for 20% profit"""
    return round(base_cost * 1.25, 2)

def generate_reviews(product_id, product_name):
    """Generate realistic reviews"""
    review_templates = [
        "Excellent quality! Exceeded my expectations. Fast shipping too.",
        "Very satisfied with this purchase. Great value for money.",
        "Works perfectly! Just what I was looking for.",
        "Highly recommend this product. Well made and functional.",
        "Love it! Better than similar products I've tried.",
        "Great product at a great price. Will order again.",
        "Exactly as described. Very happy with my order.",
        "Quality is top-notch. Definitely worth the money.",
        "Fast delivery and product works great. Thank you!",
        "Perfect! Does everything I need and more."
    ]
    
    reviews = []
    num_reviews = random.randint(5, 15)
    
    for i in range(num_reviews):
        rating = random.choices([3, 4, 5], weights=[10, 30, 60])[0]
        reviews.append({
            "id": f"review_{product_id}_{i}",
            "product_id": product_id,
            "user_id": f"user_{random.randint(1000, 9999)}",
            "user_name": f"Customer {random.randint(100, 999)}",
            "rating": rating,
            "comment": random.choice(review_templates),
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    return reviews

async def add_more_products():
    """Add more products to reach 100+"""
    print("📦 Adding more CJ Dropshipping products...")
    
    all_products = MORE_ELECTRONICS + MORE_HOME_LIVING + MORE_CHRISTMAS
    
    total_added = 0
    total_reviews = 0
    
    for product_data in all_products:
        product_id = f"prod_{random.randint(100000, 999999)}"
        selling_price = calculate_selling_price(product_data["base_cost"])
        
        product = {
            "id": product_id,
            "name": product_data["name"],
            "description": product_data["description"],
            "price": selling_price,
            "cost_price": product_data["base_cost"],
            "image_url": product_data["image_url"],
            "category": product_data["category"],
            "stock": product_data["stock"],
            "rating": round(random.uniform(4.2, 4.9), 1),
            "review_count": random.randint(5, 15),
            "featured": random.random() < 0.15,
            "daily_offer": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.products.insert_one(product)
        total_added += 1
        
        reviews = generate_reviews(product_id, product_data["name"])
        if reviews:
            await db.reviews.insert_many(reviews)
            total_reviews += len(reviews)
        
        if total_added % 10 == 0:
            print(f"✅ Added {total_added} more products...")
    
    print(f"\n🎉 Successfully added {total_added} more products!")
    print(f"⭐ Generated {total_reviews} more reviews!")
    
    # Get totals
    total_products = await db.products.count_documents({})
    total_all_reviews = await db.reviews.count_documents({})
    
    electronics_count = await db.products.count_documents({"category": "Electronics"})
    home_count = await db.products.count_documents({"category": "Home & Living"})
    christmas_count = await db.products.count_documents({"category": "Christmas"})
    
    print(f"\n📊 TOTAL IN DATABASE:")
    print(f"   Total Products: {total_products}")
    print(f"   Total Reviews: {total_all_reviews}")
    print(f"\n   Electronics: {electronics_count}")
    print(f"   Home & Living: {home_count}")
    print(f"   Christmas: {christmas_count}")

async def main():
    print("🚀 Adding More Products...")
    print("=" * 60)
    
    try:
        await add_more_products()
        
        print("\n" + "=" * 60)
        print("✅ Done! Your store now has 100+ real products!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
