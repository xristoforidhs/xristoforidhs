#!/usr/bin/env python3
"""
Backend API Testing Suite for Alexouko's Store
Tests all backend endpoints for the dropshipping e-commerce application
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
from typing import Dict, Optional, List

# Backend base URL from frontend/.env
BASE_URL = "https://dship-customizer.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = None
        self.user_token = None
        self.admin_token = None
        self.test_results = []
        self.test_user_id = str(uuid.uuid4())
        self.test_admin_id = str(uuid.uuid4())
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, details: str = "", response_data: dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        if response_data:
            result["response"] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()
    
    async def make_request(self, method: str, endpoint: str, data: dict = None, headers: dict = None, params: dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                params=params
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = {"text": await response.text()}
                
                return response.status < 400, response_data, response.status
        except Exception as e:
            return False, {"error": str(e)}, 0
    
    async def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("🔐 Testing Authentication Endpoints...")
        
        # Test user registration
        user_data = {
            "email": f"testuser_{self.test_user_id}@example.com",
            "name": "Test User",
            "password": "testpassword123"
        }
        
        success, response, status = await self.make_request("POST", "/auth/register", user_data)
        if success and "token" in response:
            self.user_token = response["token"]
            self.log_result("User Registration", True, f"User registered successfully with ID: {response.get('user', {}).get('id')}")
        else:
            self.log_result("User Registration", False, f"Status: {status}", response)
        
        # Test admin registration (create admin user)
        admin_data = {
            "email": f"admin_{self.test_admin_id}@example.com", 
            "name": "Test Admin",
            "password": "adminpassword123"
        }
        
        success, response, status = await self.make_request("POST", "/auth/register", admin_data)
        if success and "token" in response:
            # Note: In real app, admin role would be set manually in DB
            # For testing, we'll assume the first user or use existing admin
            self.admin_token = response["token"]
            self.log_result("Admin Registration", True, f"Admin registered (role needs manual DB update)")
        else:
            self.log_result("Admin Registration", False, f"Status: {status}", response)
        
        # Test user login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        success, response, status = await self.make_request("POST", "/auth/login", login_data)
        if success and "token" in response:
            self.user_token = response["token"]
            self.log_result("User Login", True, f"Login successful")
        else:
            self.log_result("User Login", False, f"Status: {status}", response)
        
        # Test get current user info
        if self.user_token:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            success, response, status = await self.make_request("GET", "/auth/me", headers=headers)
            if success and "id" in response:
                self.log_result("Get Current User", True, f"User info retrieved: {response.get('name')}")
            else:
                self.log_result("Get Current User", False, f"Status: {status}", response)
        else:
            self.log_result("Get Current User", False, "No user token available")
    
    async def test_theme_endpoints(self):
        """Test theme endpoints (NEW)"""
        print("🎨 Testing Theme Endpoints...")
        
        # Test GET /api/theme (should work without auth)
        success, response, status = await self.make_request("GET", "/theme")
        if success and "primary_color" in response:
            self.log_result("Get Theme Settings", True, f"Theme retrieved with primary color: {response.get('primary_color')}")
        else:
            self.log_result("Get Theme Settings", False, f"Status: {status}", response)
        
        # Test PUT /api/theme (requires admin auth)
        theme_update = {
            "primary_color": "#ff6b6b",
            "secondary_color": "#4ecdc4",
            "background_color": "#f8f9fa"
        }
        
        # Test without auth (should fail)
        success, response, status = await self.make_request("PUT", "/theme", theme_update)
        if not success and status == 401:
            self.log_result("Update Theme (No Auth)", True, "Correctly rejected without authentication")
        else:
            self.log_result("Update Theme (No Auth)", False, f"Should have failed with 401, got {status}", response)
        
        # Test with admin token (if available)
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            success, response, status = await self.make_request("PUT", "/theme", theme_update, headers=headers)
            if success:
                self.log_result("Update Theme (Admin)", True, "Theme updated successfully")
            else:
                self.log_result("Update Theme (Admin)", False, f"Status: {status} - May need admin role in DB", response)
        else:
            self.log_result("Update Theme (Admin)", False, "No admin token available")
    
    async def test_newsletter_endpoints(self):
        """Test newsletter endpoints (NEW)"""
        print("📧 Testing Newsletter Endpoints...")
        
        # Test POST /api/newsletter/subscribe (no auth required)
        test_email = f"newsletter_{uuid.uuid4()}@example.com"
        
        # FastAPI EmailStr parameter should be query parameter
        success, response, status = await self.make_request(
            "POST", 
            "/newsletter/subscribe", 
            params={"email": test_email}
        )
        if success and "message" in response:
            self.log_result("Newsletter Subscribe", True, f"Subscription successful: {response.get('message')}")
            
            # Test duplicate subscription
            success, response, status = await self.make_request(
                "POST", 
                "/newsletter/subscribe", 
                params={"email": test_email}
            )
            if success and "already subscribed" in response.get("message", "").lower():
                self.log_result("Newsletter Duplicate Subscribe", True, "Correctly handled duplicate subscription")
            else:
                self.log_result("Newsletter Duplicate Subscribe", False, f"Status: {status}", response)
        else:
            self.log_result("Newsletter Subscribe", False, f"Status: {status}", response)
            self.log_result("Newsletter Duplicate Subscribe", False, "Skipped due to first test failure")
    
    async def test_products_endpoints(self):
        """Test products endpoints"""
        print("🛍️ Testing Products Endpoints...")
        
        # Test GET /api/products
        success, response, status = await self.make_request("GET", "/products", params={"limit": 10})
        if success and isinstance(response, list):
            product_count = len(response)
            self.log_result("Get Products", True, f"Retrieved {product_count} products")
            
            # Store a product ID for further testing
            if response:
                self.test_product_id = response[0].get("id")
        else:
            self.log_result("Get Products", False, f"Status: {status}", response)
            self.test_product_id = None
        
        # Test GET /api/products/{product_id}
        if hasattr(self, 'test_product_id') and self.test_product_id:
            success, response, status = await self.make_request("GET", f"/products/{self.test_product_id}")
            if success and "id" in response:
                self.log_result("Get Single Product", True, f"Product retrieved: {response.get('name')}")
            else:
                self.log_result("Get Single Product", False, f"Status: {status}", response)
        else:
            self.log_result("Get Single Product", False, "No product ID available for testing")
        
        # Test GET /api/categories
        success, response, status = await self.make_request("GET", "/categories")
        if success and isinstance(response, list):
            category_count = len(response)
            self.log_result("Get Categories", True, f"Retrieved {category_count} categories")
        else:
            self.log_result("Get Categories", False, f"Status: {status}", response)
    
    async def test_profit_markup_endpoints(self):
        """Test profit markup endpoints (NEW)"""
        print("💰 Testing Profit Markup Endpoints...")
        
        if not hasattr(self, 'test_product_id') or not self.test_product_id:
            self.log_result("Profit Markup Tests", False, "No product ID available for testing")
            return
        
        # Test PUT /api/products/{product_id}/calculate-price (requires admin auth)
        cost_price = 10.00
        
        # Test without auth (should fail)
        success, response, status = await self.make_request(
            "PUT", 
            f"/products/{self.test_product_id}/calculate-price",
            params={"cost_price": cost_price}
        )
        if not success and status in [401, 403]:
            self.log_result("Calculate Price (No Auth)", True, "Correctly rejected without authentication")
        else:
            self.log_result("Calculate Price (No Auth)", False, f"Should have failed with 401/403, got {status}", response)
        
        # Test with admin token
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            success, response, status = await self.make_request(
                "PUT",
                f"/products/{self.test_product_id}/calculate-price",
                params={"cost_price": cost_price},
                headers=headers
            )
            if success and "selling_price" in response:
                self.log_result("Calculate Price (Admin)", True, 
                    f"Price calculated: Cost ${response.get('cost_price')}, Selling ${response.get('selling_price')}")
            else:
                self.log_result("Calculate Price (Admin)", False, f"Status: {status} - May need admin role", response)
        
        # Test POST /api/products/bulk-calculate-prices (requires admin auth)
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            success, response, status = await self.make_request("POST", "/products/bulk-calculate-prices", headers=headers)
            if success and "updated_count" in response:
                self.log_result("Bulk Calculate Prices", True, f"Updated {response.get('updated_count')} products")
            else:
                self.log_result("Bulk Calculate Prices", False, f"Status: {status} - May need admin role", response)
        else:
            self.log_result("Bulk Calculate Prices", False, "No admin token available")
    
    async def test_reviews_endpoints(self):
        """Test reviews endpoints"""
        print("⭐ Testing Reviews Endpoints...")
        
        if not hasattr(self, 'test_product_id') or not self.test_product_id:
            self.log_result("Reviews Tests", False, "No product ID available for testing")
            return
        
        # Test GET /api/products/{product_id}/reviews
        success, response, status = await self.make_request("GET", f"/products/{self.test_product_id}/reviews")
        if success and isinstance(response, list):
            review_count = len(response)
            self.log_result("Get Product Reviews", True, f"Retrieved {review_count} reviews")
        else:
            self.log_result("Get Product Reviews", False, f"Status: {status}", response)
        
        # Test POST /api/reviews (requires auth)
        if self.user_token:
            review_data = {
                "product_id": self.test_product_id,
                "rating": 5,
                "comment": "Great product! Very satisfied with the quality."
            }
            
            headers = {"Authorization": f"Bearer {self.user_token}"}
            success, response, status = await self.make_request("POST", "/reviews", review_data, headers=headers)
            if success and "id" in response:
                self.log_result("Create Review", True, f"Review created with rating {response.get('rating')}")
            else:
                self.log_result("Create Review", False, f"Status: {status}", response)
        else:
            self.log_result("Create Review", False, "No user token available")
    
    async def test_settings_endpoints(self):
        """Test settings endpoints"""
        print("⚙️ Testing Settings Endpoints...")
        
        # Test GET /api/settings/public (no auth required)
        success, response, status = await self.make_request("GET", "/settings/public")
        if success and isinstance(response, dict):
            self.log_result("Get Public Settings", True, "Public settings retrieved successfully")
        else:
            self.log_result("Get Public Settings", False, f"Status: {status}", response)
        
        # Test GET /api/settings (requires admin auth)
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            success, response, status = await self.make_request("GET", "/settings", headers=headers)
            if success and "store_name" in response:
                self.log_result("Get Store Settings", True, f"Store: {response.get('store_name')}")
            else:
                self.log_result("Get Store Settings", False, f"Status: {status} - May need admin role", response)
        else:
            self.log_result("Get Store Settings", False, "No admin token available")
        
        # Test PUT /api/settings (requires admin auth)
        if self.admin_token:
            settings_update = {
                "store_tagline": "Updated tagline for testing",
                "profit_markup_percentage": 120
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            success, response, status = await self.make_request("PUT", "/settings", settings_update, headers=headers)
            if success and "store_name" in response:
                self.log_result("Update Store Settings", True, "Settings updated successfully")
            else:
                self.log_result("Update Store Settings", False, f"Status: {status} - May need admin role", response)
        else:
            self.log_result("Update Store Settings", False, "No admin token available")
    
    async def test_additional_endpoints(self):
        """Test additional endpoints for completeness"""
        print("🔍 Testing Additional Endpoints...")
        
        # Test coupon validation
        success, response, status = await self.make_request(
            "POST", 
            "/coupons/validate",
            params={"code": "TESTCODE", "cart_total": 100.0}
        )
        # This should fail with 404 (coupon not found) which is expected
        if status == 404:
            self.log_result("Coupon Validation", True, "Correctly returned 404 for non-existent coupon")
        else:
            self.log_result("Coupon Validation", False, f"Unexpected status: {status}", response)
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🧪 BACKEND API TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print("\n" + "="*60)
        
        return passed_tests, failed_tests, self.test_results

async def main():
    """Run all backend tests"""
    print("🚀 Starting Backend API Tests for Alexouko's Store")
    print(f"Backend URL: {BASE_URL}")
    print("="*60)
    
    async with BackendTester() as tester:
        # Run tests in priority order
        await tester.test_auth_endpoints()
        await tester.test_theme_endpoints()
        await tester.test_newsletter_endpoints()
        await tester.test_products_endpoints()  # Run this before profit markup
        await tester.test_profit_markup_endpoints()
        await tester.test_reviews_endpoints()
        await tester.test_settings_endpoints()
        await tester.test_additional_endpoints()
        
        # Print summary
        passed, failed, results = tester.print_summary()
        
        return passed, failed, results

if __name__ == "__main__":
    asyncio.run(main())