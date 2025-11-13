#!/usr/bin/env python3
"""
Add more detailed products with realistic descriptions for each category
"""

import asyncio
import random
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client['techgadgets_store']

DETAILED_ELECTRONICS = [
    {
        "name": "4K Action Camera Waterproof 20MP",
        "description": "Professional 4K action camera with 20MP photos and ultra HD video recording. Features built-in WiFi for instant sharing, 170° wide-angle lens, and waterproof up to 30 meters without case. Includes wireless remote control, 2 rechargeable batteries (90 mins each), mounting accessories kit, and protective carrying case. Perfect for surfing, skiing, biking, diving, and all extreme sports. Time-lapse and slow-motion modes available.",
        "base_cost": 34.99,
        "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800",
        "category": "Electronics",
        "stock": 95
    },
    {
        "name": "Bluetooth Karaoke Microphone with Speaker",
        "description": "Wireless karaoke microphone with built-in Bluetooth speaker. Features echo control, voice changer with 5 different effects, and LED lights that sync with music. Compatible with all smartphones and tablets. Rechargeable battery lasts 6-8 hours. Perfect for parties, family gatherings, and karaoke nights. Comes with carrying case. Works with YouTube, Spotify, and all karaoke apps.",
        "base_cost": 16.99,
        "image_url": "https://images.unsplash.com/photo-1589003077984-894e133dabab?w=800",
        "category": "Electronics",
        "stock": 130
    },
    {
        "name": "LED Desk Lamp with USB Charging Port",
        "description": "Modern LED desk lamp with adjustable brightness (5 levels) and color temperature (3 modes: warm, natural, cool white). Built-in USB charging port for phones and tablets. Touch control panel with memory function remembers your last setting. Energy-efficient LED lasts 50,000 hours. Flexible gooseneck adjusts to any angle. Perfect for home office, studying, reading. Eye-caring flicker-free light reduces eye strain.",
        "base_cost": 13.99,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800",
        "category": "Electronics",
        "stock": 150
    },
    {
        "name": "Electric Toothbrush with 8 Brush Heads",
        "description": "Rechargeable sonic electric toothbrush with 40,000 vibrations per minute. Features 5 brushing modes: clean, white, polish, gum care, and sensitive. Smart timer with 30-second intervals ensures proper brushing. Includes 8 replacement brush heads (2-year supply), charging base, and travel case. Battery lasts 30 days on single charge. Waterproof IPX7 rated safe for shower use. Dentist recommended for superior plaque removal.",
        "base_cost": 19.99,
        "image_url": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=800",
        "category": "Electronics",
        "stock": 110
    },
    {
        "name": "Wireless Presenter Remote with Laser Pointer",
        "description": "Professional wireless presenter clicker with red laser pointer. Works up to 100 feet range. Hyperlink and volume control buttons. USB receiver stores inside the remote. Plug-and-play, no software needed. Compatible with Windows, Mac, PowerPoint, Keynote, Google Slides, PDF. Perfect for teachers, business presentations, lectures. Includes storage pouch and batteries.",
        "base_cost": 11.99,
        "image_url": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=800",
        "category": "Electronics",
        "stock": 140
    },
    {
        "name": "Bluetooth Sleep Headphones Eye Mask",
        "description": "3D sleep mask with built-in Bluetooth headphones. Ultra-soft memory foam blocks 100% light for deep sleep. Wireless headphones let you listen to music, audiobooks, meditation without earbuds. Rechargeable battery lasts 10+ hours. Perfect for sleeping, traveling, meditation, yoga, insomnia. Adjustable velcro strap fits all head sizes. Machine washable after removing speakers.",
        "base_cost": 14.99,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
        "category": "Electronics",
        "stock": 120
    },
    {
        "name": "Digital Bathroom Scale with Body Composition",
        "description": "Smart bathroom scale measures weight, BMI, body fat %, muscle mass, bone mass, water %, and more. Connects to smartphone app via Bluetooth to track progress. Tempered glass platform supports up to 400 lbs. High-precision sensors accurate to 0.2 lbs. Auto-calibration and auto on/off. Unlimited users. Includes baby weighing mode. Battery included.",
        "base_cost": 17.99,
        "image_url": "https://images.unsplash.com/photo-1576669801945-7a346954da5a?w=800",
        "category": "Electronics",
        "stock": 100
    },
    {
        "name": "Cordless Handheld Vacuum Cleaner",
        "description": "Powerful cordless hand vacuum with 120W motor and strong suction. Washable HEPA filter traps 99.97% of dust and allergens. Lightweight design weighs only 1.3 lbs. Rechargeable battery provides 30 minutes runtime. LED light illuminates dark corners. Multiple attachments: crevice tool, brush nozzle, extension tube. Perfect for car, stairs, furniture, pet hair. Quick-empty dustbin.",
        "base_cost": 22.99,
        "image_url": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800",
        "category": "Electronics",
        "stock": 105
    }
]

