# CJ Dropshipping Integration Setup Guide

## 🚀 Getting Started with CJ Dropshipping

Your e-commerce store is now **ready for CJ Dropshipping integration**! Follow these steps to connect your store with CJ Dropshipping for automated order fulfillment.

---

## 📋 Step 1: Create CJ Dropshipping Account

1. **Visit CJ Dropshipping Website**
   - Go to: https://www.cjdropshipping.com/
   - Click "Sign Up" or "Register"

2. **Complete Registration**
   - Fill in your business details
   - Verify your email address
   - Complete account verification (usually takes 1-2 business days)

3. **Apply for API Access**
   - After account approval, log into your CJ Dropshipping account
   - Navigate to: **Settings → API Settings**
   - Click **"Apply for API Access"**
   - Fill out the API application form
   - Wait for API access approval (typically 1-2 days)

---

## 🔑 Step 2: Get Your API Key

Once your API access is approved:

1. **Access API Settings**
   - Log into CJ Dropshipping
   - Go to: https://developers.cjdropshipping.com/
   - Or navigate to **Settings → API Settings** in your dashboard

2. **Generate API Key**
   - Click **"Generate API Key"** button
   - Copy your API Key (format: `CJUserNum@api@xxxxxxxxxx`)
   - ⚠️ **IMPORTANT**: Keep this key secure - it's like a password!

3. **Save Your API Key**
   - Your API key will look something like: `CJ12345@api@abc123def456ghi789...`
   - Store it securely - you'll need it in the next step

---

## ⚙️ Step 3: Configure Your Store

1. **Add API Key to Backend**
   
   Open `/app/backend/.env` and add your CJ API Key:
   
   ```env
   CJ_API_KEY=CJUserNum@api@your_actual_api_key_here
   ```

2. **Restart Backend Server**
   
   ```bash
   sudo supervisorctl restart backend
   ```

3. **Verify Connection**
   
   Your store will automatically authenticate with CJ Dropshipping on the next order!

---

## 🛍️ Step 4: Import Products from CJ

### Option A: Through Admin Dashboard
1. Log into your admin account: `admin@techgadgets.com` / `admin123`
2. Go to Admin Dashboard
3. Add products manually with CJ product details

### Option B: Bulk Import (Coming Soon)
We can add a bulk import feature that syncs products directly from CJ's catalog.

---

## 📦 How It Works - Automated Fulfillment

### When a Customer Places an Order:

1. **Customer Checkout**
   - Customer adds products to cart
   - Completes checkout with Stripe payment
   - Payment is processed

2. **Automatic Order Creation**
   - Once payment is confirmed, your store **automatically**:
     - Creates an order on CJ Dropshipping
     - Submits customer shipping address
     - Pays CJ from your account balance

3. **CJ Fulfillment**
   - CJ Dropshipping processes the order
   - Picks and packs products from their warehouse
   - Ships directly to your customer

4. **Tracking Updates**
   - CJ provides tracking numbers
   - Tracking info is automatically updated in your store
   - Customer receives tracking information

### No Manual Work Required! 🎉

---

## 💰 CJ Dropshipping Pricing

- **No Monthly Fees**: Pay only for products you sell
- **Product Sourcing**: CJ finds and sources products at wholesale prices
- **Warehousing**: Free storage in CJ warehouses
- **Shipping**: Competitive shipping rates worldwide
- **Account Balance**: You need to maintain a balance in your CJ account to pay for orders

---

## 🔧 Product Setup for CJ Integration

For products to work with CJ automatic fulfillment:

1. **When adding products in Admin Dashboard**, include:
   - **CJ Product ID** (pid from CJ catalog)
   - **CJ Variant ID** (vid from CJ catalog)

2. **Finding CJ Product IDs**:
   - Browse CJ catalog at: https://www.cjdropshipping.com/product-center.html
   - Each product has a Product ID (pid) and Variant ID (vid)
   - Copy these IDs when adding products to your store

---

## 🎯 Testing the Integration

1. **Test Order Flow**:
   - Place a test order on your store
   - Complete payment with Stripe test card: `4242 4242 4242 4242`
   - Check Admin Dashboard to see order submitted to CJ
   - Check CJ Dashboard to verify order received

2. **Monitor Order Status**:
   - Orders show fulfillment status: `unfulfilled`, `submitted_to_supplier`, `fulfilled`
   - Track CJ order ID in your admin panel
   - Customers can see tracking numbers once shipped

---

## 🆘 Troubleshooting

### Issue: "API Authentication Failed"
- **Solution**: Double-check your CJ_API_KEY in `.env` file
- Ensure there are no extra spaces or quotes
- Restart backend: `sudo supervisorctl restart backend`

### Issue: "Order not submitted to CJ"
- **Solution**: Verify product has `cj_variant_id` configured
- Check backend logs: `tail -f /var/log/supervisor/backend.out.log`
- Ensure CJ account has sufficient balance

### Issue: "Product out of stock on CJ"
- **Solution**: CJ inventory is checked before order submission
- Update product stock in admin dashboard
- Consider adding inventory sync cron job

---

## 📚 Additional Resources

- **CJ Dropshipping Help Center**: https://www.cjdropshipping.com/help-center.html
- **CJ API Documentation**: https://developers.cjdropshipping.com/
- **CJ Product Catalog**: https://www.cjdropshipping.com/product-center.html
- **Support**: Contact CJ support for API-related questions

---

## 🚢 Next Steps

1. ✅ Complete CJ account registration
2. ✅ Get API key approval
3. ✅ Add API key to your store
4. ✅ Import products with CJ IDs
5. ✅ Test with a small order
6. ✅ Scale your dropshipping business!

---

## 💡 Pro Tips

- **Start Small**: Test with a few products first
- **Monitor Inventory**: CJ inventory can change - keep an eye on stock levels
- **Pricing Strategy**: Add markup to CJ prices for profit margin
- **Customer Service**: CJ provides tracking, but you handle customer inquiries
- **Product Quality**: Order samples to check quality before listing

---

**Need Help?** Your store is fully configured and ready! Just add your CJ API key and you're good to go! 🎉
