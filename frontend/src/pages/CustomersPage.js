import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { Package, ArrowLeft, Users } from "lucide-react";
import { toast } from "sonner";

export default function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      // This endpoint needs to be added to backend
      const response = await axios.get(`${API}/admin/customers`);
      setCustomers(response.data);
    } catch (error) {
      console.error("Failed to fetch customers", error);
      toast.error("Failed to load customers");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Loading...</div>;
  }

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            <Package size={28} />
            Alexouko's Store Admin
          </Link>
        </div>
      </nav>

      <div style={{maxWidth: '1400px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/admin" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}}>
          <ArrowLeft size={20} /> Back to Admin
        </Link>

        <div style={{display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '2rem', marginBottom: '2rem'}}>
          <Users size={32} />
          <h1 className="section-title" style={{marginBottom: 0}}>Registered Customers</h1>
        </div>

        <div style={{background: 'white', borderRadius: '16px', padding: '2rem', boxShadow: '0 4px 12px rgba(0,0,0,0.08)'}}>
          <div style={{marginBottom: '2rem'}}>
            <p style={{fontSize: '1.125rem', fontWeight: 600}}>Total Customers: {customers.length}</p>
          </div>

          <table style={{width: '100%', borderCollapse: 'collapse'}}>
            <thead>
              <tr style={{borderBottom: '2px solid #e2e8f0'}}>
                <th style={{padding: '1rem', textAlign: 'left'}}>Name</th>
                <th style={{padding: '1rem', textAlign: 'left'}}>Email</th>
                <th style={{padding: '1rem', textAlign: 'left'}}>Role</th>
                <th style={{padding: '1rem', textAlign: 'left'}}>Registered</th>
              </tr>
            </thead>
            <tbody>
              {customers.map(customer => (
                <tr key={customer.id} style={{borderBottom: '1px solid #f1f5f9'}}>
                  <td style={{padding: '1rem'}}>{customer.name}</td>
                  <td style={{padding: '1rem'}}>{customer.email}</td>
                  <td style={{padding: '1rem'}}>
                    <span style={{
                      padding: '0.25rem 0.75rem',
                      borderRadius: '999px',
                      fontSize: '0.875rem',
                      fontWeight: 600,
                      background: customer.role === 'admin' ? '#fef3c7' : '#dbeafe',
                      color: customer.role === 'admin' ? '#92400e' : '#1e40af'
                    }}>
                      {customer.role}
                    </span>
                  </td>
                  <td style={{padding: '1rem', color: '#64748b'}}>
                    {new Date(customer.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {customers.length === 0 && (
            <div style={{textAlign: 'center', padding: '3rem'}}>
              <Users size={48} style={{margin: '0 auto', color: '#cbd5e1', marginBottom: '1rem'}} />
              <p style={{color: '#64748b'}}>No customers yet</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}