DETAILED_HOME_LIVING = [
    {
        "name": "Electric Milk Frother Handheld 3-in-1",
        "description": "Versatile electric milk frother creates café-quality foam at home. 3 whisks included: frother for cappuccino foam, stirrer for hot chocolate, and whisk for matcha. USB rechargeable lasts 30+ uses per charge. Powerful motor froths milk in 15-20 seconds. Quiet operation. Double spring design prevents splashing. Stainless steel whisk. Perfect for lattes, cappuccinos, bulletproof coffee, matcha, protein shakes. Stand and cleaning brush included.",
        "base_cost": 8.99,
        "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800",
        "category": "Home & Living",
        "stock": 180
    },
    {
        "name": "Shower Head with High Pressure 5 Spray Settings",
        "description": "Luxury rain shower head with 5 spray modes: power rain, massage, power mist, pulsating massage, and mixed. Self-cleaning nozzles prevent clogging. High-pressure design works great even in low water pressure homes. Universal fit installs in minutes without tools. Premium chrome finish resists corrosion. Water-saving design reduces water usage by 30%. Includes Teflon tape and instructions. 10-year warranty.",
        "base_cost": 12.99,
        "image_url": "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800",
        "category": "Home & Living",
        "stock": 140
    },
    {
        "name": "Knife Sharpener Electric 2-Stage Professional",
        "description": "Electric knife sharpener with 2-stage sharpening system. Stage 1: diamond-coated wheels create edge. Stage 2: ceramic wheels hone razor-sharp finish. Sharpens all types: chef knives, kitchen knives, pocket knives, hunting knives. Non-slip rubber feet keep stable. Simple operation - just pull knife through slots. Fast 3-10 strokes restore dull blades. Safer than manual sharpeners. Includes user guide.",
        "base_cost": 18.99,
        "image_url": "https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=800",
        "category": "Home & Living",
        "stock": 110
    },
    {
        "name": "Stainless Steel Dish Drying Rack Over Sink",
        "description": "Premium over-the-sink dish rack maximizes counter space. Made from rust-proof 304 stainless steel. Adjustable arms fit sinks 25-37 inches. 2-tier design with utensil holder, cutting board slot, and wine glass rack. Drain board directs water into sink. Holds dishes, glasses, pots, pans. Heavy-duty construction supports up to 55 lbs. Easy assembly. Modern design complements any kitchen.",
        "base_cost": 24.99,
        "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800",
        "category": "Home & Living",
        "stock": 90
    },
    {
        "name": "Pillow Cooling Gel Memory Foam King Size",
        "description": "Premium memory foam pillow with cooling gel layer regulates temperature all night. Ventilated design increases airflow. Adjustable loft - remove foam to customize height. Ergonomic contour supports neck and spine. Hypoallergenic and dust mite resistant. Breathable bamboo-derived cover is removable and machine washable. CertiPUR-US certified foam. Perfect for side, back, and stomach sleepers. Includes zippered travel bag.",
        "base_cost": 21.99,
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
        "category": "Home & Living",
        "stock": 100
    },
    {
        "name": "Spice Rack Organizer with 30 Glass Jars",
        "description": "Complete spice organization system with 30 identical glass jars (4 oz each). Airtight metal lids keep spices fresh. Each jar includes shaker lid and regular lid. Pre-printed labels included (180+ spice names). Square jars stack perfectly saving cabinet space. Bamboo rack available separately or stores flat in drawer. Dishwasher safe jars. Chalk marker included for custom labels. Transforms cluttered spice cabinet.",
        "base_cost": 19.99,
        "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f?w=800",
        "category": "Home & Living",
        "stock": 120
    },
    {
        "name": "Bathroom Accessories Set 6-Piece Stainless Steel",
        "description": "Luxury bathroom accessory set includes: toothbrush holder, soap dish, soap dispenser, tumbler cup, toilet brush with holder, and towel ring. Made from brushed stainless steel - rust and corrosion resistant. Modern sleek design complements any décor. No assembly required. Easy to clean - just wipe with damp cloth. Weighted bases prevent tipping. Hotel-quality construction. Perfect for bathroom makeover or new home.",
        "base_cost": 27.99,
        "image_url": "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800",
        "category": "Home & Living",
        "stock": 85
    },
    {
        "name": "Food Storage Containers Set 24-Piece BPA-Free",
        "description": "Complete meal prep container set with 12 containers and 12 matching lids. Airtight snap-lock lids prevent leaks and keep food fresh 3x longer. Microwave safe (vented lids), dishwasher safe, freezer safe. Stackable space-saving design. Clear containers see contents at glance. Various sizes: 4 small (12oz), 4 medium (20oz), 4 large (35oz). BPA-free durable plastic. Perfect for meal prep, leftovers, lunch boxes. Lifetime warranty.",
        "base_cost": 16.99,
        "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f?w=800",
        "category": "Home & Living",
        "stock": 130
    }
]

