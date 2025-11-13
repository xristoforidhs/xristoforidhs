#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv('/app/backend/.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# More realistic and diverse review templates
REALISTIC_REVIEWS = [
    # Positive Reviews (4-5 stars)
    "Great product! Works exactly as described. Fast shipping too.",
    "Love this! Better quality than I expected for the price.",
    "Perfect for what I needed. Highly recommend!",
    "Excellent quality and great value. Will buy again.",
    "Amazing! Arrived quickly and works perfectly.",
    "Really happy with this purchase. Good build quality.",
    "Works great! Exactly what I was looking for.",
    "Good product, fair price. No complaints.",
    "Nice quality item. Does the job well.",
    "Satisfied with the purchase. Good customer service.",
    "Product as described. Fast delivery. Recommended.",
    "Great value for money. Would purchase again.",
    "Works perfectly. Easy to use and good quality.",
    "Very pleased with this item. Great buy!",
    "Excellent product. Exceeded my expectations.",
    
    # Mixed Reviews (3-4 stars)
    "Good product overall, took a bit longer to arrive than expected.",
    "Works well but packaging could be better.",
    "Nice item, though slightly smaller than I imagined.",
    "Does the job. Not amazing but decent for the price.",
    "Pretty good quality. A few minor issues but nothing major.",
    "Solid product. Works as expected. Fair price.",
    "Good value. Some minor flaws but overall satisfied.",
    "Works fine. Delivery was a bit slow but product is good.",
    "Decent quality. Would have liked better instructions.",
    "Good product but took a while to figure out how to use it.",
    "Not bad for the price. Does what it's supposed to do.",
    "Works well enough. Nothing special but gets the job done.",
    "Reasonable quality for the cost. Happy enough.",
    "Good enough. Serves its purpose well.",
    "Fair product. Met my basic needs.",
]

# Diverse, realistic reviewer names
REALISTIC_NAMES = [
    "Alex M.", "Sarah J.", "Mike R.", "Emma K.", "David L.",
    "Jessica P.", "Tom W.", "Lisa H.", "John D.", "Amy S.",
    "Chris B.", "Maria G.", "Steve F.", "Kate N.", "Ryan C.",
    "Sophie T.", "Mark V.", "Anna R.", "Paul E.", "Julie M.",
    "Ben H.", "Rachel L.", "Nick P.", "Megan A.", "Luke S.",
    "Chloe W.", "Jake M.", "Grace B.", "Sam T.", "Eva C.",
    "Max D.", "Lily F.", "Noah G.", "Zoe H.", "Ethan J.",
    "Maya K.", "Owen L.", "Ruby N.", "Leo P.", "Ava Q.",
    "Adam R.", "Ella S.", "Jack T.", "Nora U.", "Tyler V."
]

async def create_realistic_reviews():
    """Generate realistic, human-like reviews"""
    print("📝 Creating realistic reviews...")
    
    # Get all products
    products = await db.products.find({}, {"_id": 0}).to_list(10000)
    
    # Clear existing reviews
    await db.reviews.delete_many({})
    
    reviews = []
    total_reviews = 0
    
    for product in products:
        # Randomly decide how many reviews (0-25)
        num_reviews = random.choices(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
            weights=[5, 10, 15, 15, 12, 10, 8, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )[0]
        
        if num_reviews == 0:
            continue
            
        # Generate reviews for this product
        for _ in range(num_reviews):
            # More realistic rating distribution
            rating = random.choices([1, 2, 3, 4, 5], weights=[2, 3, 8, 35, 52])[0]
            
            # Choose appropriate review based on rating
            if rating >= 4:
                review_text = random.choice(REALISTIC_REVIEWS[:15])  # Positive reviews
            else:
                review_text = random.choice(REALISTIC_REVIEWS[15:])  # Mixed reviews
            
            review = {
                "id": f"review_{total_reviews}",
                "product_id": product["id"],
                "user_id": None,
                "user_name": random.choice(REALISTIC_NAMES),
                "rating": rating,
                "comment": review_text,
                "verified_purchase": random.random() < 0.75,  # 75% verified
                "helpful_count": random.randint(0, 15),
                "created_at": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00Z"
            }
            reviews.append(review)
            total_reviews += 1
        
        # Update product with actual review count and realistic average
        if num_reviews > 0:
            product_reviews = reviews[-num_reviews:]
            avg_rating = sum(r["rating"] for r in product_reviews) / len(product_reviews)
            avg_rating = round(avg_rating, 1)
            
            await db.products.update_one(
                {"id": product["id"]},
                {"$set": {
                    "review_count": num_reviews,
                    "rating": avg_rating
                }}
            )
    
    # Insert all reviews
    if reviews:
        await db.reviews.insert_many(reviews)
    
    print(f"✅ Created {total_reviews} realistic reviews for products")
    print(f"📊 Average reviews per product: {total_reviews / len([p for p in products if random.random() < 0.7]):.1f}")

if __name__ == "__main__":
    asyncio.run(create_realistic_reviews())