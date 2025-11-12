import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart, Zap } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";

export default function DailyOffersPage() {
  const [products, setProducts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDailyOffers();
  }, []);

  const fetchDailyOffers = async () => {
    try {
      const response = await axios.get(`${API}/products?daily_offer=true`);
      setProducts(response.data);
    } catch (error) {
      console.error("Failed to fetch daily offers", error);
      toast.error("Failed to load offers");
    }
  };

  const addToCart = (product) => {
    const cart = JSON.parse(localStorage.getItem("cart") || "[]");
    const existing = cart.find(item => item.id === product.id);
    let newCart;
    if (existing) {
      newCart = cart.map(item => 
        item.id === product.id ? {...item, quantity: item.quantity + 1} : item
      );
    } else {
      newCart = [...cart, {...product, quantity: 1}];
    }
    localStorage.setItem("cart", JSON.stringify(newCart));
    toast.success("Added to cart!");
  };

  return (
    <div>
      <Navbar />

      <div style={{background: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)', color: 'white', padding: '3rem 2rem', textAlign: 'center'}}>
        <Zap size={48} style={{margin: '0 auto', marginBottom: '1rem'}} />
        <h1 style={{fontSize: '3rem', fontWeight: 700, marginBottom: '1rem'}}>Daily Offers</h1>
        <p style={{fontSize: '1.25rem', opacity: 0.95}}>Limited time deals - Don't miss out!</p>
      </div>

      <div style={{maxWidth: '1400px', margin: '3rem auto', padding: '2rem'}}>
        {products.length === 0 ? (
          <div style={{textAlign: 'center', padding: '4rem 2rem'}}>
            <h2 style={{fontSize: '1.5rem', marginBottom: '1rem'}}>No daily offers available yet</h2>
            <p style={{color: '#64748b'}}>Check back soon for amazing deals!</p>
          </div>
        ) : (
          <div className="products-grid">
            {products.map(product => (
              <div key={product.id} className="product-card" style={{border: '2px solid #f59e0b'}}>
                <div style={{position: 'absolute', top: '1rem', right: '1rem', background: '#ef4444', color: 'white', padding: '0.25rem 0.75rem', borderRadius: '999px', fontSize: '0.875rem', fontWeight: 600}}>
                  DEAL
                </div>
                <img 
                  src={product.image_url} 
                  alt={product.name} 
                  className="product-image"
                  onClick={() => navigate(`/product/${product.id}`)}
                />
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem'}}>
                    <span style={{color: '#f59e0b'}}>{'★'.repeat(Math.round(product.rating))}</span>
                    <span style={{fontSize: '0.875rem', color: '#64748b'}}>({product.review_count})</span>
                  </div>
                  <p className="product-description">{product.description.substring(0, 80)}...</p>
                  <div className="product-price">${product.price}</div>
                  <button 
                    onClick={() => addToCart(product)} 
                    className="btn btn-primary"
                    style={{width: '100%', background: '#f59e0b'}}
                  >
                    <ShoppingCart size={18} />
                    Add to Cart
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}