DETAILED_CHRISTMAS = [
    {
        "name": "Pre-Lit Christmas Tree 7.5ft with LED Lights",
        "description": "Premium artificial Christmas tree with 600 warm white LED lights already installed. Full, realistic branches made from PVC and PE materials look like real pine. Easy 3-section assembly with color-coded branches. Metal stand included for stability. Lights feature 8 functions: steady, twinkle, fade, flash combinations. Energy-efficient LEDs never need replacing. Flame-retardant and hypoallergenic. Foldable branches for compact storage. Measures 7.5 ft tall x 4.5 ft wide. Perfect fullness to display ornaments.",
        "base_cost": 69.99,
        "image_url": "https://images.unsplash.com/photo-1544289890-f54ac1dd2789?w=800",
        "category": "Christmas",
        "stock": 50
    },
    {
        "name": "Christmas Ornament Set 100-Piece Shatterproof",
        "description": "Complete ornament set with 100 shatterproof ornaments in assorted sizes (60mm, 40mm, 30mm) and finishes (matte, shiny, glitter). Made from durable plastic won't break if dropped - safe around kids and pets. Traditional red, gold, and white color scheme. Each ornament has removable metal cap with string attached. Storage box included with individual compartments. Lightweight yet look like real glass. Perfect for 6-7.5 ft tree. Timeless elegant design.",
        "base_cost": 22.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 100
    },
    {
        "name": "Outdoor Christmas Laser Light Projector",
        "description": "Powerful outdoor Christmas light projector displays moving red and green patterns on house. Projects up to 2,200 square feet. 16 different holiday patterns: snowflakes, stars, Santa, trees. 7 lighting modes including steady, flash, strobe. Remote control operation up to 80 feet. Timer function (2, 4, 6, 8 hours). Waterproof IP65 rated for all weather. Ground stake and wall mount included. Covers entire house in minutes - no ladder needed. Adjustable speed and brightness.",
        "base_cost": 24.99,
        "image_url": "https://images.unsplash.com/photo-1576919228236-a097c32a5cd4?w=800",
        "category": "Christmas",
        "stock": 85
    },
    {
        "name": "Christmas Village Houses Set of 5 with Lights",
        "description": "Charming Christmas village set includes 5 illuminated buildings: church with steeple, Victorian house, toy shop, bakery, and train station. Each building features hand-painted details and warm white LED lights inside. Made from durable resin. Battery operated (not included) - each uses 2 AA batteries. Dimensions range from 5-8 inches tall. Creates magical winter scene on mantle or table. Includes artificial snow. Collectible quality that lasts for years. Perfect centerpiece decoration.",
        "base_cost": 39.99,
        "image_url": "https://images.unsplash.com/photo-1513297887119-d46091b24bfa?w=800",
        "category": "Christmas",
        "stock": 60
    },
    {
        "name": "Christmas Stocking Holders for Mantle Set of 4",
        "description": "Elegant stocking holders with stable 3-inch base prevents tipping. Set of 4 holders with holiday designs: Santa, Snowman, Reindeer, Christmas Tree. Made from heavy-duty iron with antique silver finish. Each holds up to 10 lbs - won't fall even with heavy filled stockings. Rubber pads on bottom protect mantle surface. No nails or screws needed. Decorative hooks add festive touch. Works on mantles up to 9 inches deep. Classic design matches any décor.",
        "base_cost": 18.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 110
    },
    {
        "name": "Christmas Blanket Throw Fleece Sherpa 50x60",
        "description": "Cozy Christmas throw blanket with festive design on front and ultra-soft sherpa fleece on back. Measures 50x60 inches - perfect for couch or bed. Machine washable and dryer safe - colors won't fade. Premium microfiber fleece is lightweight yet incredibly warm. Multiple holiday designs available: snowflakes, reindeer, plaid, Fair Isle patterns. Reversible for two looks. Makes great gift. Use year after year. Adds instant Christmas cheer to living room.",
        "base_cost": 16.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 120
    },
    {
        "name": "Advent Calendar Wooden with LED Lights 24 Drawers",
        "description": "Beautiful wooden advent calendar with 24 small drawers for countdown to Christmas. Each drawer is numbered and perfect size for candy, small toys, or notes. Built-in LED lights illuminate the festive winter scene. Measures 15 inches tall - substantial size for display. Made from quality wood with detailed laser-cut design. Reusable year after year. Battery operated lights (2 AA not included). Creates family tradition. Great alternative to disposable calendars. Heirloom quality.",
        "base_cost": 29.99,
        "image_url": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800",
        "category": "Christmas",
        "stock": 75
    }
]

