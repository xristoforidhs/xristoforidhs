import { useState } from "react";
import { Link } from "react-router-dom";
import { ChevronDown } from "lucide-react";

export default function CategoryDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  const categories = [
    { name: "Electronics", path: "/category/Electronics" },
    { name: "Home & Living", path: "/category/Home & Living" }
  ];

  return (
    <div 
      style={{position: 'relative'}}
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <button 
        className="navbar-link"
        style={{
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '0.25rem'
        }}
      >
        Categories <ChevronDown size={16} />
      </button>
      
      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          background: 'white',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          padding: '0.5rem',
          minWidth: '180px',
          marginTop: '0.5rem',
          zIndex: 1000
        }}>
          {categories.map(cat => (
            <Link
              key={cat.name}
              to={cat.path}
              style={{
                display: 'block',
                padding: '0.75rem 1rem',
                color: '#475569',
                textDecoration: 'none',
                borderRadius: '6px',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.background = '#f1f5f9'}
              onMouseLeave={(e) => e.target.style.background = 'transparent'}
            >
              {cat.name}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
