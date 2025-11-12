from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Header, BackgroundTasks
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
import httpx

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

# CJ Dropshipping
CJ_API_KEY = os.environ.get("CJ_API_KEY", "")
CJ_API_BASE_URL = "https://developers.cjdropshipping.com/api2.0/v1"

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ===== CJ DROPSHIPPING CLIENT =====

class CJDropshippingClient:
    def __init__(self):
        self.base_url = CJ_API_BASE_URL
        self.api_key = CJ_API_KEY
        self.access_token = None
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def authenticate(self):
        """Authenticate with CJ Dropshipping API"""
        try:
            response = await self.client.post(
                f"{self.base_url}/authentication/getAccessToken",
                json={"apiKey": self.api_key}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    self.access_token = data["data"]["accessToken"]
                    return True
        except Exception as e:
            logging.error(f"CJ Authentication failed: {e}")
        return False
    
    async def get_headers(self):
        if not self.access_token:
            await self.authenticate()
        return {
            "CJ-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    async def create_order(self, order_data: Dict):
        """Create order on CJ Dropshipping"""
        try:
            headers = await self.get_headers()
            response = await self.client.post(
                f"{self.base_url}/shopping/order/create",
                headers=headers,
                json=order_data
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    return data["data"]
        except Exception as e:
            logging.error(f"CJ Order creation failed: {e}")
        return None

# Global CJ client
cj_client = CJDropshippingClient()

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
    cost_price: float = 0  # CJ cost price
    image_url: str
    images: List[str] = []  # Multiple images
    category: str
    subcategory: Optional[str] = None
    stock: int
    featured: bool = False
    daily_offer: bool = False
    rating: float = 0
    review_count: int = 0
    cj_product_id: Optional[str] = None
    cj_variant_id: Optional[str] = None
    supplier: str = "cj_dropshipping"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Review(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    user_id: Optional[str] = None
    user_name: str
    rating: int  # 1-5
    comment: str
    verified_purchase: bool = False
    helpful_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReviewCreate(BaseModel):
    product_id: str
    rating: int
    comment: str

class ThemeSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = "theme_settings"
    primary_color: str = "#2563eb"
    secondary_color: str = "#764ba2"
    background_color: str = "#f5f7fa"
    text_color: str = "#1a202c"
    font_heading: str = "Space Grotesk"
    font_body: str = "Inter"
    hero_background: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    button_style: str = "rounded"  # rounded, square, pill
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
    status: str = "pending"  # pending, processing, dispatched, completed, cancelled
    payment_status: str = "pending"  # pending, paid, failed
    stripe_session_id: Optional[str] = None
    cj_order_id: Optional[str] = None
    tracking_number: Optional[str] = None
    fulfillment_status: str = "unfulfilled"  # unfulfilled, submitted_to_supplier, fulfilled
    shipping_address: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: Optional[Dict] = None

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
    coupon_code: Optional[str] = None

class Coupon(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str
    discount_type: str  # percentage or fixed
    discount_value: float
    min_purchase: Optional[float] = 0
    max_uses: Optional[int] = None
    used_count: int = 0
    valid_from: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: Optional[datetime] = None
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CouponCreate(BaseModel):
    code: str
    discount_type: str
    discount_value: float
    min_purchase: Optional[float] = 0
    max_uses: Optional[int] = None
    valid_until: Optional[str] = None

class StoreSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = "store_settings"
    store_name: str = "TechGadgets"
    store_email: str = ""
    store_phone: str = ""
    currency: str = "USD"
    tax_rate: float = 0
    shipping_flat_rate: float = 0
    free_shipping_threshold: float = 0
    stripe_publishable_key: str = ""
    stripe_secret_key: str = ""
    # Social Media
    tiktok_url: str = ""
    instagram_url: str = ""
    facebook_url: str = ""
    twitter_url: str = ""
    # Ad Networks
    google_adsense_id: str = ""
    google_adsense_enabled: bool = False
    medianet_id: str = ""
    medianet_enabled: bool = False
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StoreSettingsUpdate(BaseModel):
    store_name: Optional[str] = None
    store_email: Optional[str] = None
    store_phone: Optional[str] = None
    currency: Optional[str] = None
    tax_rate: Optional[float] = None
    shipping_flat_rate: Optional[float] = None
    free_shipping_threshold: Optional[float] = None
    stripe_publishable_key: Optional[str] = None
    stripe_secret_key: Optional[str] = None
    tiktok_url: Optional[str] = None
    instagram_url: Optional[str] = None
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    google_adsense_id: Optional[str] = None
    google_adsense_enabled: Optional[bool] = None
    medianet_id: Optional[str] = None
    medianet_enabled: Optional[bool] = None

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

# ===== BACKGROUND TASKS =====

async def submit_order_to_cj(order_id: str, order_data: Dict):
    """Submit order to CJ Dropshipping in background"""
    try:
        logging.info(f"Submitting order {order_id} to CJ Dropshipping")
        
        # Create order on CJ Dropshipping
        cj_response = await cj_client.create_order(order_data)
        
        if cj_response and cj_response.get("orderId"):
            cj_order_id = cj_response["orderId"]
            
            # Update order with CJ order ID
            await db.orders.update_one(
                {"id": order_id},
                {"$set": {
                    "cj_order_id": cj_order_id,
                    "fulfillment_status": "submitted_to_supplier",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            logging.info(f"Order {order_id} submitted to CJ with ID {cj_order_id}")
        else:
            logging.error(f"Failed to submit order {order_id} to CJ Dropshipping")
            await db.orders.update_one(
                {"id": order_id},
                {"$set": {"fulfillment_status": "failed"}}
            )
    except Exception as e:
        logging.error(f"Error submitting order to CJ: {e}")
        await db.orders.update_one(
            {"id": order_id},
            {"$set": {"fulfillment_status": "failed"}}
        )

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
async def create_order(order_input: OrderCreate, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    # Calculate total
    total = sum(item.price * item.quantity for item in order_input.items)
    
    order = Order(
        user_id=current_user.id,
        user_email=current_user.email,
        user_name=current_user.name,
        items=[item.model_dump() for item in order_input.items],
        total_amount=total,
        shipping_address=str(order_input.shipping_address) if order_input.shipping_address else None
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
async def create_checkout_session(checkout_req: CheckoutRequest, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    # Get order
    order = await db.orders.find_one({"id": checkout_req.order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order['user_id'] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Apply coupon if provided
    final_amount = float(order['total_amount'])
    discount_amount = 0
    
    if checkout_req.coupon_code:
        try:
            coupon = await db.coupons.find_one({"code": checkout_req.coupon_code.upper(), "active": True}, {"_id": 0})
            if coupon:
                # Calculate discount
                if coupon['discount_type'] == 'percentage':
                    discount_amount = final_amount * (coupon['discount_value'] / 100)
                else:
                    discount_amount = coupon['discount_value']
                
                final_amount = max(0, final_amount - discount_amount)
                
                # Increment coupon usage
                await db.coupons.update_one(
                    {"code": checkout_req.coupon_code.upper()},
                    {"$inc": {"used_count": 1}}
                )
        except:
            pass  # Invalid coupon, proceed without discount
    
    # Initialize Stripe
    host_url = checkout_req.host_url
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    # Create checkout session
    success_url = f"{host_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{host_url}/cart"
    
    session_request = CheckoutSessionRequest(
        amount=final_amount,
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "order_id": order['id'],
            "user_id": current_user.id,
            "user_email": current_user.email,
            "discount_applied": str(discount_amount)
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
async def get_checkout_status(session_id: str, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
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
            
            # Get order details for CJ submission
            order = await db.orders.find_one({"id": transaction['order_id']}, {"_id": 0})
            
            # Submit to CJ Dropshipping in background if API key is configured
            if CJ_API_KEY and order:
                # Prepare CJ order data
                product_list = []
                for item in order['items']:
                    product = await db.products.find_one({"id": item['product_id']}, {"_id": 0})
                    if product and product.get('cj_variant_id'):
                        product_list.append({
                            "vid": product['cj_variant_id'],
                            "quantity": item['quantity'],
                            "productPrice": float(item['price'])
                        })
                
                if product_list:
                    cj_order_data = {
                        "productList": product_list,
                        "orderAmount": float(order['total_amount']),
                        "shipAddress": {
                            "name": order['user_name'],
                            "email": order['user_email'],
                            "country": "US",
                            "address": order.get('shipping_address', '')
                        },
                        "payType": 1
                    }
                    background_tasks.add_task(submit_order_to_cj, order['id'], cj_order_data)
        
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

# ===== COUPON ROUTES =====

@api_router.get("/coupons", response_model=List[Coupon])
async def get_coupons(current_user: User = Depends(get_current_admin)):
    """Get all coupons (admin only)"""
    coupons = await db.coupons.find({}, {"_id": 0}).to_list(1000)
    for coupon in coupons:
        if isinstance(coupon.get('created_at'), str):
            coupon['created_at'] = datetime.fromisoformat(coupon['created_at'])
        if isinstance(coupon.get('valid_from'), str):
            coupon['valid_from'] = datetime.fromisoformat(coupon['valid_from'])
        if coupon.get('valid_until') and isinstance(coupon.get('valid_until'), str):
            coupon['valid_until'] = datetime.fromisoformat(coupon['valid_until'])
    return coupons

@api_router.post("/coupons", response_model=Coupon)
async def create_coupon(coupon_input: CouponCreate, current_user: User = Depends(get_current_admin)):
    """Create new coupon (admin only)"""
    # Check if code already exists
    existing = await db.coupons.find_one({"code": coupon_input.code.upper()})
    if existing:
        raise HTTPException(status_code=400, detail="Coupon code already exists")
    
    coupon = Coupon(
        code=coupon_input.code.upper(),
        discount_type=coupon_input.discount_type,
        discount_value=coupon_input.discount_value,
        min_purchase=coupon_input.min_purchase or 0,
        max_uses=coupon_input.max_uses,
        valid_until=datetime.fromisoformat(coupon_input.valid_until) if coupon_input.valid_until else None
    )
    
    doc = coupon.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['valid_from'] = doc['valid_from'].isoformat()
    if doc.get('valid_until'):
        doc['valid_until'] = doc['valid_until'].isoformat()
    
    await db.coupons.insert_one(doc)
    return coupon

@api_router.post("/coupons/validate")
async def validate_coupon(code: str, cart_total: float):
    """Validate coupon code and return discount"""
    coupon = await db.coupons.find_one({"code": code.upper(), "active": True}, {"_id": 0})
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon code")
    
    # Check expiry
    if coupon.get('valid_until'):
        valid_until = datetime.fromisoformat(coupon['valid_until']) if isinstance(coupon['valid_until'], str) else coupon['valid_until']
        if datetime.now(timezone.utc) > valid_until:
            raise HTTPException(status_code=400, detail="Coupon has expired")
    
    # Check max uses
    if coupon.get('max_uses') and coupon['used_count'] >= coupon['max_uses']:
        raise HTTPException(status_code=400, detail="Coupon usage limit reached")
    
    # Check minimum purchase
    if cart_total < coupon.get('min_purchase', 0):
        raise HTTPException(status_code=400, detail=f"Minimum purchase of ${coupon.get('min_purchase', 0)} required")
    
    # Calculate discount
    discount = 0
    if coupon['discount_type'] == 'percentage':
        discount = cart_total * (coupon['discount_value'] / 100)
    else:  # fixed
        discount = coupon['discount_value']
    
    return {
        "valid": True,
        "discount": round(discount, 2),
        "discount_type": coupon['discount_type'],
        "discount_value": coupon['discount_value']
    }

@api_router.delete("/coupons/{coupon_id}")
async def delete_coupon(coupon_id: str, current_user: User = Depends(get_current_admin)):
    """Delete coupon (admin only)"""
    result = await db.coupons.delete_one({"id": coupon_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return {"message": "Coupon deleted"}

@api_router.put("/coupons/{coupon_id}/toggle")
async def toggle_coupon(coupon_id: str, current_user: User = Depends(get_current_admin)):
    """Toggle coupon active status (admin only)"""
    coupon = await db.coupons.find_one({"id": coupon_id})
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    new_status = not coupon.get('active', True)
    await db.coupons.update_one({"id": coupon_id}, {"$set": {"active": new_status}})
    return {"active": new_status}

# ===== STORE SETTINGS ROUTES =====

@api_router.get("/settings/public")
async def get_public_settings():
    """Get public store settings (no auth required) - for social links and ads"""
    settings = await db.store_settings.find_one({"id": "store_settings"}, {"_id": 0})
    if not settings:
        return {
            "tiktok_url": "",
            "instagram_url": "",
            "facebook_url": "",
            "twitter_url": "",
            "google_adsense_id": "",
            "google_adsense_enabled": False,
            "medianet_id": "",
            "medianet_enabled": False
        }
    
    return {
        "tiktok_url": settings.get("tiktok_url", ""),
        "instagram_url": settings.get("instagram_url", ""),
        "facebook_url": settings.get("facebook_url", ""),
        "twitter_url": settings.get("twitter_url", ""),
        "google_adsense_id": settings.get("google_adsense_id", ""),
        "google_adsense_enabled": settings.get("google_adsense_enabled", False),
        "medianet_id": settings.get("medianet_id", ""),
        "medianet_enabled": settings.get("medianet_enabled", False)
    }

@api_router.get("/settings", response_model=StoreSettings)
async def get_store_settings(current_user: User = Depends(get_current_admin)):
    """Get store settings (admin only)"""
    settings = await db.store_settings.find_one({"id": "store_settings"}, {"_id": 0})
    if not settings:
        # Create default settings
        default_settings = StoreSettings()
        doc = default_settings.model_dump()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.store_settings.insert_one(doc)
        return default_settings
    
    if isinstance(settings.get('updated_at'), str):
        settings['updated_at'] = datetime.fromisoformat(settings['updated_at'])
    return StoreSettings(**settings)

@api_router.put("/settings", response_model=StoreSettings)
async def update_store_settings(settings_input: StoreSettingsUpdate, current_user: User = Depends(get_current_admin)):
    """Update store settings (admin only)"""
    update_data = {k: v for k, v in settings_input.model_dump().items() if v is not None}
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    await db.store_settings.update_one(
        {"id": "store_settings"},
        {"$set": update_data},
        upsert=True
    )
    
    settings = await db.store_settings.find_one({"id": "store_settings"}, {"_id": 0})
    if isinstance(settings.get('updated_at'), str):
        settings['updated_at'] = datetime.fromisoformat(settings['updated_at'])
    return StoreSettings(**settings)

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
    await cj_client.client.aclose()