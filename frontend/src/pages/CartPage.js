import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "@/App";
import { ShoppingCart, Plus, Minus, Trash2, ArrowLeft, Package } from "lucide-react";
import { toast } from "sonner";

export default function CartPage() {
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const updateQuantity = (productId, delta) => {
    const newCart = cart.map(item => {
      if (item.id === productId) {
        const newQuantity = item.quantity + delta;
        return newQuantity > 0 ? {...item, quantity: newQuantity} : null;
      }
      return item;
    }).filter(Boolean);
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
  };

  const removeItem = (productId) => {
    const newCart = cart.filter(item => item.id !== productId);
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
    toast.success("Removed from cart");
  };

  const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  const handleCheckout = () => {
    if (!user) {
      toast.error("Please log in to complete your order");
      navigate("/auth");
      return;
    }
    navigate("/checkout");
  };

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand" data-testid="navbar-brand">
            <Package size={28} />
            TechGadgets
          </Link>
        </div>
      </nav>

      <div className="cart-section" data-testid="cart-section">
        <Link to="/" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}} data-testid="back-to-shop">
          <ArrowLeft size={20} /> Επιστροφή στο κατάστημα
        </Link>
        
        <h1 className="section-title">Το Καλάθι μου</h1>

        {cart.length === 0 ? (
          <div className="cart-empty" data-testid="cart-empty">
            <ShoppingCart size={64} style={{margin: '0 auto', color: '#cbd5e1'}} />
            <h2 style={{marginTop: '1rem', marginBottom: '1rem'}}>Το καλάθι σας είναι άδειο</h2>
            <Link to="/" className="btn btn-primary" data-testid="continue-shopping">
              Συνέχεια Αγορών
            </Link>
          </div>
        ) : (
          <>
            {cart.map(item => (
              <div key={item.id} className="cart-item" data-testid={`cart-item-${item.id}`}>
                <img src={item.image_url} alt={item.name} className="cart-item-image" />
                <div className="cart-item-info">
                  <h3 style={{fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem'}} data-testid="cart-item-name">{item.name}</h3>
                  <p style={{color: '#64748b'}} data-testid="cart-item-price">${item.price} × {item.quantity}</p>
                </div>
                <div className="quantity-controls">
                  <button 
                    className="quantity-btn" 
                    onClick={() => updateQuantity(item.id, -1)}
                    data-testid={`decrease-quantity-${item.id}`}
                  >
                    <Minus size={18} />
                  </button>
                  <span style={{fontSize: '1.125rem', fontWeight: 600, minWidth: '2rem', textAlign: 'center'}} data-testid={`quantity-${item.id}`}>{item.quantity}</span>
                  <button 
                    className="quantity-btn" 
                    onClick={() => updateQuantity(item.id, 1)}
                    data-testid={`increase-quantity-${item.id}`}
                  >
                    <Plus size={18} />
                  </button>
                </div>
                <div style={{fontSize: '1.5rem', fontWeight: 700, color: '#2563eb', minWidth: '6rem', textAlign: 'right'}} data-testid={`item-total-${item.id}`}>
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
                <button 
                  className="btn btn-danger" 
                  onClick={() => removeItem(item.id)}
                  data-testid={`remove-item-${item.id}`}
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))}

            <div style={{marginTop: '2rem', background: 'white', borderRadius: '16px', padding: '2rem', boxShadow: '0 4px 12px rgba(0,0,0,0.08)'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
                <h3 style={{fontSize: '1.5rem', fontWeight: 700}}>Σύνολο</h3>
                <div style={{fontSize: '2rem', fontWeight: 700, color: '#2563eb'}} data-testid="cart-total">${total.toFixed(2)}</div>
              </div>
              <button 
                onClick={handleCheckout} 
                className="btn btn-primary" 
                style={{width: '100%', fontSize: '1.125rem', padding: '1rem'}}
                data-testid="proceed-to-checkout"
              >
                Ολοκλήρωση Παραγγελίας
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}