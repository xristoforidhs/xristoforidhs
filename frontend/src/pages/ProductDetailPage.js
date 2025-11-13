import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart, ArrowLeft, Package, Star } from "lucide-react";
import { toast } from "sonner";

export default function ProductDetailPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProduct();
    fetchReviews();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await axios.get(`${API}/products/${id}`);
      setProduct(response.data);
    } catch (error) {
      console.error("Failed to fetch product", error);
      toast.error("Product not found");
      navigate("/");
    } finally {
      setLoading(false);
    }
  };

  const fetchReviews = async () => {
    try {
      const response = await axios.get(`${API}/products/${id}/reviews`);
      setReviews(response.data);
    } catch (error) {
      console.error("Failed to fetch reviews", error);
    }
  };

  const addToCart = () => {
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

  if (loading) {
    return <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Loading...</div>;
  }

  if (!product) return null;

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            <Package size={28} />
            TechGadgets
          </Link>
        </div>
      </nav>

      <div style={{maxWidth: '1200px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}}>
          <ArrowLeft size={20} /> Back
        </Link>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', marginTop: '2rem'}}>
          <div>
            <img 
              src={product.image_url} 
              alt={product.name} 
              style={{width: '100%', borderRadius: '16px', boxShadow: '0 8px 24px rgba(0,0,0,0.12)'}}
            />
          </div>
          
          <div>
            <h1 style={{fontSize: '2.5rem', fontWeight: 700, marginBottom: '1rem'}}>{product.name}</h1>
            <div style={{fontSize: '2rem', fontWeight: 700, color: '#2563eb', marginBottom: '2rem'}}>€{product.price}</div>
            
            <p style={{fontSize: '1.125rem', lineHeight: 1.7, color: '#475569', marginBottom: '2rem'}}>
              {product.description}
            </p>

            <div style={{marginBottom: '2rem'}}>
              <p><strong>Category:</strong> {product.category}</p>
              <p><strong>Availability:</strong> {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}</p>
            </div>

            <div style={{display: 'flex', gap: '1rem'}}>
              <button 
                onClick={addToCart}
                className="btn btn-primary"
                style={{flex: 1, fontSize: '1.125rem', padding: '1rem'}}
                disabled={product.stock === 0}
              >
                <ShoppingCart size={20} />
                Add to Cart
              </button>
              <button 
                onClick={() => {
                  addToCart();
                  navigate("/cart");
                }}
                className="btn btn-secondary"
                style={{flex: 1, fontSize: '1.125rem', padding: '1rem'}}
                disabled={product.stock === 0}
              >
                Buy Now
              </button>
            </div>
          </div>
        </div>

        {/* Reviews Section */}
        {reviews.length > 0 && (
          <div style={{marginTop: '4rem'}}>
            <div style={{display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem'}}>
              <Star size={32} style={{color: '#f59e0b'}} />
              <h2 style={{fontSize: '2rem', fontWeight: 700}}>Customer Reviews</h2>
              <span style={{fontSize: '1.25rem', color: '#64748b'}}>({reviews.length} reviews)</span>
            </div>

            <div style={{display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
              {reviews.map(review => (
                <div 
                  key={review.id}
                  style={{
                    background: 'white',
                    padding: '1.5rem',
                    borderRadius: '12px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                    border: '1px solid #e2e8f0'
                  }}
                >
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem'}}>
                    <div>
                      <div style={{fontWeight: 600, fontSize: '1.125rem', marginBottom: '0.25rem'}}>
                        {review.user_name}
                      </div>
                      <div style={{color: '#f59e0b', fontSize: '1.125rem'}}>
                        {'★'.repeat(review.rating)}
                        {'☆'.repeat(5 - review.rating)}
                      </div>
                    </div>
                    <div style={{fontSize: '0.875rem', color: '#64748b'}}>
                      {new Date(review.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <p style={{fontSize: '1rem', lineHeight: 1.6, color: '#475569'}}>
                    {review.comment}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}