def calculate_price(cost):
    return round(cost * 1.25, 2)

def generate_detailed_reviews(product_id, product_name):
    """Generate more detailed, realistic reviews"""
    detailed_reviews = [
        "Absolutely love this product! It exceeded all my expectations. The quality is outstanding and it works exactly as described. Shipping was fast and packaging was excellent. Would definitely recommend to anyone looking for {}.",
        "Great purchase! I've been using this for a few weeks now and I'm very impressed. The build quality is solid and it's very easy to use. Much better than similar products I've tried before. Worth every penny!",
        "Exactly what I needed! This product solved my problem perfectly. Setup was simple and it works flawlessly. The attention to detail is impressive. My family loves it too. Will be ordering more as gifts.",
        "Five stars! This is one of the best purchases I've made this year. The features are amazing and everything works great. Customer service was also very responsive when I had a question. Highly satisfied!",
        "Fantastic quality! I was a bit skeptical at first but this product really delivers. It's well-made, durable, and performs better than expected. The instructions were clear and setup took only minutes. Very happy customer!",
        "Couldn't be happier with this purchase! It arrived quickly and in perfect condition. The product quality is excellent and it looks even better in person. Using it daily and it makes my life so much easier.",
        "Best value for money! I compared many similar products before buying this one and I'm glad I chose it. The functionality is perfect and it has all the features I need. Would buy again without hesitation.",
        "Amazing product! Everything about it is great - the quality, the design, the performance. It's become an essential item in my daily routine. My friends have asked where I got it because they want one too!",
        "So glad I bought this! It's made a huge difference and I wish I had purchased it sooner. The craftsmanship is impressive and it's very user-friendly. This company really knows how to make quality products.",
        "Perfect! This product is exactly as advertised and performs flawlessly. The attention to detail is remarkable and you can tell it's made with care. Already recommended to several friends and family members."
    ]
    
    reviews = []
    num_reviews = random.randint(8, 15)
    
    for i in range(num_reviews):
        rating = random.choices([3, 4, 5], weights=[5, 25, 70])[0]  # Mostly 5 stars
        comment_template = random.choice(detailed_reviews)
        # Some reviews mention the product name
        if "{}" in comment_template:
            comment = comment_template.format(product_name.lower())
        else:
            comment = comment_template
            
        reviews.append({
            "id": f"review_{product_id}_{i}",
            "product_id": product_id,
            "user_id": f"user_{random.randint(1000, 9999)}",
            "user_name": f"Customer {random.randint(100, 999)}",
            "rating": rating,
            "comment": comment,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    return reviews

async def add_detailed_products():
    print("📦 Προσθήκη λεπτομερών προϊόντων...")
    
    all_products = DETAILED_ELECTRONICS + DETAILED_HOME_LIVING + DETAILED_CHRISTMAS
    
    total_added = 0
    total_reviews = 0
    
    for product_data in all_products:
        product_id = f"prod_{random.randint(100000, 999999)}"
        selling_price = calculate_price(product_data["base_cost"])
        
        product = {
            "id": product_id,
            "name": product_data["name"],
            "description": product_data["description"],
            "price": selling_price,
            "cost_price": product_data["base_cost"],
            "image_url": product_data["image_url"],
            "category": product_data["category"],
            "stock": product_data["stock"],
            "rating": round(random.uniform(4.5, 4.9), 1),
            "review_count": random.randint(8, 15),
            "featured": random.random() < 0.2,
            "daily_offer": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.products.insert_one(product)
        total_added += 1
        
        reviews = generate_detailed_reviews(product_id, product_data["name"])
        if reviews:
            await db.reviews.insert_many(reviews)
            total_reviews += len(reviews)
    
    print(f"\n✅ Προστέθηκαν {total_added} λεπτομερή προϊόντα!")
    print(f"⭐ Δημιουργήθηκαν {total_reviews} αναλυτικές κριτικές!")
    
    total = await db.products.count_documents({})
    total_rev = await db.reviews.count_documents({})
    electronics = await db.products.count_documents({"category": "Electronics"})
    home = await db.products.count_documents({"category": "Home & Living"})
    christmas = await db.products.count_documents({"category": "Christmas"})
    
    print(f"\n📊 ΣΥΝΟΛΟ:")
    print(f"   Προϊόντα: {total}")
    print(f"   Κριτικές: {total_rev}")
    print(f"   Electronics: {electronics}")
    print(f"   Home & Living: {home}")
    print(f"   Christmas: {christmas}")

async def main():
    try:
        await add_detailed_products()
    except Exception as e:
        print(f"❌ Σφάλμα: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
