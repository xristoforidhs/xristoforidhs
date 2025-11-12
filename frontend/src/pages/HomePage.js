import { useEffect, useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { ShoppingCart, User, LogOut, Package } from "lucide-react";
import { toast } from "sonner";

export default function HomePage() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error("Failed to fetch products", error);
      toast.error("Failed to load products");
    }
  };

  const addToCart = (product) => {
    const existing = cart.find(item => item.id === product.id);
    let newCart;
    if (existing) {
      newCart = cart.map(item => 
        item.id === product.id ? {...item, quantity: item.quantity + 1} : item
      );
    } else {
      newCart = [...cart, {...product, quantity: 1}];
    }
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
    toast.success("Προστέθηκε στο καλάθι!");
  };

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand" data-testid="navbar-brand">
            <Package size={28} />
            Alexouko's Store
          </Link>
          <div className="navbar-links">
            <Link to="/" className="navbar-link">Home</Link>
            <Link to="/category/Electronics" className="navbar-link">Categories</Link>
            <Link to="/daily-offers" className="navbar-link" style={{color: '#f59e0b', fontWeight: 600}}>Daily Offers</Link>
            <Link to="/social" className="navbar-link">Socials</Link>
            <Link to="/cart" className="navbar-link" data-testid="cart-link">
              <ShoppingCart size={20} />
              Cart {cartCount > 0 && <span className="cart-badge" data-testid="cart-count">{cartCount}</span>}
            </Link>
            {user ? (
              <>
                {user.role === "admin" && (
                  <Link to="/admin" className="navbar-link" data-testid="admin-link">
                    Admin
                  </Link>
                )}
                <Link to="/orders" className="navbar-link" data-testid="orders-link">
                  Orders
                </Link>
                <button onClick={logout} className="navbar-link" style={{background: 'none', border: 'none', cursor: 'pointer'}} data-testid="logout-btn">
                  <LogOut size={20} /> Logout
                </button>
              </>
            ) : (
              <Link to="/auth" className="navbar-link" data-testid="login-link">
                <User size={20} /> Login
              </Link>
            )}
          </div>
        </div>
      </nav>

      <div className="hero-section" data-testid="hero-section">
        <h1 className="hero-title">Alexouko's Store</h1>
        <p className="hero-subtitle">Quality Products, Great Prices</p>
      </div>

      <div className="products-section">
        <h2 className="section-title">Κορυφαία Προϊόντα</h2>
        <div className="products-grid" data-testid="products-grid">
          {products.map(product => (
            <div key={product.id} className="product-card" data-testid={`product-card-${product.id}`}>
              <img 
                src={product.image_url} 
                alt={product.name} 
                className="product-image"
                onClick={() => navigate(`/product/${product.id}`)}
              />
              <div className="product-info">
                <h3 className="product-name" data-testid="product-name">{product.name}</h3>
                <p className="product-description">{product.description.substring(0, 80)}...</p>
                <div className="product-price" data-testid="product-price">${product.price}</div>
                <button 
                  onClick={() => addToCart(product)} 
                  className="btn btn-primary"
                  style={{width: '100%'}}
                  data-testid={`add-to-cart-${product.id}`}
                >
                  <ShoppingCart size={18} />
                  Προσθήκη στο Καλάθι
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <footer className="footer">
        <p>© 2025 TechGadgets - Το κορυφαίο e-shop για gadgets</p>
      </footer>
    </div>
  );
}