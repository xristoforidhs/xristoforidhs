import { useEffect, useState, useContext } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { CheckCircle, Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function PaymentSuccessPage() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const [status, setStatus] = useState("checking");
  const [orderId, setOrderId] = useState(null);
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  useEffect(() => {
    if (!sessionId || !user) {
      navigate("/");
      return;
    }
    pollPaymentStatus();
  }, [sessionId, user]);

  const pollPaymentStatus = async (attempts = 0) => {
    const maxAttempts = 5;
    if (attempts >= maxAttempts) {
      setStatus("error");
      toast.error("Could not verify payment");
      return;
    }

    try {
      const response = await axios.get(`${API}/checkout/status/${sessionId}`);
      
      if (response.data.payment_status === "paid") {
        setStatus("success");
        setOrderId(response.data.order_id);
        localStorage.removeItem("cart");
        return;
      }

      // Continue polling
      setTimeout(() => pollPaymentStatus(attempts + 1), 2000);
    } catch (error) {
      console.error("Error checking payment:", error);
      setTimeout(() => pollPaymentStatus(attempts + 1), 2000);
    }
  };

  return (
    <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem'}}>
      <div style={{textAlign: 'center', maxWidth: '500px'}}>
        {status === "checking" && (
          <>
            <Loader2 className="animate-spin" size={64} style={{margin: '0 auto', color: '#2563eb'}} />
            <h1 style={{fontSize: '2rem', fontWeight: 700, marginTop: '2rem'}}>Verifying Payment...</h1>
            <p style={{color: '#64748b', marginTop: '1rem'}}>Please wait</p>
          </>
        )}

        {status === "success" && (
          <>
            <CheckCircle size={64} style={{margin: '0 auto', color: '#22c55e'}} data-testid="success-icon" />
            <h1 style={{fontSize: '2rem', fontWeight: 700, marginTop: '2rem', color: '#22c55e'}} data-testid="success-message">Payment Completed!</h1>
            <p style={{color: '#64748b', marginTop: '1rem'}}>Thank you for your order!</p>
            <div style={{display: 'flex', gap: '1rem', marginTop: '2rem', justifyContent: 'center'}}>
              <button onClick={() => navigate("/orders")} className="btn btn-primary" data-testid="view-orders-btn">
                View Orders
              </button>
              <button onClick={() => navigate("/")} className="btn btn-secondary" data-testid="continue-shopping-btn">
                Continue Shopping
              </button>
            </div>
          </>
        )}

        {status === "error" && (
          <>
            <h1 style={{fontSize: '2rem', fontWeight: 700, color: '#ef4444'}}>Σφάλμα</h1>
            <p style={{color: '#64748b', marginTop: '1rem'}}>Κάτι πήγε στραβά</p>
            <button onClick={() => navigate("/")} className="btn btn-primary" style={{marginTop: '2rem'}}>
              Επιστροφή στην Αρχική
            </button>
          </>
        )}
      </div>
    </div>
  );
}