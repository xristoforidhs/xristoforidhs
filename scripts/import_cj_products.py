import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
import httpx

# Load environment
ROOT_DIR = Path(__file__).parent.parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

CJ_API_KEY = os.environ.get('CJ_API_KEY', '')
CJ_API_BASE_URL = "https://developers.cjdropshipping.com/api2.0/v1"

async def import_cj_products():
    """Import products from CJ Dropshipping"""
    
    if not CJ_API_KEY:
        print("❌ CJ_API_KEY not found in .env file")
        return
    
    print("🔄 Connecting to CJ Dropshipping API...")
    
    # Authenticate
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Get access token
            auth_response = await client.post(
                f"{CJ_API_BASE_URL}/authentication/getAccessToken",
                json={"apiKey": CJ_API_KEY}
            )
            
            if auth_response.status_code != 200:
                print(f"❌ Authentication failed: {auth_response.text}")
                return
            
            auth_data = auth_response.json()
            if auth_data.get("code") != 200:
                print(f"❌ API returned error: {auth_data.get('message')}")
                return
            
            access_token = auth_data["data"]["accessToken"]
            print("✅ Authenticated with CJ Dropshipping")
            
            # Get products - search for popular gadgets
            headers = {
                "CJ-Access-Token": access_token,
                "Content-Type": "application/json"
            }
            
            # Search for tech gadgets
            search_keywords = ["wireless earbuds", "smart watch", "phone holder", "usb cable", "power bank"]
            all_products = []
            
            for keyword in search_keywords:
                print(f"🔍 Searching for: {keyword}")
                
                products_response = await client.get(
                    f"{CJ_API_BASE_URL}/product/list",
                    headers=headers,
                    params={
                        "pageNum": 1,
                        "pageSize": 5,
                        "keyWord": keyword
                    }
                )
                
                if products_response.status_code == 200:
                    products_data = products_response.json()
                    if products_data.get("code") == 200:
                        products = products_data.get("data", {}).get("list", [])
                        all_products.extend(products[:2])  # Take 2 products per keyword
                        print(f"  ✅ Found {len(products)} products")
                
                await asyncio.sleep(0.5)  # Rate limiting
            
            if not all_products:
                print("❌ No products found from CJ Dropshipping")
                return
            
            print(f"\n📦 Importing {len(all_products)} products to database...")
            
            # Connect to MongoDB
            mongo_url = os.environ['MONGO_URL']
            client_db = AsyncIOMotorClient(mongo_url)
            db = client_db[os.environ['DB_NAME']]
            
            # Clear existing products
            await db.products.delete_many({})
            print("🗑️  Cleared existing products")
            
            # Insert CJ products
            imported = 0
            for product in all_products:
                try:
                    product_doc = {
                        "id": str(uuid.uuid4()),
                        "cj_product_id": product.get("pid"),
                        "cj_variant_id": product.get("vid"),
                        "name": product.get("productNameEn", product.get("productName", "Product")),
                        "description": product.get("description", "High-quality product from CJ Dropshipping"),
                        "price": float(product.get("sellPrice", 0)) * 2.5,  # Add markup
                        "image_url": product.get("productImage", ""),
                        "category": product.get("categoryName", "Electronics"),
                        "stock": int(product.get("productNum", 100)),
                        "featured": imported < 5,  # First 5 as featured
                        "supplier": "cj_dropshipping",
                        "created_at": datetime.now(timezone.utc).isoformat()
                    }
                    
                    await db.products.insert_one(product_doc)
                    imported += 1
                    print(f"  ✅ Imported: {product_doc['name'][:50]}...")
                    
                except Exception as e:
                    print(f"  ❌ Error importing product: {e}")
            
            client_db.close()
            print(f"\n✅ Successfully imported {imported} products from CJ Dropshipping!")
            print("🎉 Your store is now stocked with real dropshipping products!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(import_cj_products())
