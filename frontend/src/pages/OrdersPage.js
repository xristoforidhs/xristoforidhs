import { useEffect, useState, useContext } from "react";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { Package } from "lucide-react";
import { toast } from "sonner";
import { Link } from "react-router-dom";
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
      toast.error("Failed to load orders");
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
      pending: 'Pending',
      processing: 'Processing',
      completed: 'Completed',
      cancelled: 'Cancelled'
    };
    return labels[status] || status;
  };

  const completedOrders = orders.filter(order => order.status === 'completed');
  const pendingOrders = orders.filter(order => order.status === 'pending');
  const shippedOrders = orders.filter(order => order.tracking_number);

  if (loading) {
    return <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Loading...</div>;
  }

  return (
    <div>
      <Navbar />

      <div style={{maxWidth: '1200px', margin: '3rem auto', padding: '2rem'}}>
        <h1 className="section-title">Order Management</h1>
        
        {/* Tabs */}
        <div style={{display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '2px solid #e2e8f0'}}>
          <button
            onClick={() => setActiveTab('completed')}
            style={{
              padding: '0.75rem 1.5rem',
              background: activeTab === 'completed' ? '#3b82f6' : 'transparent',
              color: activeTab === 'completed' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            ✅ Completed ({completedOrders.length})
          </button>
          <button
            onClick={() => setActiveTab('pending')}
            style={{
              padding: '0.75rem 1.5rem',
              background: activeTab === 'pending' ? '#f59e0b' : 'transparent',
              color: activeTab === 'pending' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            ⏳ Pending ({pendingOrders.length})
          </button>
          <button
            onClick={() => setActiveTab('shipped')}
            style={{
              padding: '0.75rem 1.5rem',
              background: activeTab === 'shipped' ? '#10b981' : 'transparent',
              color: activeTab === 'shipped' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            🚚 With Tracking ({shippedOrders.length})
          </button>
          <button
            onClick={() => setActiveTab('abandoned')}
            style={{
              padding: '0.75rem 1.5rem',
              background: activeTab === 'abandoned' ? '#ef4444' : 'transparent',
              color: activeTab === 'abandoned' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            🛒 Abandoned Carts ({carts.length})
          </button>
        </div>

        {/* Content */}
        {activeTab === 'completed' && (
          <div>
            <h2 style={{marginBottom: '1rem'}}>Completed Orders</h2>
            {completedOrders.length === 0 ? (
              <p>No completed orders</p>
            ) : (
              completedOrders.map(order => (
                <div key={order.id} style={{
                  background: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  padding: '1.5rem',
                  marginBottom: '1rem'
                }}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                    <div>
                      <h3>Order #{order.id}</h3>
                      <p><strong>Customer:</strong> {order.customer_email}</p>
                      <p><strong>Total Cost:</strong> €{order.total_amount}</p>
                      <p><strong>Date:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
                    </div>
                    <span style={{
                      background: '#10b981',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '4px',
                      fontSize: '0.875rem'
                    }}>
                      ✅ Completed
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'pending' && (
          <div>
            <h2 style={{marginBottom: '1rem'}}>Εκκρεμείς Παραγγελίες</h2>
            {pendingOrders.length === 0 ? (
              <p>Δεν υπάρχουν εκκρεμείς παραγγελίες</p>
            ) : (
              pendingOrders.map(order => (
                <div key={order.id} style={{
                  background: 'white',
                  border: '1px solid #f59e0b',
                  borderRadius: '8px',
                  padding: '1.5rem',
                  marginBottom: '1rem'
                }}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                    <div>
                      <h3>Παραγγελία #{order.id}</h3>
                      <p><strong>Πελάτης:</strong> {order.customer_email}</p>
                      <p><strong>Συνολικό Κόστος:</strong> €{order.total_amount}</p>
                      <p><strong>Ημερομηνία:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
                    </div>
                    <span style={{
                      background: '#f59e0b',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '4px',
                      fontSize: '0.875rem'
                    }}>
                      ⏳ Εκκρεμής
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'shipped' && (
          <div>
            <h2 style={{marginBottom: '1rem'}}>Παραγγελίες με Tracking Number</h2>
            {shippedOrders.length === 0 ? (
              <p>Δεν υπάρχουν παραγγελίες με tracking number</p>
            ) : (
              shippedOrders.map(order => (
                <div key={order.id} style={{
                  background: 'white',
                  border: '1px solid #10b981',
                  borderRadius: '8px',
                  padding: '1.5rem',
                  marginBottom: '1rem'
                }}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                    <div>
                      <h3>Παραγγελία #{order.id}</h3>
                      <p><strong>Πελάτης:</strong> {order.customer_email}</p>
                      <p><strong>Tracking Number:</strong> {order.tracking_number}</p>
                      <p><strong>Συνολικό Κόστος:</strong> €{order.total_amount}</p>
                      <p><strong>Ημερομηνία:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
                    </div>
                    <span style={{
                      background: '#10b981',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '4px',
                      fontSize: '0.875rem'
                    }}>
                      🚚 Στάλθηκε
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'abandoned' && (
          <div>
            <h2 style={{marginBottom: '1rem'}}>Abandoned Carts</h2>
            {carts.length === 0 ? (
              <p>No abandoned carts found</p>
            ) : (
              carts.map(cart => (
                <div key={cart.id} style={{
                  background: 'white',
                  border: '1px solid #ef4444',
                  borderRadius: '8px',
                  padding: '1.5rem',
                  marginBottom: '1rem'
                }}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                    <div>
                      <h3>Cart #{cart.id}</h3>
                      <p><strong>Customer:</strong> {cart.customer_email}</p>
                      <p><strong>Items in cart:</strong> {cart.items_count}</p>
                      <p><strong>Cart value:</strong> €{cart.total_value}</p>
                      <p><strong>Last activity:</strong> {new Date(cart.updated_at).toLocaleDateString()}</p>
                    </div>
                    <span style={{
                      background: '#ef4444',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '4px',
                      fontSize: '0.875rem'
                    }}>
                      🛒 Εγκαταλελειμμένο
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}