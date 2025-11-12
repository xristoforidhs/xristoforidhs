from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Stripe
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ===== MODELS =====

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    role: str = "customer"  # admin or customer
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    image_url: str
    category: str
    stock: int
    featured: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    category: str
    stock: int
    featured: bool = False

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_email: str
    user_name: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"  # pending, processing, completed, cancelled
    payment_status: str = "pending"  # pending, paid, failed
    stripe_session_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderCreate(BaseModel):
    items: List[OrderItem]

class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    order_id: str
    user_id: str
    amount: float
    currency: str
    payment_status: str = "pending"
    metadata: Optional[Dict] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CheckoutRequest(BaseModel):
    order_id: str
    host_url: str

# ===== AUTH HELPERS =====

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user)

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

# ===== AUTH ROUTES =====

@api_router.post("/auth/register")
async def register(user_input: UserRegister):
    # Check if user exists
    existing = await db.users.find_one({"email": user_input.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_input.email,
        name=user_input.name,
        password_hash=get_password_hash(user_input.password)
    )
    
    doc = user.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.users.insert_one(doc)
    
    # Create token
    token = create_access_token({"sub": user.id})
    
    return {
        "token": token,
        "user": UserResponse(id=user.id, email=user.email, name=user.name, role=user.role)
    }

@api_router.post("/auth/login")
async def login(user_input: UserLogin):
    user_doc = await db.users.find_one({"email": user_input.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = User(**user_doc)
    if not verify_password(user_input.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.id})
    
    return {
        "token": token,
        "user": UserResponse(id=user.id, email=user.email, name=user.name, role=user.role)
    }

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email, name=current_user.name, role=current_user.role)

# ===== PRODUCT ROUTES =====

@api_router.get("/products", response_model=List[Product])
async def get_products():
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    for product in products:
        if isinstance(product.get('created_at'), str):
            product['created_at'] = datetime.fromisoformat(product['created_at'])
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if isinstance(product.get('created_at'), str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    return Product(**product)

@api_router.post("/products", response_model=Product)
async def create_product(product_input: ProductCreate, current_user: User = Depends(get_current_admin)):
    product = Product(**product_input.model_dump())
    doc = product.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.products.insert_one(doc)
    return product

@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_input: ProductCreate, current_user: User = Depends(get_current_admin)):
    existing = await db.products.find_one({"id": product_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_input.model_dump()
    await db.products.update_one({"id": product_id}, {"$set": update_data})
    
    updated = await db.products.find_one({"id": product_id}, {"_id": 0})
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    return Product(**updated)

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user: User = Depends(get_current_admin)):
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# ===== ORDER ROUTES =====

@api_router.get("/orders", response_model=List[Order])
async def get_orders(current_user: User = Depends(get_current_user)):
    # Admin sees all orders, customer sees only their orders
    query = {} if current_user.role == "admin" else {"user_id": current_user.id}
    orders = await db.orders.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for order in orders:
        if isinstance(order.get('created_at'), str):
            order['created_at'] = datetime.fromisoformat(order['created_at'])
    return orders

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    order = await db.orders.find_one({"id": order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check authorization
    if current_user.role != "admin" and order['user_id'] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if isinstance(order.get('created_at'), str):
        order['created_at'] = datetime.fromisoformat(order['created_at'])
    return Order(**order)

@api_router.post("/orders", response_model=Order)
async def create_order(order_input: OrderCreate, current_user: User = Depends(get_current_user)):
    # Calculate total
    total = sum(item.price * item.quantity for item in order_input.items)
    
    order = Order(
        user_id=current_user.id,
        user_email=current_user.email,
        user_name=current_user.name,
        items=[item.model_dump() for item in order_input.items],
        total_amount=total
    )
    
    doc = order.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.orders.insert_one(doc)
    
    return order

@api_router.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str, current_user: User = Depends(get_current_admin)):
    result = await db.orders.update_one({"id": order_id}, {"$set": {"status": status}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated"}

# ===== STRIPE PAYMENT ROUTES =====

@api_router.post("/checkout/session")
async def create_checkout_session(checkout_req: CheckoutRequest, current_user: User = Depends(get_current_user)):
    # Get order
    order = await db.orders.find_one({"id": checkout_req.order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order['user_id'] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Initialize Stripe
    host_url = checkout_req.host_url
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    # Create checkout session
    success_url = f"{host_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{host_url}/cart"
    
    session_request = CheckoutSessionRequest(
        amount=float(order['total_amount']),
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "order_id": order['id'],
            "user_id": current_user.id,
            "user_email": current_user.email
        }
    )
    
    session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(session_request)
    
    # Create payment transaction
    transaction = PaymentTransaction(
        session_id=session.session_id,
        order_id=order['id'],
        user_id=current_user.id,
        amount=float(order['total_amount']),
        currency="usd",
        payment_status="pending",
        metadata=session_request.metadata
    )
    
    trans_doc = transaction.model_dump()
    trans_doc['created_at'] = trans_doc['created_at'].isoformat()
    trans_doc['updated_at'] = trans_doc['updated_at'].isoformat()
    await db.payment_transactions.insert_one(trans_doc)
    
    # Update order with session_id
    await db.orders.update_one({"id": order['id']}, {"$set": {"stripe_session_id": session.session_id}})
    
    return {"url": session.url, "session_id": session.session_id}

@api_router.get("/checkout/status/{session_id}")
async def get_checkout_status(session_id: str, current_user: User = Depends(get_current_user)):
    # Get transaction
    transaction = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction['user_id'] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if already processed
    if transaction['payment_status'] == "paid":
        return {
            "status": "complete",
            "payment_status": "paid",
            "order_id": transaction['order_id']
        }
    
    # Initialize Stripe and check status
    webhook_url = ""  # Not needed for status check
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    try:
        checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Update transaction
        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {"$set": {
                "payment_status": checkout_status.payment_status,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        # Update order if paid
        if checkout_status.payment_status == "paid":
            await db.orders.update_one(
                {"id": transaction['order_id']},
                {"$set": {
                    "payment_status": "paid",
                    "status": "processing"
                }}
            )
        
        return {
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "order_id": transaction['order_id']
        }
    except Exception as e:
        logging.error(f"Error checking payment status: {e}")
        raise HTTPException(status_code=500, detail="Error checking payment status")

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    body = await request.body()
    
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
    
    try:
        webhook_response = await stripe_checkout.handle_webhook(body, stripe_signature)
        
        # Update transaction and order
        if webhook_response.payment_status == "paid":
            await db.payment_transactions.update_one(
                {"session_id": webhook_response.session_id},
                {"$set": {
                    "payment_status": "paid",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            # Get order_id from metadata
            order_id = webhook_response.metadata.get('order_id')
            if order_id:
                await db.orders.update_one(
                    {"id": order_id},
                    {"$set": {
                        "payment_status": "paid",
                        "status": "processing"
                    }}
                )
        
        return {"status": "success"}
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()