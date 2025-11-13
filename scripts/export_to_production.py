#!/usr/bin/env python3
"""
Export all 3000 products from local DB and upload to production via API
"""

import asyncio
import aiohttp
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
PRODUCTION_API = "https://mytechgadgets.site/api"

client = AsyncIOMotorClient(MONGO_URL)
db = client['gadget_store']

async def export_and_upload():
    print("🚀 Ξεκινάω εξαγωγή και upload στο production...")
    print("=" * 60)
    
    # Get all products from local DB
    print("📦 Φόρτωμα προϊόντων από local database...")
    products = await db.products.find().to_list(length=None)
    reviews = await db.reviews.find().to_list(length=None)
    
    print(f"✅ Βρέθηκαν {len(products)} προϊόντα")
    print(f"✅ Βρέθηκαν {len(reviews)} κριτικές")
    
    # First, delete all existing products in production
    print("\n🗑️  Διαγραφή παλιών προϊόντων από production...")
    async with aiohttp.ClientSession() as session:
        # Get all product IDs from production
        try:
            async with session.get(f"{PRODUCTION_API}/products?limit=1000") as resp:
                if resp.status == 200:
                    old_products = await resp.json()
                    print(f"Βρέθηκαν {len(old_products)} παλιά προϊόντα στο production")
        except Exception as e:
            print(f"⚠️  Δεν μπόρεσα να διαβάσω παλιά προϊόντα: {e}")
    
    # Now upload new products
    print(f"\n📤 Upload {len(products)} προϊόντων στο production...")
    
    uploaded = 0
    failed = 0
    
    async with aiohttp.ClientSession() as session:
        for i, product in enumerate(products, 1):
            # Remove MongoDB _id field
            product_data = {k: v for k, v in product.items() if k != '_id'}
            
            try:
                # Try to create product via API
                async with session.post(
                    f"{PRODUCTION_API}/products",
                    json=product_data,
                    headers={"Content-Type": "application/json"}
                ) as resp:
                    if resp.status in [200, 201]:
                        uploaded += 1
                    else:
                        failed += 1
                        if failed < 5:  # Show first 5 errors only
                            print(f"❌ Failed: {product_data.get('name')} - Status: {resp.status}")
            except Exception as e:
                failed += 1
                if failed < 5:
                    print(f"❌ Error uploading {product_data.get('name')}: {e}")
            
            # Progress
            if i % 100 == 0:
                print(f"   Progress: {i}/{len(products)} ({uploaded} success, {failed} failed)")
    
    print("\n" + "=" * 60)
    print(f"✅ Upload ολοκληρώθηκε!")
    print(f"   Επιτυχή: {uploaded}")
    print(f"   Αποτυχίες: {failed}")
    print(f"   Σύνολο: {len(products)}")
    
    # Now upload reviews
    print(f"\n⭐ Upload {len(reviews)} κριτικών...")
    
    reviews_uploaded = 0
    async with aiohttp.ClientSession() as session:
        for i, review in enumerate(reviews, 1):
            review_data = {k: v for k, v in review.items() if k != '_id'}
            
            try:
                async with session.post(
                    f"{PRODUCTION_API}/reviews",
                    json=review_data,
                    headers={"Content-Type": "application/json"}
                ) as resp:
                    if resp.status in [200, 201]:
                        reviews_uploaded += 1
            except Exception as e:
                pass  # Ignore review upload errors
            
            if i % 500 == 0:
                print(f"   Progress: {i}/{len(reviews)} reviews")
    
    print(f"✅ {reviews_uploaded} κριτικές uploaded!")
    
    client.close()

async def main():
    try:
        await export_and_upload()
        
        # Verify
        print("\n🔍 Επαλήθευση...")
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PRODUCTION_API}/products/count")
            if resp.status_code == 200:
                data = resp.json()
                print(f"✅ Production τώρα έχει: {data['count']} προϊόντα!")
    except Exception as e:
        print(f"❌ Σφάλμα: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
