import { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

export default function CheckoutPage() {
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const [loading, setLoading] = useState(false);
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      toast.error("Please log in");
      navigate("/auth");
    }
    if (cart.length === 0) {
      toast.error("Το καλάθι είναι άδειο");
      navigate("/cart");
    }
  }, [user, cart, navigate]);

  const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  const handlePayment = async () => {
    setLoading(true);
    try {
      // Create order
      const orderItems = cart.map(item => ({
        product_id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity
      }));

      const orderResponse = await axios.post(`${API}/orders`, {
        items: orderItems
      });

      const orderId = orderResponse.data.id;

      // Create checkout session
      const hostUrl = window.location.origin;
      const checkoutResponse = await axios.post(`${API}/checkout/session`, {
        order_id: orderId,
        host_url: hostUrl
      });

      // Redirect to Stripe
      window.location.href = checkoutResponse.data.url;
    } catch (error) {
      console.error("Payment error:", error);
      toast.error("Σφάλμα κατά την πληρωμή");
      setLoading(false);
    }
  };

  return (
    <div style={{maxWidth: '800px', margin: '4rem auto', padding: '2rem'}}>
      <h1 style={{fontSize: '2rem', fontWeight: 700, marginBottom: '2rem'}} data-testid="checkout-title">Ολοκλήρωση Παραγγελίας</h1>
      
      <div style={{background: 'white', borderRadius: '16px', padding: '2rem', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', marginBottom: '2rem'}}>
        <h2 style={{fontSize: '1.5rem', fontWeight: 600, marginBottom: '1rem'}}>Στοιχεία Χρήστη</h2>
        <p><strong>Όνομα:</strong> {user?.name}</p>
        <p><strong>Email:</strong> {user?.email}</p>
      </div>

      <div style={{background: 'white', borderRadius: '16px', padding: '2rem', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', marginBottom: '2rem'}}>
        <h2 style={{fontSize: '1.5rem', fontWeight: 600, marginBottom: '1rem'}}>Περίληψη Παραγγελίας</h2>
        {cart.map(item => (
          <div key={item.id} style={{display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem'}} data-testid={`checkout-item-${item.id}`}>
            <span>{item.name} × {item.quantity}</span>
            <span style={{fontWeight: 600}}>${(item.price * item.quantity).toFixed(2)}</span>
          </div>
        ))}
        <hr style={{margin: '1rem 0'}} />
        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '1.5rem', fontWeight: 700}}>
          <span>Σύνολο</span>
          <span style={{color: '#2563eb'}} data-testid="checkout-total">${total.toFixed(2)}</span>
        </div>
      </div>

      <button 
        onClick={handlePayment} 
        disabled={loading}
        className="btn btn-primary" 
        style={{width: '100%', fontSize: '1.125rem', padding: '1rem'}}
        data-testid="pay-now-btn"
      >
        {loading ? (
          <><Loader2 className="animate-spin" size={20} /> Μεταφορά στο Stripe...</>
        ) : (
          `Πληρωμή $${total.toFixed(2)}`
        )}
      </button>
    </div>
  );
}