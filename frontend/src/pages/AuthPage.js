import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { Package } from "lucide-react";
import { toast } from "sonner";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = isLogin ? "/auth/login" : "/auth/register";
      const payload = isLogin ? { email, password } : { email, password, name };
      
      const response = await axios.post(`${API}${endpoint}`, payload);
      login(response.data.token, response.data.user);
      toast.success(isLogin ? "Επιτυχής σύνδεση!" : "Λογαριασμός δημιουργήθηκε!");
      navigate("/");
    } catch (error) {
      console.error("Auth error:", error);
      toast.error(error.response?.data?.detail || "Κάτι πήγε στραβά");
    } finally {
      setLoading(false);
    }
  };

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

      <div style={{minHeight: 'calc(100vh - 80px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem'}}>
        <div style={{width: '100%', maxWidth: '400px', background: 'white', borderRadius: '16px', padding: '3rem', boxShadow: '0 8px 24px rgba(0,0,0,0.12)'}}>
          <h1 style={{fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem', textAlign: 'center'}} data-testid="auth-title">
            {isLogin ? 'Login' : 'Sign Up'}
          </h1>
          <p style={{color: '#64748b', textAlign: 'center', marginBottom: '2rem'}}>
            {isLogin ? 'Welcome back!' : 'Create your account'}
          </p>

          {!isLogin && (
            <div style={{marginBottom: '2rem'}}>
              <div style={{display: 'flex', gap: '0.5rem', marginBottom: '1rem'}}>
                <button 
                  type="button"
                  onClick={() => toast.info("Google Sign In coming soon!")}
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    border: '2px solid #e2e8f0',
                    borderRadius: '8px',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    fontSize: '0.875rem',
                    fontWeight: 600
                  }}
                >
                  <img src="https://www.google.com/favicon.ico" alt="Google" style={{width: '18px', height: '18px'}} />
                  Google
                </button>
                <button 
                  type="button"
                  onClick={() => toast.info("Apple Sign In coming soon!")}
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    border: '2px solid #e2e8f0',
                    borderRadius: '8px',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    fontSize: '0.875rem',
                    fontWeight: 600
                  }}
                >
                  🍎 Apple
                </button>
              </div>
              <div style={{textAlign: 'center', color: '#64748b', fontSize: '0.875rem', marginBottom: '1rem'}}>or</div>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <div style={{marginBottom: '1.5rem'}}>
                <label style={{display: 'block', marginBottom: '0.5rem', fontWeight: 600, fontSize: '0.875rem'}}>Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '2px solid #e2e8f0',
                    fontSize: '1rem'
                  }}
                  data-testid="name-input"
                />
              </div>
            )}

            <div style={{marginBottom: '1.5rem'}}>
              <label style={{display: 'block', marginBottom: '0.5rem', fontWeight: 600, fontSize: '0.875rem'}}>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '2px solid #e2e8f0',
                  fontSize: '1rem'
                }}
                data-testid="email-input"
              />
            </div>

            <div style={{marginBottom: '2rem'}}>
              <label style={{display: 'block', marginBottom: '0.5rem', fontWeight: 600, fontSize: '0.875rem'}}>Κωδικός</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '2px solid #e2e8f0',
                  fontSize: '1rem'
                }}
                data-testid="password-input"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="btn btn-primary" 
              style={{width: '100%', marginBottom: '1rem'}}
              data-testid="submit-btn"
            >
              {loading ? 'Παρακαλώ περιμένετε...' : (isLogin ? 'Σύνδεση' : 'Εγγραφή')}
            </button>
          </form>

          <p style={{textAlign: 'center', color: '#64748b', fontSize: '0.875rem'}}>
            {isLogin ? 'Δεν έχετε λογαριασμό;' : 'Έχετε ήδη λογαριασμό;'}
            {' '}
            <button 
              onClick={() => setIsLogin(!isLogin)}
              style={{background: 'none', border: 'none', color: '#2563eb', fontWeight: 600, cursor: 'pointer'}}
              data-testid="toggle-auth-mode"
            >
              {isLogin ? 'Εγγραφή' : 'Σύνδεση'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}