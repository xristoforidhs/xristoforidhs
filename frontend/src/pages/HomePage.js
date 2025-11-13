import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useCartNotification } from "@/contexts/CartNotificationContext";

export default function HomePage() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
  const { sendCartNotification } = useCartNotification();
  const productsPerPage = 24;

  useEffect(() => {
    fetchProducts(currentPage);
  }, [currentPage]);

  const fetchProducts = async (page = 1) => {
    try {
      const skip = (page - 1) * productsPerPage;
      const response = await axios.get(`${API}/products?limit=${productsPerPage}&skip=${skip}`);
      setProducts(response.data);
      
      // Get total count for pagination
      const countResponse = await axios.get(`${API}/products/count`);
      const totalProducts = countResponse.data.count;
      setTotalPages(Math.ceil(totalProducts / productsPerPage));
    } catch (error) {
      console.error("Failed to fetch products", error);
      toast.error("Failed to load products");
    }
  };

  const addToCart = async (product) => {
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
    toast.success("Added to cart!");

    // Send notification to admin
    await sendCartNotification(product, {
      name: 'Guest User',
      email: 'guest@example.com',
      sessionId: Date.now()
    });
  };

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div>
      <Navbar cartCount={cartCount} />

      <div className="hero-section" data-testid="hero-section">
        <h1 className="hero-title">Alexouko's Store</h1>
        <p className="hero-subtitle">Quality Products, Great Prices</p>
      </div>

      <div className="products-section">
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
                <div className="product-price" data-testid="product-price">€{product.price}</div>
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

        {/* Pagination */}
        {totalPages > 1 && (
          <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem', margin: '3rem 0'}}>
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              style={{
                padding: '0.75rem 1rem',
                background: currentPage === 1 ? '#e2e8f0' : '#3b82f6',
                color: currentPage === 1 ? '#94a3b8' : 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: currentPage === 1 ? 'not-allowed' : 'pointer'
              }}
            >
              Previous
            </button>
            
            <div style={{display: 'flex', gap: '0.5rem'}}>
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = i + 1;
                return (
                  <button
                    key={pageNum}
                    onClick={() => setCurrentPage(pageNum)}
                    style={{
                      padding: '0.75rem 1rem',
                      background: currentPage === pageNum ? '#3b82f6' : 'white',
                      color: currentPage === pageNum ? 'white' : '#374151',
                      border: '2px solid #e2e8f0',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      minWidth: '3rem'
                    }}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
            
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              style={{
                padding: '0.75rem 1rem',
                background: currentPage === totalPages ? '#e2e8f0' : '#3b82f6',
                color: currentPage === totalPages ? '#94a3b8' : 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: currentPage === totalPages ? 'not-allowed' : 'pointer'
              }}
            >
              Next
            </button>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}