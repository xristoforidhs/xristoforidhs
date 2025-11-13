import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function ChristmasPage() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const navigate = useNavigate();

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  useEffect(() => {
    fetchChristmasProducts();
  }, []);

  const fetchChristmasProducts = async () => {
    try {
      // Get ONLY Christmas category products
      const response = await axios.get(`${API}/products?category=Christmas&limit=100`);
      setProducts(response.data);
    } catch (error) {
      console.error("Failed to fetch Christmas products", error);
    }
  };

  const addToCart = (product) => {
    const existing = cart.find(item => item.id === product.id);
    let newCart;
    
    if (existing) {
      newCart = cart.map(item => 
        item.id === product.id 
          ? {...item, quantity: item.quantity + 1}
          : item
      );
    } else {
      newCart = [...cart, {...product, quantity: 1}];
    }
    
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
    toast.success("🎄 Added to Christmas cart!");
  };

  return (
    <div style={{background: 'linear-gradient(135deg, #165b33 0%, #dc2626 100%)', minHeight: '100vh'}}>
      <Navbar cartCount={cartCount} />
      
      {/* Christmas Header */}
      <div style={{
        textAlign: 'center',
        padding: '4rem 2rem',
        color: 'white'
      }}>
        <h1 style={{fontSize: '3rem', fontWeight: 'bold', marginBottom: '1rem'}}>
          🎄 Christmas Special 🎄
        </h1>
        <p style={{fontSize: '1.25rem', opacity: 0.9}}>
          ❄️ Amazing Christmas deals and festive products! ❄️
        </p>
        
        {/* Music Controls */}
        <div style={{marginTop: '2rem', display: 'flex', gap: '1rem', justifyContent: 'center'}}>
          <button
            onClick={playChristmasMusic}
            disabled={musicPlaying}
            style={{
              background: musicPlaying ? '#6b7280' : '#22c55e',
              color: 'white',
              padding: '0.75rem 1.5rem',
              border: 'none',
              borderRadius: '8px',
              cursor: musicPlaying ? 'not-allowed' : 'pointer',
              fontWeight: 600
            }}
          >
            🎵 {musicPlaying ? 'Music Playing' : 'Play Christmas Music'}
          </button>
          
          {musicPlaying && (
            <button
              onClick={stopMusic}
              style={{
                background: '#ef4444',
                color: 'white',
                padding: '0.75rem 1.5rem',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600
              }}
            >
              🔇 Stop Music
            </button>
          )}
        </div>
      </div>

      {/* Christmas Products */}
      <div style={{maxWidth: '1400px', margin: '0 auto', padding: '2rem'}}>
        <div className="products-grid">
          {products.map(product => (
            <div key={product.id} className="product-card" style={{
              background: 'white',
              borderRadius: '12px',
              overflow: 'hidden',
              boxShadow: '0 8px 25px rgba(220, 38, 38, 0.15)',
              position: 'relative'
            }}>
              {/* Christmas Badge */}
              <div style={{
                position: 'absolute',
                top: '10px',
                left: '10px',
                background: '#dc2626',
                color: 'white',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontSize: '0.75rem',
                fontWeight: 600,
                zIndex: 10
              }}>
                🎄 CHRISTMAS
              </div>
              
              <img 
                src={product.image_url}
                alt={product.name}
                className="product-image"
              />
              <div style={{padding: '1.5rem'}}>
                <h3 className="product-title">{product.name}</h3>
                <p className="product-price" style={{color: '#dc2626', fontWeight: 700}}>
                  €{product.price}
                </p>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem'}}>
                  <div className="product-rating">
                    {"★".repeat(Math.floor(product.rating))}
                    {"☆".repeat(5 - Math.floor(product.rating))}
                  </div>
                  <span style={{fontSize: '0.875rem', color: '#6b7280'}}>
                    ({product.review_count})
                  </span>
                </div>
                <button
                  onClick={() => addToCart(product)}
                  style={{
                    background: 'linear-gradient(135deg, #165b33, #22c55e)',
                    color: 'white',
                    border: 'none',
                    padding: '0.75rem 1rem',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontWeight: 600,
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem'
                  }}
                >
                  <ShoppingCart size={18} />
                  🎁 Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <Footer />
    </div>
  );
}