import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { Search, Plus, Package, ArrowLeft } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";

export default function ProductSearchPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedProducts, setSelectedProducts] = useState([]);

  const searchProducts = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      // In a real app, this would search external APIs like AliExpress, Amazon, etc.
      // For now, we'll simulate with a mock API
      const mockResults = [
        {
          id: `search_${Date.now()}_1`,
          name: `${searchQuery} Premium Quality`,
          description: `High-quality ${searchQuery} with excellent reviews and fast shipping`,
          price: (Math.random() * 50 + 10).toFixed(2),
          image_url: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
          supplier: "external_supplier",
          category: "Electronics"
        },
        {
          id: `search_${Date.now()}_2`,
          name: `${searchQuery} Professional Grade`,
          description: `Professional ${searchQuery} perfect for business and personal use`,
          price: (Math.random() * 80 + 20).toFixed(2),
          image_url: "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=400&fit=crop",
          supplier: "external_supplier",
          category: "Electronics"
        },
        {
          id: `search_${Date.now()}_3`,
          name: `${searchQuery} Luxury Edition`,
          description: `Luxury ${searchQuery} with premium materials and design`,
          price: (Math.random() * 120 + 50).toFixed(2),
          image_url: "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop",
          supplier: "external_supplier",
          category: "Electronics"
        }
      ];
      
      setSearchResults(mockResults);
    } catch (error) {
      toast.error("Search failed");
    } finally {
      setLoading(false);
    }
  };

  const addProductToStore = async (product) => {
    try {
      const storeProduct = {
        name: product.name,
        description: product.description,
        price: parseFloat(product.price),
        cost_price: parseFloat(product.price) * 0.6, // 40% markup
        image_url: product.image_url,
        images: [],
        category: product.category,
        subcategory: "Imported",
        stock: 100,
        featured: false,
        daily_offer: false,
        rating: 4.5,
        review_count: 0,
        supplier: product.supplier
      };

      await axios.post(`${API}/products`, storeProduct);
      toast.success("Product added to your store!");
      setSelectedProducts([...selectedProducts, product.id]);
    } catch (error) {
      console.error("Failed to add product", error);
      toast.error("Failed to add product to store");
    }
  };

  return (
    <div>
      <Navbar />

      <div style={{maxWidth: '1200px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/admin" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}}>
          <ArrowLeft size={20} /> Back to Admin
        </Link>

        <div style={{display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '2rem', marginBottom: '2rem'}}>
          <Package size={32} />
          <h1 className="section-title" style={{marginBottom: 0}}>Add Products to Store</h1>
        </div>

        {/* Search Interface */}
        <div style={{
          background: 'white',
          border: '2px solid #e2e8f0',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '3rem'
        }}>
          <h2 style={{marginBottom: '1rem'}}>Search for Products</h2>
          <p style={{color: '#64748b', marginBottom: '1.5rem'}}>
            Search for products you want to add to your store. Enter product names, categories, or keywords.
          </p>
          
          <div style={{display: 'flex', gap: '1rem', marginBottom: '2rem'}}>
            <div style={{position: 'relative', flex: 1}}>
              <input
                type="text"
                placeholder="Search for products (e.g., 'wireless headphones', 'kitchen tools')"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && searchProducts()}
                style={{
                  width: '100%',
                  padding: '1rem 3rem 1rem 1rem',
                  borderRadius: '8px',
                  border: '2px solid #e2e8f0',
                  fontSize: '1rem'
                }}
              />
              <Search 
                size={24} 
                style={{
                  position: 'absolute',
                  right: '1rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: '#64748b'
                }}
              />
            </div>
            <button
              onClick={searchProducts}
              disabled={loading}
              style={{
                background: '#3b82f6',
                color: 'white',
                padding: '1rem 2rem',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                opacity: loading ? 0.7 : 1
              }}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Search Tips */}
          <div style={{
            background: '#f0f9ff',
            border: '1px solid #3b82f6',
            borderRadius: '8px',
            padding: '1rem'
          }}>
            <h4 style={{marginBottom: '0.5rem', color: '#1e40af'}}>Search Tips:</h4>
            <ul style={{margin: 0, paddingLeft: '1.5rem', color: '#1e40af'}}>
              <li>Try specific product names: "bluetooth speaker", "coffee maker"</li>
              <li>Use categories: "electronics", "home decor", "fitness"</li>
              <li>Include brand preferences: "apple accessories", "kitchen gadgets"</li>
            </ul>
          </div>
        </div>

        {/* Search Results */}
        {searchResults.length > 0 && (
          <div>
            <h2 style={{marginBottom: '2rem'}}>Search Results ({searchResults.length} products found)</h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '2rem'
            }}>
              {searchResults.map(product => (
                <div key={product.id} style={{
                  background: 'white',
                  border: '2px solid #e2e8f0',
                  borderRadius: '12px',
                  overflow: 'hidden',
                  position: 'relative'
                }}>
                  <img 
                    src={product.image_url}
                    alt={product.name}
                    style={{
                      width: '100%',
                      height: '200px',
                      objectFit: 'cover'
                    }}
                  />
                  <div style={{padding: '1.5rem'}}>
                    <h3 style={{fontSize: '1.125rem', fontWeight: 600, marginBottom: '0.5rem'}}>
                      {product.name}
                    </h3>
                    <p style={{color: '#64748b', fontSize: '0.875rem', marginBottom: '1rem'}}>
                      {product.description}
                    </p>
                    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                      <span style={{fontSize: '1.25rem', fontWeight: 700, color: '#059669'}}>
                        €{product.price}
                      </span>
                      <button
                        onClick={() => addProductToStore(product)}
                        disabled={selectedProducts.includes(product.id)}
                        style={{
                          background: selectedProducts.includes(product.id) ? '#10b981' : '#3b82f6',
                          color: 'white',
                          padding: '0.5rem 1rem',
                          border: 'none',
                          borderRadius: '6px',
                          cursor: selectedProducts.includes(product.id) ? 'default' : 'pointer',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.5rem'
                        }}
                      >
                        {selectedProducts.includes(product.id) ? (
                          <>✅ Added</>
                        ) : (
                          <><Plus size={16} /> Add to Store</>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {searchResults.length === 0 && searchQuery && !loading && (
          <div style={{
            textAlign: 'center',
            padding: '4rem 2rem',
            background: 'white',
            borderRadius: '12px',
            border: '2px solid #e2e8f0'
          }}>
            <Search size={64} style={{margin: '0 auto 1rem', color: '#cbd5e1'}} />
            <h3>No results found</h3>
            <p style={{color: '#64748b'}}>Try different keywords or check your spelling</p>
          </div>
        )}
      </div>
    </div>
  );
}