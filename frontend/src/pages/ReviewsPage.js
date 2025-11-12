import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { Star } from "lucide-react";
import Navbar from "@/components/Navbar";

export default function ReviewsPage() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProductsWithReviews();
  }, []);

  const fetchProductsWithReviews = async () => {
    try {
      const response = await axios.get(`${API}/products?limit=200`);
      const productsWithReviews = response.data.filter(p => p.review_count > 0);
      setProducts(productsWithReviews);
    } catch (error) {
      console.error("Failed to fetch products", error);
    }
  };

  return (
    <div>
      <Navbar />

      <div style={{maxWidth: '1400px', margin: '3rem auto', padding: '2rem'}}>
        <div style={{textAlign: 'center', marginBottom: '3rem'}}>
          <Star size={48} style={{margin: '0 auto', color: '#f59e0b', marginBottom: '1rem'}} />
          <h1 style={{fontSize: '3rem', fontWeight: 700, marginBottom: '1rem'}}>Customer Reviews</h1>
          <p style={{fontSize: '1.25rem', color: '#64748b'}}>See what our customers are saying</p>
        </div>

        <div className="products-grid">
          {products.map(product => (
            <Link
              key={product.id}
              to={`/product/${product.id}`}
              style={{textDecoration: 'none'}}
            >
              <div className="product-card">
                <img src={product.image_url} alt={product.name} className="product-image" />
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem'}}>
                    <span style={{color: '#f59e0b', fontSize: '1.25rem'}}>
                      {'★'.repeat(Math.round(product.rating))}
                      {'☆'.repeat(5 - Math.round(product.rating))}
                    </span>
                  </div>
                  <div style={{fontSize: '1.125rem', fontWeight: 600, color: '#2563eb', marginBottom: '0.5rem'}}>
                    {product.rating.toFixed(1)} / 5.0
                  </div>
                  <p style={{fontSize: '0.875rem', color: '#64748b'}}>{product.review_count} reviews</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}