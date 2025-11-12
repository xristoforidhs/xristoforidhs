import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart, Search } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";

export default function CategoryPage() {
  const { categoryName } = useParams();
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchProducts();
  }, [categoryName]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API}/products?category=${categoryName}&limit=1000`);
      setProducts(response.data);
    } catch (error) {
      console.error("Failed to fetch products", error);
      toast.error("Failed to load products");
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchProducts();
      return;
    }
    try {
      const response = await axios.get(`${API}/products?category=${categoryName}&search=${searchQuery}`);
      setProducts(response.data);
    } catch (error) {
      toast.error("Search failed");
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

      <div style={{maxWidth: '1400px', margin: '3rem auto', padding: '2rem'}}>
        <h1 className="section-title">{categoryName}</h1>
        <p style={{color: '#64748b', marginBottom: '1rem'}}>{products.length} products</p>

        {/* Search Bar */}
        <div style={{marginBottom: '2rem', display: 'flex', gap: '1rem', maxWidth: '500px'}}>
          <div style={{position: 'relative', flex: 1}}>
            <input
              type="text"
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              style={{
                padding: '0.75rem 2.5rem 0.75rem 1rem',
                borderRadius: '8px',
                border: '2px solid #e2e8f0',
                width: '100%',
                fontSize: '1rem'
              }}
            />
            <button 
              onClick={handleSearch} 
              style={{
                position: 'absolute', 
                right: '0.5rem', 
                top: '50%', 
                transform: 'translateY(-50%)', 
                background: 'none', 
                border: 'none', 
                cursor: 'pointer',
                color: '#64748b'
              }}
            >
              <Search size={20} />
            </button>
          </div>
        </div>

        <div className="products-grid">
          {products.map(product => (
            <div key={product.id} className="product-card">
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
                  style={{width: '100%'}}
                >
                  <ShoppingCart size={18} />
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}