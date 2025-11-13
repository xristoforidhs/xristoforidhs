import { useEffect, useState, useContext } from "react";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { Package } from "lucide-react";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";

export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [carts, setCarts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('completed');
  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchOrders();
    fetchAbandonedCarts();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API}/orders`);
      setOrders(response.data);
    } catch (error) {
      console.error("Failed to fetch orders", error);
      toast.error("Αποτυχία φόρτωσης παραγγελιών");
    } finally {
      setLoading(false);
    }
  };

  const fetchAbandonedCarts = async () => {
    try {
      // Fetch users who added items to cart but didn't complete order
      const response = await axios.get(`${API}/abandoned-carts`);
      setCarts(response.data);
    } catch (error) {
      console.error("Failed to fetch abandoned carts", error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: '#f59e0b',
      processing: '#3b82f6',
      completed: '#22c55e',
      cancelled: '#ef4444'
    };
    return colors[status] || '#6b7280';
  };

  const getStatusLabel = (status) => {
    const labels = {
      pending: 'Εκκρεμής',
      processing: 'Σε Επεξεργασία',
      completed: 'Ολοκληρωμένη',
      cancelled: 'Ακυρωμένη'
    };
    return labels[status] || status;
  };

  if (loading) {
    return <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Φόρτωση...</div>;
  }

  return (
    <div>
      <Navbar />

      <div style={{maxWidth: '1200px', margin: '3rem auto', padding: '2rem'}}>
        <h1 className="section-title">Οι Παραγγελίες μου</h1>

        {orders.length === 0 ? (
          <div style={{textAlign: 'center', padding: '4rem 2rem'}}>
            <Package size={64} style={{margin: '0 auto', color: '#cbd5e1'}} />
            <h2 style={{marginTop: '1rem', marginBottom: '1rem'}}>Δεν έχετε παραγγελίες ακόμα</h2>
            <Link to="/" className="btn btn-primary">
              Ξεκινήστε την αγορά
            </Link>
          </div>
        ) : (
          <div>
            {orders.map(order => (
              <div 
                key={order.id} 
                style={{
                  background: 'white', 
                  borderRadius: '16px', 
                  padding: '2rem', 
                  marginBottom: '1.5rem',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
                }}
                data-testid={`order-${order.id}`}
              >
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1.5rem'}}>
                  <div>
                    <h3 style={{fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem'}}>
                      Παραγγελία #{order.id.substring(0, 8)}
                    </h3>
                    <p style={{color: '#64748b', fontSize: '0.875rem'}}>
                      {new Date(order.created_at).toLocaleDateString('el-GR', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                  <div>
                    <span 
                      style={{
                        padding: '0.5rem 1rem',
                        borderRadius: '999px',
                        fontSize: '0.875rem',
                        fontWeight: 600,
                        background: `${getStatusColor(order.status)}20`,
                        color: getStatusColor(order.status)
                      }}
                      data-testid="order-status"
                    >
                      {getStatusLabel(order.status)}
                    </span>
                  </div>
                </div>

                <div style={{marginBottom: '1.5rem'}}>
                  {order.items.map((item, idx) => (
                    <div key={idx} style={{display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem'}}>
                      <span>{item.name} × {item.quantity}</span>
                      <span style={{fontWeight: 600}}>${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                </div>

                <hr style={{margin: '1.5rem 0'}} />

                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <div>
                    <p style={{color: '#64748b', fontSize: '0.875rem'}}>Κατάσταση Πληρωμής:</p>
                    <p style={{fontWeight: 600, color: order.payment_status === 'paid' ? '#22c55e' : '#f59e0b'}}>
                      {order.payment_status === 'paid' ? 'Πληρωμένη' : 'Εκκρεμής'}
                    </p>
                  </div>
                  <div style={{textAlign: 'right'}}>
                    <p style={{color: '#64748b', fontSize: '0.875rem'}}>Σύνολο</p>
                    <p style={{fontSize: '1.75rem', fontWeight: 700, color: '#2563eb'}} data-testid="order-total">
                      ${order.total_amount.toFixed(2)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}