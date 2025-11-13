import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function HomePage() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
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

      <Footer />
    </div>
  );
}