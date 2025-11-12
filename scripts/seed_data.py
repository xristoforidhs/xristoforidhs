import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path(__file__).parent.parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🌱 Seeding database...")
    
    # Create admin user
    admin_email = "admin@techgadgets.com"
    existing_admin = await db.users.find_one({"email": admin_email})
    
    if not existing_admin:
        admin = {
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "name": "Admin",
            "role": "admin",
            "password_hash": pwd_context.hash("admin123"),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(admin)
        print(f"✅ Admin user created: {admin_email} / admin123")
    else:
        print(f"ℹ️  Admin user already exists")
    
    # Check if products exist
    existing_products = await db.products.count_documents({})
    if existing_products > 0:
        print(f"ℹ️  {existing_products} products already exist")
        client.close()
        return
    
    # Sample products - Top 10 Tech Gadgets 2025
    products = [
        {
            "id": str(uuid.uuid4()),
            "name": "Apple AirPods Pro 3",
            "description": "Τα νέα AirPods Pro 3 με βελτιωμένη ακύρωση θορύβου, spatial audio και έως 8 ώρες αυτονομία. Ιδανικά για μουσική και κλήσεις.",
            "price": 249.99,
            "image_url": "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=800&q=80",
            "category": "Audio",
            "stock": 50,
            "featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Samsung Galaxy Watch 6",
            "description": "Έξυπνο ρολόι με παρακολούθηση υγείας, GPS, και μέχρι 40 ώρες αυτονομία. Συμβατό με Android και iOS.",
            "price": 329.99,
            "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&q=80",
            "category": "Wearables",
            "stock": 35,
            "featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Anker PowerCore 30000mAh",
            "description": "Φορητός φορτιστής υψηλής χωρητικότητας με USB-C PD 100W και δύο USB-A θύρες. Φορτίζει laptop, tablet και smartphones.",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80",
            "category": "Power Banks",
            "stock": 100,
            "featured": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Logitech MX Master 4",
            "description": "Εργονομικό ασύρματο mouse με 8K DPI sensor, customizable buttons και υποστήριξη για 3 συσκευές. Ιδανικό για παραγωγικότητα.",
            "price": 99.99,
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80",
            "category": "Accessories",
            "stock": 60,
            "featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Ring Video Doorbell Pro 2",
            "description": "Έξυπνο κουδούνι με 1536p HDR video, 3D motion detection και Two-Way Talk. Προστασία για το σπίτι σας 24/7.",
            "price": 249.99,
            "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80",
            "category": "Smart Home",
            "stock": 40,
            "featured": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "DJI Mini 4 Pro Drone",
            "description": "Compact drone με 4K 60fps camera, 34 λεπτά πτήσης και omnidirectional obstacle sensing. Τέλειο για φωτογραφίες και video.",
            "price": 759.99,
            "image_url": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800&q=80",
            "category": "Drones",
            "stock": 20,
            "featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bose QuietComfort Ultra",
            "description": "Premium over-ear ακουστικά με κορυφαία ακύρωση θορύβου, Immersive Audio και 24 ώρες αυτονομία.",
            "price": 429.99,
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80",
            "category": "Audio",
            "stock": 45,
            "featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "GoPro HERO 12 Black",
            "description": "Action camera με 5.3K60 video, HyperSmooth 6.0 stabilization και αδιάβροχο σχεδιασμό. Για extreme περιπέτειες.",
            "price": 399.99,
            "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&q=80",
            "category": "Cameras",
            "stock": 30,
            "featured": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Sony WH-1000XM5",
            "description": "Industry-leading noise canceling με 30 ώρες αυτονομία. Εξαιρετική ποιότητα ήχου και comfort για όλη την ημέρα.",
            "price": 399.99,
            "image_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&q=80",
            "category": "Audio",
            "stock": 55,
            "featured": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Kindle Paperwhite Signature",
            "description": "Premium e-reader με 6.8\" οθόνη, auto-adjusting light και 32GB αποθηκευτικό χώρο. Διαβάστε χωρίς καταπόνηση των ματιών.",
            "price": 189.99,
            "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&q=80",
            "category": "E-Readers",
            "stock": 70,
            "featured": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.products.insert_many(products)
    print(f"✅ {len(products)} products created")
    
    client.close()
    print("✅ Database seeded successfully!")
    print("\n📝 Admin Credentials:")
    print(f"   Email: admin@techgadgets.com")
    print(f"   Password: admin123")

if __name__ == "__main__":
    asyncio.run(seed_database())
