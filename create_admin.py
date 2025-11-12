#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv('/app/backend/.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin_user():
    """Create an admin user"""
    
    # Check if admin already exists
    existing = await db.users.find_one({"email": "admin@test.com"})
    if existing:
        print("Admin user already exists!")
        # Update role to admin if it's not already
        if existing.get('role') != 'admin':
            await db.users.update_one(
                {"email": "admin@test.com"},
                {"$set": {"role": "admin"}}
            )
            print("Updated existing user to admin role")
        return
    
    # Create admin user
    admin_user = {
        "id": str(uuid.uuid4()),
        "email": "admin@test.com",
        "name": "Admin User",
        "password_hash": pwd_context.hash("password123"),
        "role": "admin",
        "created_at": datetime.now().isoformat()
    }
    
    await db.users.insert_one(admin_user)
    print("Admin user created successfully!")
    print("Email: admin@test.com")
    print("Password: password123")

if __name__ == "__main__":
    asyncio.run(create_admin_user())