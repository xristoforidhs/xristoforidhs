#!/usr/bin/env python3
"""
Localization-specific Backend API Tests
Tests the specific endpoints mentioned in the review request
"""

import asyncio
import aiohttp
import json

# Backend base URL from frontend/.env
BASE_URL = "https://estore-dashboard-4.preview.emergentagent.com/api"

class LocalizationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        print()
        self.test_results.append({"test": test_name, "success": success, "details": details})
    
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
    
    async def test_product_endpoints_detailed(self):
        """Test all product endpoints mentioned in review request"""
        print("🛍️ Testing Product Endpoints (Localization Focus)...")
        
        # Test GET /api/products with pagination
        success, response, status = await self.make_request("GET", "/products", params={"limit": 5, "skip": 0})
        if success and isinstance(response, list):
            self.log_result("GET /api/products (with pagination)", True, f"Retrieved {len(response)} products with limit=5, skip=0")
        else:
            self.log_result("GET /api/products (with pagination)", False, f"Status: {status}")
        
        # Test GET /api/products/count
        success, response, status = await self.make_request("GET", "/products/count")
        if success and "count" in response:
            total_count = response["count"]
            self.log_result("GET /api/products/count", True, f"Total products count: {total_count}")
        else:
            self.log_result("GET /api/products/count", False, f"Status: {status}")
        
        # Get a product ID for individual product test
        success, products, status = await self.make_request("GET", "/products", params={"limit": 1})
        if success and products:
            product_id = products[0]["id"]
            
            # Test GET /api/products/{product_id}
            success, response, status = await self.make_request("GET", f"/products/{product_id}")
            if success and "id" in response:
                self.log_result("GET /api/products/{product_id}", True, f"Product '{response.get('name')}' retrieved successfully")
            else:
                self.log_result("GET /api/products/{product_id}", False, f"Status: {status}")
        else:
            self.log_result("GET /api/products/{product_id}", False, "No products available for testing")
        
        # Test category filtering
        categories = ["Electronics", "Home & Living", "Christmas"]
        for category in categories:
            success, response, status = await self.make_request("GET", "/products", params={"category": category})
            if success and isinstance(response, list):
                self.log_result(f"GET /api/products?category={category}", True, f"Retrieved {len(response)} products in {category} category")
            else:
                self.log_result(f"GET /api/products?category={category}", False, f"Status: {status}")
    
    async def test_auth_endpoints_detailed(self):
        """Test authentication endpoints mentioned in review request"""
        print("🔐 Testing Authentication Endpoints (Localization Focus)...")
        
        # Test with provided credentials
        test_credentials = [
            {"email": "admin@test.com", "password": "password123", "type": "Admin"},
            {"email": "test@example.com", "password": "password123", "type": "Regular"}
        ]
        
        tokens = {}
        
        for cred in test_credentials:
            # Test login
            success, response, status = await self.make_request("POST", "/auth/login", {
                "email": cred["email"],
                "password": cred["password"]
            })
            
            if success and "token" in response:
                tokens[cred["type"]] = response["token"]
                user_info = response.get("user", {})
                self.log_result(f"POST /auth/login ({cred['type']})", True, 
                    f"Login successful for {user_info.get('name', 'Unknown')} (Role: {user_info.get('role', 'Unknown')})")
            else:
                self.log_result(f"POST /auth/login ({cred['type']})", False, f"Status: {status} - User may not exist")
        
        # Test GET /auth/me with available tokens
        for user_type, token in tokens.items():
            headers = {"Authorization": f"Bearer {token}"}
            success, response, status = await self.make_request("GET", "/auth/me", headers=headers)
            if success and "id" in response:
                self.log_result(f"GET /auth/me ({user_type})", True, 
                    f"User info: {response.get('name')} ({response.get('role')})")
            else:
                self.log_result(f"GET /auth/me ({user_type})", False, f"Status: {status}")
        
        return tokens
    
    async def test_order_endpoints(self, tokens):
        """Test order endpoints"""
        print("📦 Testing Order Endpoints...")
        
        # Test GET /api/orders (requires auth)
        for user_type, token in tokens.items():
            headers = {"Authorization": f"Bearer {token}"}
            success, response, status = await self.make_request("GET", "/orders", headers=headers)
            if success and isinstance(response, list):
                self.log_result(f"GET /api/orders ({user_type})", True, f"Retrieved {len(response)} orders")
            else:
                self.log_result(f"GET /api/orders ({user_type})", False, f"Status: {status}")
        
        # Test GET /api/abandoned-carts
        success, response, status = await self.make_request("GET", "/abandoned-carts")
        if success and isinstance(response, list):
            self.log_result("GET /api/abandoned-carts", True, f"Retrieved {len(response)} abandoned carts")
        else:
            self.log_result("GET /api/abandoned-carts", False, f"Status: {status}")
    
    async def test_settings_endpoints_detailed(self, tokens):
        """Test settings endpoints"""
        print("⚙️ Testing Settings Endpoints (Localization Focus)...")
        
        # Test GET /api/settings (requires admin)
        admin_token = tokens.get("Admin")
        if admin_token:
            headers = {"Authorization": f"Bearer {admin_token}"}
            success, response, status = await self.make_request("GET", "/settings", headers=headers)
            if success and "store_name" in response:
                self.log_result("GET /api/settings (Admin)", True, 
                    f"Store: {response.get('store_name')}, Currency: {response.get('currency', 'Not set')}")
            else:
                self.log_result("GET /api/settings (Admin)", False, f"Status: {status}")
            
            # Test PUT /api/settings (admin only)
            settings_update = {
                "store_tagline": "Quality Products, Great Prices - Localization Test"
            }
            success, response, status = await self.make_request("PUT", "/settings", settings_update, headers=headers)
            if success:
                self.log_result("PUT /api/settings (Admin)", True, "Settings updated successfully")
            else:
                self.log_result("PUT /api/settings (Admin)", False, f"Status: {status}")
        else:
            self.log_result("GET /api/settings (Admin)", False, "No admin token available")
            self.log_result("PUT /api/settings (Admin)", False, "No admin token available")
    
    async def test_review_endpoints_detailed(self):
        """Test review endpoints"""
        print("⭐ Testing Review Endpoints...")
        
        # Get a product ID first
        success, products, status = await self.make_request("GET", "/products", params={"limit": 1})
        if success and products:
            product_id = products[0]["id"]
            
            # Test GET /api/products/{product_id}/reviews
            success, response, status = await self.make_request("GET", f"/products/{product_id}/reviews")
            if success and isinstance(response, list):
                self.log_result("GET /api/products/{product_id}/reviews", True, 
                    f"Retrieved {len(response)} reviews for product '{products[0].get('name')}'")
            else:
                self.log_result("GET /api/products/{product_id}/reviews", False, f"Status: {status}")
        else:
            self.log_result("GET /api/products/{product_id}/reviews", False, "No products available for testing")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🌍 LOCALIZATION BACKEND TEST SUMMARY")
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
        
        return passed_tests, failed_tests

async def main():
    """Run localization-specific tests"""
    print("🌍 Starting Localization Backend API Tests")
    print(f"Backend URL: {BASE_URL}")
    print("="*60)
    
    async with LocalizationTester() as tester:
        # Test authentication first to get tokens
        tokens = await tester.test_auth_endpoints_detailed()
        
        # Test all other endpoints
        await tester.test_product_endpoints_detailed()
        await tester.test_order_endpoints(tokens)
        await tester.test_settings_endpoints_detailed(tokens)
        await tester.test_review_endpoints_detailed()
        
        # Print summary
        passed, failed = tester.print_summary()
        
        return passed, failed

if __name__ == "__main__":
    asyncio.run(main())