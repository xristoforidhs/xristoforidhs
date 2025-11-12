import { useEffect, useState } from "react";
import axios from "axios";
import { API } from "@/App";
import Navbar from "@/components/Navbar";

export default function SocialPage() {
  const [settings, setSettings] = useState(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API}/settings/public`);
      setSettings(response.data);
    } catch (error) {
      console.error("Failed to fetch settings", error);
    }
  };

  return (
    <div>
      <Navbar />

      <div style={{maxWidth: '800px', margin: '4rem auto', padding: '2rem', textAlign: 'center'}}>
        <h1 style={{fontSize: '3rem', fontWeight: 700, marginBottom: '1rem'}}>Follow Us</h1>
        <p style={{fontSize: '1.25rem', color: '#64748b', marginBottom: '3rem'}}>Stay connected on social media for exclusive deals and updates!</p>

        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem'}}>
          {settings?.tiktok_url && (
            <a href={settings.tiktok_url} target="_blank" rel="noopener noreferrer" style={{
              background: 'linear-gradient(135deg, #000000 0%, #ee1d52 100%)',
              color: 'white',
              padding: '2rem',
              borderRadius: '16px',
              textDecoration: 'none',
              transition: 'transform 0.2s'
            }} className="social-card">
              <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🎵</div>
              <h3 style={{fontSize: '1.5rem', fontWeight: 600}}>TikTok</h3>
              <p style={{opacity: 0.9, marginTop: '0.5rem'}}>Watch our videos</p>
            </a>
          )}

          {settings?.instagram_url && (
            <a href={settings.instagram_url} target="_blank" rel="noopener noreferrer" style={{
              background: 'linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)',
              color: 'white',
              padding: '2rem',
              borderRadius: '16px',
              textDecoration: 'none',
              transition: 'transform 0.2s'
            }} className="social-card">
              <div style={{fontSize: '3rem', marginBottom: '1rem'}}>📸</div>
              <h3 style={{fontSize: '1.5rem', fontWeight: 600}}>Instagram</h3>
              <p style={{opacity: 0.9, marginTop: '0.5rem'}}>See our photos</p>
            </a>
          )}

          {settings?.facebook_url && (
            <a href={settings.facebook_url} target="_blank" rel="noopener noreferrer" style={{
              background: 'linear-gradient(135deg, #3b5998 0%, #4c70ba 100%)',
              color: 'white',
              padding: '2rem',
              borderRadius: '16px',
              textDecoration: 'none',
              transition: 'transform 0.2s'
            }} className="social-card">
              <div style={{fontSize: '3rem', marginBottom: '1rem'}}>👥</div>
              <h3 style={{fontSize: '1.5rem', fontWeight: 600}}>Facebook</h3>
              <p style={{opacity: 0.9, marginTop: '0.5rem'}}>Join our community</p>
            </a>
          )}

          {settings?.twitter_url && (
            <a href={settings.twitter_url} target="_blank" rel="noopener noreferrer" style={{
              background: 'linear-gradient(135deg, #000000 0%, #1da1f2 100%)',
              color: 'white',
              padding: '2rem',
              borderRadius: '16px',
              textDecoration: 'none',
              transition: 'transform 0.2s'
            }} className="social-card">
              <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🐦</div>
              <h3 style={{fontSize: '1.5rem', fontWeight: 600}}>Twitter/X</h3>
              <p style={{opacity: 0.9, marginTop: '0.5rem'}}>Follow for updates</p>
            </a>
          )}
        </div>

        {!settings?.tiktok_url && !settings?.instagram_url && !settings?.facebook_url && !settings?.twitter_url && (
          <div style={{padding: '3rem', background: '#f1f5f9', borderRadius: '16px'}}>
            <p style={{fontSize: '1.125rem', color: '#64748b'}}>Social media links coming soon!</p>
          </div>
        )}
      </div>

      <style>{`
        .social-card:hover {
          transform: translateY(-8px);
          box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        }
      `}</style>
    </div>
  );
}