import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { Send, Mail } from "lucide-react";
import { toast } from "sonner";

export default function Footer() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [socialSettings, setSocialSettings] = useState({
    tiktok_url: "",
    instagram_url: "",
    facebook_url: "",
    twitter_url: ""
  });

  useEffect(() => {
    fetchSocialSettings();
  }, []);

  const fetchSocialSettings = async () => {
    try {
      const response = await axios.get(`${API}/settings/public`);
      setSocialSettings(response.data);
    } catch (error) {
      console.error("Failed to fetch social settings", error);
    }
  };

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      toast.error("Please enter your email");
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/newsletter/subscribe`, { email });
      toast.success("Successfully subscribed to newsletter!");
      setEmail("");
    } catch (error) {
      console.error("Failed to subscribe", error);
      toast.error("Failed to subscribe. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <footer style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      padding: '4rem 2rem 2rem 2rem',
      marginTop: '4rem'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '3rem',
        marginBottom: '3rem'
      }}>
        {/* About Section */}
        <div>
          <h3 style={{fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem'}}>Alexouko's Store</h3>
          <p style={{opacity: 0.9, lineHeight: 1.6, marginBottom: '1rem'}}>
            Your trusted destination for quality products at great prices. We offer a wide selection of electronics, home goods, and more.
          </p>
          <div style={{marginTop: '1.5rem'}}>
            <h4 style={{fontSize: '1.125rem', fontWeight: 600, marginBottom: '0.75rem'}}>Quick Links</h4>
            <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
              <Link to="/" style={{color: 'white', opacity: 0.9, textDecoration: 'none'}}>Home</Link>
              <Link to="/daily-offers" style={{color: 'white', opacity: 0.9, textDecoration: 'none'}}>Daily Offers</Link>
              <Link to="/reviews" style={{color: 'white', opacity: 0.9, textDecoration: 'none'}}>Customer Reviews</Link>
              <Link to="/social" style={{color: 'white', opacity: 0.9, textDecoration: 'none'}}>Social Media</Link>
            </div>
          </div>
        </div>

        {/* Newsletter Section */}
        <div>
          <h3 style={{fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Mail size={24} /> Newsletter
          </h3>
          <p style={{opacity: 0.9, lineHeight: 1.6, marginBottom: '1.5rem'}}>
            Subscribe to get special offers, free giveaways, and once-in-a-lifetime deals.
          </p>
          <form onSubmit={handleNewsletterSubmit} style={{display: 'flex', gap: '0.5rem'}}>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                flex: 1,
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                border: 'none',
                fontSize: '1rem'
              }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '0.75rem 1.5rem',
                background: '#22c55e',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                opacity: loading ? 0.7 : 1
              }}
            >
              <Send size={18} /> {loading ? 'Sending...' : 'Subscribe'}
            </button>
          </form>
        </div>

        {/* Social Media & Trustpilot */}
        <div>
          <h3 style={{fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem'}}>Connect With Us</h3>
          <div style={{display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap'}}>
            {socialSettings.instagram_url && (
              <a 
                href={socialSettings.instagram_url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '0.75rem 1.25rem',
                  borderRadius: '8px',
                  color: 'white',
                  textDecoration: 'none',
                  fontWeight: 600,
                  transition: 'background 0.2s'
                }}
              >
                📷 Instagram
              </a>
            )}
            {socialSettings.tiktok_url && (
              <a 
                href={socialSettings.tiktok_url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '0.75rem 1.25rem',
                  borderRadius: '8px',
                  color: 'white',
                  textDecoration: 'none',
                  fontWeight: 600,
                  transition: 'background 0.2s'
                }}
              >
                🎵 TikTok
              </a>
            )}
            {socialSettings.facebook_url && (
              <a 
                href={socialSettings.facebook_url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '0.75rem 1.25rem',
                  borderRadius: '8px',
                  color: 'white',
                  textDecoration: 'none',
                  fontWeight: 600,
                  transition: 'background 0.2s'
                }}
              >
                👍 Facebook
              </a>
            )}
            {socialSettings.twitter_url && (
              <a 
                href={socialSettings.twitter_url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '0.75rem 1.25rem',
                  borderRadius: '8px',
                  color: 'white',
                  textDecoration: 'none',
                  fontWeight: 600,
                  transition: 'background 0.2s'
                }}
              >
                🐦 Twitter
              </a>
            )}
          </div>

          {/* Trustpilot Widget */}
          <div>
            <h4 style={{fontSize: '1.125rem', fontWeight: 600, marginBottom: '0.75rem'}}>Trusted by Customers</h4>
            <div 
              className="trustpilot-widget" 
              data-locale="en-US" 
              data-template-id="5419b6a8b0d04a076446a9ad" 
              data-businessunit-id="YOUR_BUSINESS_UNIT_ID" 
              data-style-height="24px" 
              data-style-width="100%" 
              data-theme="dark"
              style={{
                background: 'rgba(255,255,255,0.1)',
                padding: '1rem',
                borderRadius: '8px',
                textAlign: 'center'
              }}
            >
              <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', justifyContent: 'center'}}>
                <span style={{fontSize: '1.5rem'}}>⭐⭐⭐⭐⭐</span>
                <span style={{fontWeight: 600}}>Excellent</span>
              </div>
              <p style={{fontSize: '0.875rem', opacity: 0.8, marginTop: '0.5rem'}}>
                Based on 1,247 reviews
              </p>
              <p style={{fontSize: '0.75rem', opacity: 0.7, marginTop: '0.25rem'}}>
                Trustpilot
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div style={{
        borderTop: '1px solid rgba(255,255,255,0.2)',
        paddingTop: '2rem',
        textAlign: 'center'
      }}>
        <p style={{opacity: 0.9}}>© 2025 Alexouko's Store - Your trusted e-commerce destination</p>
        <p style={{opacity: 0.7, fontSize: '0.875rem', marginTop: '0.5rem'}}>
          All rights reserved. Powered by CJ Dropshipping.
        </p>
      </div>
    </footer>
  );
}
