import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { ShoppingCart, User, LogOut, Package } from "lucide-react";
import { AuthContext } from "@/App";

export default function Navbar({ cartCount = 0 }) {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand" data-testid="navbar-brand">
          <Package size={28} />
          Alexouko's Store
        </Link>
        <div className="navbar-links">
          <Link to="/" className="navbar-link">Home</Link>
          <Link to="/category/Electronics" className="navbar-link" style={{background: '#3b82f6', color: 'white', padding: '0.5rem 1rem', borderRadius: '6px', fontWeight: 600}}>Electronics</Link>
          <Link to="/category/Home%20%26%20Living" className="navbar-link" style={{background: '#10b981', color: 'white', padding: '0.5rem 1rem', borderRadius: '6px', fontWeight: 600}}>Home & Living</Link>
          <Link to="/daily-offers" className="navbar-link" style={{color: '#f59e0b', fontWeight: 600}}>Daily Offers</Link>
          <Link to="/reviews" className="navbar-link">Reviews</Link>
          <Link to="/social" className="navbar-link">Socials</Link>
          <Link to="/cart" className="navbar-link" data-testid="cart-link">
            <ShoppingCart size={20} />
            Cart {cartCount > 0 && <span className="cart-badge" data-testid="cart-count">{cartCount}</span>}
          </Link>
          {user ? (
            <>
              {user.role === "admin" && (
                <Link to="/admin" className="navbar-link" data-testid="admin-link">
                  Admin
                </Link>
              )}
              <Link to="/orders" className="navbar-link" data-testid="orders-link">
                Orders
              </Link>
              <button onClick={logout} className="navbar-link" style={{background: 'none', border: 'none', cursor: 'pointer'}} data-testid="logout-btn">
                <LogOut size={20} /> Logout
              </button>
            </>
          ) : (
            <Link to="/auth" className="navbar-link" data-testid="login-link">
              <User size={20} /> Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
