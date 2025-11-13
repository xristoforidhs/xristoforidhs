import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ShoppingCart, ArrowLeft, Package } from "lucide-react";
import { toast } from "sonner";

export default function ProductDetailPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProduct();
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
    toast.success("Προστέθηκε στο καλάθι!");
  };

  if (loading) {
    return <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Φόρτωση...</div>;
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
          <ArrowLeft size={20} /> Επιστροφή
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
            <div style={{fontSize: '2rem', fontWeight: 700, color: '#2563eb', marginBottom: '2rem'}}>${product.price}</div>
            
            <p style={{fontSize: '1.125rem', lineHeight: 1.7, color: '#475569', marginBottom: '2rem'}}>
              {product.description}
            </p>

            <div style={{marginBottom: '2rem'}}>
              <p><strong>Κατηγορία:</strong> {product.category}</p>
              <p><strong>Διαθεσιμότητα:</strong> {product.stock > 0 ? `${product.stock} σε απόθεμα` : 'Εξαντλημένο'}</p>
            </div>

            <div style={{display: 'flex', gap: '1rem'}}>
              <button 
                onClick={addToCart}
                className="btn btn-primary"
                style={{flex: 1, fontSize: '1.125rem', padding: '1rem'}}
                disabled={product.stock === 0}
              >
                <ShoppingCart size={20} />
                Προσθήκη στο Καλάθι
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
                Αγορά Τώρα
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}