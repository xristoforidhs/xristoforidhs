import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone, timedelta
import uuid
from dotenv import load_dotenv
import random

# Load environment
ROOT_DIR = Path(__file__).parent.parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

async def seed_mega_store():
    """Seed 100+ products across categories with reviews"""
    
    print("🚀 Starting mega store seed...")
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Clear existing data
    await db.products.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing products and reviews")
    
    # Electronics Products (50+)
    electronics = [
        # Headphones & Audio
        {"name": "Wireless Bluetooth Earbuds Pro", "desc": "Premium TWS earbuds with active noise cancellation, 30-hour battery life, and IPX7 waterproof rating. Crystal clear sound quality with deep bass. Perfect for music, calls, workouts, and daily commuting.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80"},
        {"name": "Over-Ear Wireless Headphones", "desc": "Premium wireless headphones with studio-quality sound, 40-hour battery, and ultra-comfortable ear cushions. Active noise cancellation blocks out distractions. Foldable design for easy portability.", "price": 49.99, "cost": 20, "img": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80"},
        {"name": "Portable Bluetooth Speaker", "desc": "Waterproof portable speaker with 360° surround sound and 24-hour playtime. Perfect for outdoor adventures, beach trips, and parties. Built-in microphone for hands-free calls.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80"},
        {"name": "In-Ear Sports Earphones", "desc": "Sweatproof sports earbuds with secure ear hooks and powerful bass. Perfect for running, gym workouts, and active lifestyles. Tangle-free cable design.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&q=80"},
        {"name": "USB Condenser Microphone", "desc": "Professional USB microphone for streaming, podcasting, and gaming. Cardioid polar pattern reduces background noise. Plug-and-play setup with adjustable gain control.", "price": 44.99, "cost": 18, "img": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=80"},
        
        # Watches & Wearables
        {"name": "Smart Fitness Watch", "desc": "Advanced smartwatch with heart rate monitoring, sleep tracking, and 50+ sport modes. AMOLED display with 7-day battery life. Water-resistant design for swimming.", "price": 39.99, "cost": 16, "img": "https://images.unsplash.com/photo-1544117519-31a4b719223d?w=800&q=80"},
        {"name": "Activity Tracker Band", "desc": "Lightweight fitness band tracks steps, calories, distance, and sleep patterns. Long 14-day battery life. Receive notifications for calls and messages on your wrist.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80"},
        {"name": "GPS Sports Watch", "desc": "Multi-sport GPS watch with route tracking, pace monitoring, and altitude measurement. Perfect for runners, cyclists, and hikers. Durable design with military-grade durability.", "price": 59.99, "cost": 24, "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80"},
        
        # Charging & Power
        {"name": "Fast Charging Power Bank 20000mAh", "desc": "Ultra-high capacity portable charger with 65W PD fast charging. Charges laptops, tablets, and phones simultaneously with 3 USB ports. LED display shows remaining battery percentage.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80"},
        {"name": "Wireless Charging Pad", "desc": "Fast wireless charger compatible with all Qi-enabled devices. Slim design with non-slip surface. LED indicator shows charging status. Includes USB-C cable.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1591290619762-c588f7bc00c5?w=800&q=80"},
        {"name": "Multi-Port USB Charging Station", "desc": "6-port USB charging hub with intelligent power distribution. Charges multiple devices simultaneously. Compact design perfect for home, office, or travel.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80"},
        {"name": "Portable Solar Charger", "desc": "Eco-friendly solar power bank with 25000mAh capacity. Perfect for camping, hiking, and emergency preparedness. Dual USB outputs and built-in flashlight.", "price": 39.99, "cost": 16, "img": "https://images.unsplash.com/photo-1593642532454-e138e28a63f4?w=800&q=80"},
        
        # Computer Accessories
        {"name": "Wireless Gaming Mouse RGB", "desc": "Ergonomic wireless gaming mouse with 7 programmable buttons and adjustable DPI up to 8000. Customizable RGB lighting with 16 million color options. 60-hour battery life.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80"},
        {"name": "Mechanical Gaming Keyboard RGB", "desc": "Mechanical keyboard with tactile switches and per-key RGB backlighting. Anti-ghosting technology ensures every keystroke registers. Durable aluminum frame.", "price": 54.99, "cost": 22, "img": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&q=80"},
        {"name": "USB-C Hub 7-in-1", "desc": "Universal USB-C multiport adapter with HDMI 4K, 3x USB 3.0, SD/microSD card readers, and 100W PD charging. Slim aluminum design compatible with all USB-C devices.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80"},
        {"name": "Laptop Stand Aluminum", "desc": "Ergonomic laptop stand with adjustable height and angle. Improves posture and increases airflow for better cooling. Compatible with all laptop sizes 10-17 inches.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80"},
        {"name": "Wireless Keyboard and Mouse Combo", "desc": "Slim wireless keyboard and mouse set with quiet keys and precise tracking. Single USB receiver for both devices. 12-month battery life on 2 AAA batteries.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80"},
        {"name": "HD Webcam 1080P", "desc": "Professional webcam for video calls, streaming, and online meetings. Auto-focus and low-light correction ensure clear video. Dual noise-canceling microphones. Plug and play setup.", "price": 39.99, "cost": 16, "img": "https://images.unsplash.com/photo-1614624532983-4ce03382d63d?w=800&q=80"},
        
        # Phone Accessories
        {"name": "Phone Gimbal Stabilizer", "desc": "3-axis smartphone gimbal for smooth video recording. Perfect for vlogging, travel videos, and social media content. Folds to pocket size with 12-hour battery.", "price": 69.99, "cost": 28, "img": "https://images.unsplash.com/photo-1611532736579-6b16e2b50449?w=800&q=80"},
        {"name": "Wireless Car Phone Mount", "desc": "Auto-clamping car mount with 15W wireless fast charging. One-hand operation with 360° rotation. Strong suction cup and air vent clip included.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=800&q=80"},
        {"name": "Phone Camera Lens Kit", "desc": "5-in-1 smartphone camera lens kit: wide angle, macro, fisheye, telephoto, and CPL filter. Professional photography on your phone. Universal clip fits all phones.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1606229365485-93a3b8ee0385?w=800&q=80"},
        {"name": "Selfie Ring Light", "desc": "10-inch LED ring light with adjustable brightness and 3 color modes. Perfect for selfies, TikTok videos, and makeup application. Includes tripod stand and phone holder.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80"},
        
        # Cables & Adapters
        {"name": "USB-C to USB-C Cable 6ft", "desc": "Durable braided USB-C cable supports 100W fast charging and 10Gbps data transfer. Compatible with laptops, tablets, and phones. Tangle-free nylon braided design.", "price": 12.99, "cost": 5, "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80"},
        {"name": "Lightning to USB Cable 3-Pack", "desc": "MFi certified lightning cables in 3ft, 6ft, and 10ft lengths. Fast charging and data sync. Durable design withstands 10,000+ bends.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1593642532454-e138e28a63f4?w=800&q=80"},
        {"name": "HDMI Cable 4K 10ft", "desc": "High-speed HDMI 2.0 cable supports 4K@60Hz and HDR. Gold-plated connectors ensure stable signal. Perfect for gaming, streaming, and home theater.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80"},
        
        # Smart Home
        {"name": "Smart WiFi Plug 4-Pack", "desc": "Control appliances remotely with smartphone app or voice commands. Schedule on/off times and monitor energy usage. Works with Alexa and Google Assistant.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1558089687-e460d04af84e?w=800&q=80"},
        {"name": "Smart LED Light Bulbs", "desc": "WiFi smart bulbs with 16 million colors and dimming. Control with app or voice. Set schedules and scenes. Energy-efficient LED technology.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1558089687-e460d04af84e?w=800&q=80"},
        {"name": "Video Doorbell Camera", "desc": "HD video doorbell with motion detection and two-way audio. See and speak to visitors from anywhere. Night vision and cloud storage included.", "price": 79.99, "cost": 32, "img": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80"},
        
        # Camera & Photography
        {"name": "Action Camera 4K", "desc": "Waterproof action camera records 4K video at 60fps. Image stabilization for smooth footage. Includes mounting accessories for extreme sports.", "price": 89.99, "cost": 36, "img": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&q=80"},
        {"name": "Tripod with Remote", "desc": "Flexible tripod with Bluetooth remote shutter. Bendable legs grip any surface. Phone and camera compatible. Perfect for group photos and time-lapses.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1606229365485-93a3b8ee0385?w=800&q=80"},
        
        # Gaming
        {"name": "Gaming Headset with Mic", "desc": "Surround sound gaming headset with noise-canceling microphone. Comfortable memory foam ear cups for long gaming sessions. Compatible with PC, console, and mobile.", "price": 39.99, "cost": 16, "img": "https://images.unsplash.com/photo-1599669454699-248893623440?w=800&q=80"},
        {"name": "Controller Charging Dock", "desc": "Dual controller charging station with LED indicators. Fast charging for two controllers simultaneously. Overcharge protection keeps batteries healthy.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=800&q=80"},
        
        # Tablets & E-Readers
        {"name": "E-Reader 6 inch", "desc": "Glare-free e-ink display reads like real paper. Thousands of books in your pocket. Weeks of battery life. Adjustable front light for reading in any environment.", "price": 79.99, "cost": 32, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&q=80"},
        {"name": "Tablet Stylus Pen", "desc": "Precision stylus for drawing, note-taking, and navigation. Palm rejection technology. Rechargeable with 12-hour battery. Compatible with most touchscreen tablets.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1585282263861-f55e341878f8?w=800&q=80"},
        
        # Projectors & Displays
        {"name": "Mini Portable Projector", "desc": "Compact LED projector with 1080P resolution and 100-inch display. Built-in speaker and WiFi connectivity. Perfect for home entertainment and presentations.", "price": 119.99, "cost": 48, "img": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800&q=80"},
        {"name": "Portable Monitor 15.6 inch", "desc": "USB-C portable monitor for dual-screen productivity. Full HD IPS display with ultra-slim design. Perfect for working from anywhere.", "price": 149.99, "cost": 60, "img": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80"},
        
        # Storage
        {"name": "External SSD 1TB", "desc": "Ultra-fast external SSD with 540MB/s read speed. Durable metal casing protects your data. USB-C and USB-A compatible. Perfect for backups and file transfers.", "price": 89.99, "cost": 36, "img": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&q=80"},
        {"name": "USB Flash Drive 128GB", "desc": "High-speed USB 3.0 flash drive with keychain loop. Transfer files at 150MB/s. Compact metal design fits in any pocket. Compatible with PC, Mac, and Linux.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1588421357574-87938a86fa28?w=800&q=80"},
        
        # Networking
        {"name": "WiFi Range Extender", "desc": "Boost WiFi signal to eliminate dead zones. Easy setup with WPS button. Dual-band support for maximum speed. Covers up to 1500 sq ft.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=800&q=80"},
        
        # Drones
        {"name": "Mini Drone with Camera", "desc": "Compact quadcopter with HD camera and FPV transmission. One-key takeoff/landing and altitude hold. Perfect for beginners. 20-minute flight time.", "price": 69.99, "cost": 28, "img": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800&q=80"},
        
        # Fans & Cooling
        {"name": "USB Desk Fan", "desc": "Portable mini fan with adjustable speed and tilting head. Quiet operation perfect for office, bedroom, or dorm. USB-powered works anywhere.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1574336736891-fbd537ffdb65?w=800&q=80"},
        {"name": "Laptop Cooling Pad", "desc": "Laptop cooler with dual fans and adjustable height. Prevents overheating during intensive tasks. Extra USB port and ergonomic design.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80"},
        
        # Car Electronics
        {"name": "Dash Cam Front and Rear", "desc": "Dual-lens dash camera records 1080P front and rear. Loop recording and G-sensor. Night vision and parking monitor. Includes 32GB SD card.", "price": 59.99, "cost": 24, "img": "https://images.unsplash.com/photo-1558089687-e460d04af84e?w=800&q=80"},
        {"name": "Bluetooth Car Adapter", "desc": "FM transmitter adds Bluetooth to any car. Stream music and take calls hands-free. Dual USB charging ports. LED display shows battery voltage.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80"},
        
        # Health Tech
        {"name": "Digital Thermometer", "desc": "Fast and accurate infrared thermometer. Non-contact measurement in 1 second. Fever alarm and memory recall. Perfect for families with kids.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80"},
        {"name": "Pulse Oximeter", "desc": "Fingertip pulse oximeter measures blood oxygen and heart rate. OLED display with 6 viewing modes. Lightweight and portable. Includes lanyard and case.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80"},
        
        # Misc Electronics
        {"name": "Digital Voice Recorder", "desc": "Voice-activated recorder with 16GB storage. Crystal-clear audio quality. Perfect for meetings, lectures, and interviews. Long 20-hour battery life.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=80"},
        {"name": "Digital Alarm Clock", "desc": "Smart alarm clock with USB charging ports and night light. Adjustable brightness and dual alarms. Battery backup keeps time during power outages.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800&q=80"},
        {"name": "Portable Blender USB", "desc": "Rechargeable personal blender makes smoothies anywhere. 6 stainless steel blades. BPA-free 380ml capacity. Perfect for gym, office, or travel.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&q=80"},
    ]
    
    # Home Accessories (50+)
    home = [
        # Kitchen Gadgets
        {"name": "Electric Can Opener", "desc": "Automatic can opener opens any size can with one touch. Safe smooth-edge cutting. Battery-powered portable design. Essential kitchen tool for easy meal prep.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Digital Kitchen Scale", "desc": "Precision food scale measures up to 11lbs. Tare function and unit conversion. Tempered glass platform easy to clean. Perfect for baking and portion control.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Vegetable Chopper", "desc": "Multi-function vegetable chopper with interchangeable blades. Chop, dice, and slice in seconds. Large container catches food. Dishwasher safe parts.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Garlic Press", "desc": "Heavy-duty garlic press crushes cloves in one squeeze. Easy-clean design with removable chamber. Stainless steel construction. Includes garlic peeler.", "price": 12.99, "cost": 5, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Silicone Baking Mats", "desc": "Non-stick silicone baking sheets reusable up to 3000 times. Replace parchment paper and save money. Heat-resistant to 480°F. Set of 2.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Knife Sharpener", "desc": "3-stage knife sharpener restores dull blades to razor-sharp. Safe non-slip base. Works with all knife types. Makes cooking safer and more efficient.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Measuring Cups and Spoons", "desc": "Stainless steel measuring set includes 5 cups and 5 spoons. Engraved measurements never fade. Nesting design saves drawer space. Dishwasher safe.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Meat Thermometer Digital", "desc": "Instant-read thermometer gives temperature in 3 seconds. Backlit display and foldable probe. Essential for perfect cooking. Includes calibration function.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Pot and Pan Organizer", "desc": "Adjustable cookware rack organizes up to 8 pans and lids. Heavy-duty metal construction. Fits most cabinets and maximizes storage space.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        {"name": "Spice Rack Organizer", "desc": "3-tier spice rack holds 30 jars. Expandable design fits any cabinet. Non-slip grip keeps bottles secure. Transform your spice storage.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80"},
        
        # Bathroom
        {"name": "Shower Caddy", "desc": "Rustproof shower organizer with adjustable shelves. No-drilling installation with strong adhesive. Holds shampoo, soap, and accessories. Sleek modern design.", "price": 22.99, "cost": 9, "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80"},
        {"name": "Toilet Paper Holder Wall", "desc": "Modern toilet paper holder with phone shelf. Easy installation with included hardware. Stainless steel construction. Holds standard and mega rolls.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80"},
        {"name": "Bath Mat Non-Slip", "desc": "Luxury bath mat with memory foam cushioning. Quick-dry microfiber absorbs water fast. Non-slip backing prevents sliding. Machine washable.", "price": 18.99, "cost": 8, "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80"},
        {"name": "Shower Head High Pressure", "desc": "3-mode shower head increases water pressure by 200%. Easy installation without tools. Chrome finish resists tarnish. Includes plumber's tape.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80"},
        {"name": "Makeup Organizer", "desc": "Clear acrylic cosmetic organizer with multiple compartments. Stackable design maximizes counter space. Keeps makeup and skincare products tidy.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80"},
        
        # Bedroom
        {"name": "LED Strip Lights 16ft", "desc": "Smart LED light strips with 16 million colors. Control with remote or app. Music sync mode pulses lights to beat. Easy peel-and-stick installation.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"},
        {"name": "Blackout Curtains", "desc": "Thermal insulated blackout curtains block 99% of light. Energy-saving design reduces heating and cooling costs. Noise-reducing fabric. Multiple colors available.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"},
        {"name": "Under Bed Storage Bags", "desc": "Set of 2 under-bed storage containers with clear window. Reinforced zippers and handles. Protects seasonal clothes from dust. Space-saving flat design.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"},
        {"name": "Bedside Shelf", "desc": "Clamp-on bedside shelf attaches to bed frame. No drilling required. Holds phone, glasses, books. Perfect for dorms and small bedrooms.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"},
        {"name": "Pillow Inserts Set of 2", "desc": "Hypoallergenic pillow inserts filled with premium microfiber. Fluffy yet supportive for all sleep positions. Machine washable cover. Standard size.", "price": 22.99, "cost": 9, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"},
        
        # Organization
        {"name": "Closet Organizer Hanging", "desc": "5-shelf hanging closet organizer maximizes vertical space. Collapsible design stores flat when not in use. Durable fabric construction.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80"},
        {"name": "Drawer Dividers Adjustable", "desc": "Expandable drawer organizers fit any drawer size. Spring-loaded design holds firm. Organize clothes, utensils, office supplies. Set of 4.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80"},
        {"name": "Cable Management Box", "desc": "Hide messy power strips and cables in stylish box. Ventilated design prevents overheating. Compact size fits behind TV or desk. Includes cable ties.", "price": 18.99, "cost": 8, "img": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80"},
        {"name": "Velvet Hangers 50-Pack", "desc": "Ultra-thin velvet hangers save 50% closet space. Non-slip surface prevents clothes from sliding. 360° swivel hook. Includes tie/belt hooks.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80"},
        {"name": "Stackable Storage Bins", "desc": "Set of 6 clear plastic bins with lids. Stackable design maximizes vertical space. Perfect for craft supplies, toys, pantry items. BPA-free plastic.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80"},
        
        # Cleaning
        {"name": "Microfiber Cleaning Cloths", "desc": "Pack of 12 ultra-absorbent microfiber towels. Lint-free and scratch-free cleaning. Machine washable up to 500 times. Multiple colors for different tasks.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&q=80"},
        {"name": "Spin Mop and Bucket", "desc": "360° spin mop with self-wringing bucket. Microfiber mop head cleans without chemicals. Adjustable handle extends to 51 inches. Separate wash/dry chambers.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&q=80"},
        {"name": "Dustpan and Broom Set", "desc": "Upright dustpan and broom combo with long handle. No-bend design saves your back. Dustpan teeth comb out debris from broom. Stands upright for storage.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&q=80"},
        {"name": "Lint Roller 5-Pack", "desc": "Extra-sticky lint rollers remove pet hair and lint. Ergonomic handle with 450 sheets total. Refillable design. Perfect for clothes, furniture, car seats.", "price": 12.99, "cost": 5, "img": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&q=80"},
        {"name": "Scrub Brush Set", "desc": "4-piece scrub brush set for tile, grout, and tough stains. Ergonomic handles reduce hand fatigue. Stiff bristles power through grime. Hang holes for storage.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&q=80"},
        
        # Laundry
        {"name": "Collapsible Laundry Basket", "desc": "Pop-up laundry hamper folds flat for storage. Reinforced handles carry heavy loads. Mesh side pockets for detergent. Waterproof interior lining.", "price": 18.99, "cost": 8, "img": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&q=80"},
        {"name": "Mesh Laundry Bags", "desc": "Set of 5 mesh wash bags protect delicates in washing machine. Different sizes for bras, socks, lingerie. Durable zipper and reinforced seams.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&q=80"},
        {"name": "Drying Rack Folding", "desc": "3-tier clothes drying rack holds up to 66lbs. Rust-resistant coated steel. Folds flat to 2 inches for storage. Perfect for air-drying delicates.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&q=80"},
        {"name": "Iron and Ironing Board", "desc": "Steam iron with ceramic soleplate glides smoothly. Vertical steam function freshens hanging clothes. Compact ironing board with heat-resistant cover.", "price": 39.99, "cost": 16, "img": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&q=80"},
        
        # Home Decor
        {"name": "Wall Mirrors Set of 3", "desc": "Modern hexagon mirrors create stunning wall art. Frameless beveled edges. Easy hanging with included adhesive strips. Reflects light to brighten rooms.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=80"},
        {"name": "Artificial Plants Set", "desc": "Realistic faux succulents and eucalyptus. No watering required. UV-resistant for indoor/outdoor use. Includes decorative pots. Set of 4.", "price": 22.99, "cost": 9, "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=80"},
        {"name": "Picture Frames Set", "desc": "Gallery wall frame set includes 7 frames in various sizes. Includes mounting template for easy arrangement. Glass front and hanging hardware included.", "price": 29.99, "cost": 12, "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=80"},
        {"name": "Floating Shelves", "desc": "Set of 2 rustic wood floating shelves. Hidden bracket design appears to float. Holds up to 30lbs each. Perfect for books, plants, photos.", "price": 26.99, "cost": 11, "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=80"},
        {"name": "Throw Pillow Covers", "desc": "Pack of 4 decorative pillow covers in modern patterns. Soft linen-like fabric with hidden zipper. Machine washable. Fits 18x18 inch inserts.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=80"},
        
        # Pet Supplies
        {"name": "Pet Hair Remover Roller", "desc": "Reusable pet hair roller cleans without tape. Roll back and forth to trap fur in waste compartment. Works on furniture, clothes, car seats.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800&q=80"},
        {"name": "Pet Food Storage Container", "desc": "Airtight pet food bin keeps kibble fresh. Rolling wheels and scoop included. Stackable design saves space. Holds up to 25lbs of food.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800&q=80"},
        {"name": "Cat Litter Mat", "desc": "Traps litter from paws before it spreads. Soft on cat's feet but tough on messes. Easy to clean - shake or vacuum. Waterproof backing.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800&q=80"},
        
        # Safety & Security
        {"name": "Door Stopper 4-Pack", "desc": "Heavy-duty door stops with non-slip rubber. Protects walls from damage. Works on all floor types. Stylish brushed nickel finish.", "price": 12.99, "cost": 5, "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80"},
        {"name": "Window Locks 8-Pack", "desc": "Child safety window locks prevent falls. Easy adult operation with key. No drilling - strong adhesive mounting. Works on sliding windows.", "price": 16.99, "cost": 7, "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80"},
        {"name": "Cabinet Locks Child Safety", "desc": "Magnetic cabinet locks invisible from outside. Strong hold keeps curious kids out. Easy installation with 3M adhesive. Includes 8 locks and 2 keys.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80"},
        {"name": "Motion Sensor Night Light", "desc": "Battery-powered motion sensor light auto-activates in dark. Perfect for hallways, bathrooms, stairs. Stick-anywhere mounting. 3-pack saves on batteries.", "price": 18.99, "cost": 8, "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80"},
        
        # Tools & Hardware
        {"name": "Tool Kit 39-Piece", "desc": "Complete household tool set in storage case. Includes hammer, screwdrivers, pliers, wrench, tape measure. Perfect for repairs and DIY projects.", "price": 34.99, "cost": 14, "img": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=800&q=80"},
        {"name": "Picture Hanging Kit", "desc": "Complete picture hanging set with nails, hooks, wire, and level. Assorted sizes for frames up to 100lbs. Includes wall anchors for drywall.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=800&q=80"},
        {"name": "Stud Finder", "desc": "Electronic stud sensor detects wood and metal behind walls. Deep-scanning mode finds center of studs. Backlit LCD display. Essential for safe mounting.", "price": 19.99, "cost": 8, "img": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=800&q=80"},
        
        # Outdoor & Garden
        {"name": "Garden Tool Set", "desc": "6-piece gardening tools with ergonomic handles. Includes trowel, transplanter, cultivator, weeder, pruner, and gloves. Rust-resistant aluminum.", "price": 24.99, "cost": 10, "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80"},
        {"name": "Hose Nozzle Spray", "desc": "Heavy-duty metal garden hose nozzle with 10 spray patterns. Adjustable flow control and easy thumb trigger. Leak-proof connection.", "price": 14.99, "cost": 6, "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80"},
        {"name": "Plant Pots Set", "desc": "Set of 5 modern ceramic planters with drainage holes and saucers. Perfect for succulents, herbs, and small plants. Matte finish in neutral colors.", "price": 22.99, "cost": 9, "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80"},
    ]
    
    # Create all products
    all_products = []
    product_id_map = {}
    
    for idx, p in enumerate(electronics):
        product_id = str(uuid.uuid4())
        product_id_map[idx] = product_id
        product = {
            "id": product_id,
            "name": p["name"],
            "description": p["desc"],
            "price": p["price"],
            "cost_price": p["cost"],
            "image_url": p["img"],
            "images": [p["img"]],
            "category": "Electronics",
            "subcategory": "Gadgets",
            "stock": random.randint(50, 200),
            "featured": idx < 8,  # First 8 featured
            "daily_offer": False,
            "rating": round(random.uniform(4.0, 5.0), 1),
            "review_count": random.randint(10, 150),
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        all_products.append(product)
    
    for idx, p in enumerate(home):
        product_id = str(uuid.uuid4())
        product_id_map[len(electronics) + idx] = product_id
        product = {
            "id": product_id,
            "name": p["name"],
            "description": p["desc"],
            "price": p["price"],
            "cost_price": p["cost"],
            "image_url": p["img"],
            "images": [p["img"]],
            "category": "Home & Living",
            "subcategory": "Accessories",
            "stock": random.randint(50, 200),
            "featured": idx < 8,
            "daily_offer": False,
            "rating": round(random.uniform(4.0, 5.0), 1),
            "review_count": random.randint(10, 150),
            "supplier": "cj_dropshipping",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        all_products.append(product)
    
    await db.products.insert_many(all_products)
    print(f"✅ {len(all_products)} products added!")
    
    # Create realistic reviews
    review_templates = [
        {"rating": 5, "comment": "Absolutely love this product! Exceeded my expectations. Highly recommend!"},
        {"rating": 5, "comment": "Great quality for the price. Fast shipping too!"},
        {"rating": 5, "comment": "Perfect! Exactly what I was looking for. Will buy again."},
        {"rating": 5, "comment": "Amazing product! Works perfectly and looks great."},
        {"rating": 4, "comment": "Very good product. Only minor issue but overall satisfied."},
        {"rating": 4, "comment": "Good value for money. Does what it says."},
        {"rating": 4, "comment": "Happy with my purchase. Shipping was quick."},
        {"rating": 5, "comment": "Best purchase I've made in a while! Can't recommend enough."},
        {"rating": 5, "comment": "Top quality! Definitely worth the money."},
        {"rating": 4, "comment": "Nice product. Met my expectations."},
        {"rating": 5, "comment": "Fantastic! Better than I imagined. Five stars!"},
        {"rating": 4, "comment": "Solid product. Would purchase again."},
        {"rating": 5, "comment": "Impressive quality and fast delivery!"},
        {"rating": 5, "comment": "Love it! Exactly as described."},
        {"rating": 4, "comment": "Good product overall. Minor room for improvement."},
    ]
    
    fake_names = ["Sarah M.", "John D.", "Emily R.", "Michael S.", "Jessica L.", "David K.", "Amanda W.", 
                  "Chris P.", "Lisa B.", "James T.", "Rachel F.", "Tom H.", "Maria G.", "Alex C.", "Sophie N."]
    
    all_reviews = []
    for product in all_products[:30]:  # Add reviews to first 30 products
        num_reviews = random.randint(3, 8)
        for _ in range(num_reviews):
            review_template = random.choice(review_templates)
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_id": None,
                "user_name": random.choice(fake_names),
                "rating": review_template["rating"],
                "comment": review_template["comment"],
                "verified_purchase": random.choice([True, False]),
                "helpful_count": random.randint(0, 25),
                "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))).isoformat()
            }
            all_reviews.append(review)
    
    await db.reviews.insert_many(all_reviews)
    print(f"✅ {len(all_reviews)} reviews added!")
    
    client.close()
    print("\n🎉 Mega store seed complete!")
    print(f"📦 Total: {len(all_products)} products")
    print(f"💬 Total: {len(all_reviews)} reviews")
    print(f"📁 Categories: Electronics, Home & Living")

if __name__ == "__main__":
    asyncio.run(seed_mega_store())
