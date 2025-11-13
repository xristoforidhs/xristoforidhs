import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ArrowLeft, Palette, Save, Upload, Image as ImageIcon, Type, Layout } from "lucide-react";
import Navbar from "@/components/Navbar";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ThemeCustomizer() {
  const [theme, setTheme] = useState({
    primary_color: '#2563eb',
    secondary_color: '#764ba2',
    background_color: '#f5f7fa',
    text_color: '#1a202c',
    font_heading: 'Space Grotesk',
    font_body: 'Inter',
    hero_background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    button_style: 'rounded',
    layout_width: 'wide',
    product_card_size: 'medium',
    header_height: 'normal',
    background_image: '',
    show_background_image: false
  });
  const [backgroundFile, setBackgroundFile] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchTheme();
  }, []);

  const fetchTheme = async () => {
    try {
      const response = await axios.get(`${API}/theme`);
      setTheme(response.data);
    } catch (error) {
      console.error("Failed to fetch theme", error);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await axios.put(`${API}/theme`, theme);
      toast.success("Theme saved! Refresh page to see changes.");
      // Apply theme immediately
      applyTheme();
    } catch (error) {
      toast.error("Failed to save theme");
    } finally {
      setSaving(false);
    }
  };

  const applyTheme = () => {
    document.documentElement.style.setProperty('--primary-color', theme.primary_color);
    document.documentElement.style.setProperty('--secondary-color', theme.secondary_color);
    document.documentElement.style.setProperty('--background-color', theme.background_color);
    document.documentElement.style.setProperty('--text-color', theme.text_color);
  };

  const presetThemes = [
    { name: "Default Blue", primary: '#2563eb', secondary: '#764ba2', bg: '#f5f7fa' },
    { name: "Ocean", primary: '#0891b2', secondary: '#06b6d4', bg: '#ecfeff' },
    { name: "Forest", primary: '#059669', secondary: '#10b981', bg: '#f0fdf4' },
    { name: "Sunset", primary: '#f59e0b', secondary: '#ef4444', bg: '#fffbeb' },
    { name: "Purple", primary: '#7c3aed', secondary: '#a78bfa', bg: '#faf5ff' },
    { name: "Dark", primary: '#1f2937', secondary: '#374151', bg: '#111827' }
  ];

  const applyPreset = (preset) => {
    setTheme(prev => ({
      ...prev,
      primary_color: preset.primary,
      secondary_color: preset.secondary,
      background_color: preset.bg
    }));
  };

  const handleBackgroundUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setBackgroundFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setTheme(prev => ({
          ...prev,
          background_image: e.target.result,
          show_background_image: true
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div>
      <Navbar />

      <div style={{maxWidth: '1200px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/admin" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}}>
          <ArrowLeft size={20} /> Back to Admin
        </Link>

        <div style={{display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '2rem', marginBottom: '2rem'}}>
          <Palette size={32} />
          <h1 className="section-title" style={{marginBottom: 0}}>Theme Customization</h1>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem'}}>
          {/* Controls */}
          <div>
            <Card className="mb-4">
              <CardHeader>
                <CardTitle>Quick Presets</CardTitle>
                <CardDescription>Choose a pre-made theme</CardDescription>
              </CardHeader>
              <CardContent>
                <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem'}}>
                  {presetThemes.map(preset => (
                    <button
                      key={preset.name}
                      onClick={() => applyPreset(preset)}
                      style={{
                        padding: '1rem',
                        borderRadius: '8px',
                        border: '2px solid #e2e8f0',
                        background: preset.bg,
                        cursor: 'pointer',
                        textAlign: 'center'
                      }}
                    >
                      <div style={{display: 'flex', gap: '0.25rem', marginBottom: '0.5rem', justifyContent: 'center'}}>
                        <div style={{width: '20px', height: '20px', background: preset.primary, borderRadius: '4px'}} />
                        <div style={{width: '20px', height: '20px', background: preset.secondary, borderRadius: '4px'}} />
                      </div>
                      <div style={{fontSize: '0.875rem', fontWeight: 600}}>{preset.name}</div>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="mb-4">
              <CardHeader>
                <CardTitle>Colors</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Primary Color</Label>
                  <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
                    <input
                      type="color"
                      value={theme.primary_color}
                      onChange={(e) => setTheme({...theme, primary_color: e.target.value})}
                      style={{width: '60px', height: '40px', cursor: 'pointer'}}
                    />
                    <Input value={theme.primary_color} onChange={(e) => setTheme({...theme, primary_color: e.target.value})} />
                  </div>
                </div>
                <div>
                  <Label>Secondary Color</Label>
                  <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
                    <input
                      type="color"
                      value={theme.secondary_color}
                      onChange={(e) => setTheme({...theme, secondary_color: e.target.value})}
                      style={{width: '60px', height: '40px', cursor: 'pointer'}}
                    />
                    <Input value={theme.secondary_color} onChange={(e) => setTheme({...theme, secondary_color: e.target.value})} />
                  </div>
                </div>
                <div>
                  <Label>Background Color</Label>
                  <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
                    <input
                      type="color"
                      value={theme.background_color}
                      onChange={(e) => setTheme({...theme, background_color: e.target.value})}
                      style={{width: '60px', height: '40px', cursor: 'pointer'}}
                    />
                    <Input value={theme.background_color} onChange={(e) => setTheme({...theme, background_color: e.target.value})} />
                  </div>
                </div>
                <div>
                  <Label>Text Color</Label>
                  <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
                    <input
                      type="color"
                      value={theme.text_color}
                      onChange={(e) => setTheme({...theme, text_color: e.target.value})}
                      style={{width: '60px', height: '40px', cursor: 'pointer'}}
                    />
                    <Input value={theme.text_color} onChange={(e) => setTheme({...theme, text_color: e.target.value})} />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="mb-4">
              <CardHeader>
                <CardTitle>Typography</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Heading Font</Label>
                  <select
                    value={theme.font_heading}
                    onChange={(e) => setTheme({...theme, font_heading: e.target.value})}
                    style={{width: '100%', padding: '0.5rem', borderRadius: '8px', border: '2px solid #e2e8f0'}}
                  >
                    <option value="Space Grotesk">Space Grotesk</option>
                    <option value="Playfair Display">Playfair Display</option>
                    <option value="Bebas Neue">Bebas Neue</option>
                    <option value="Montserrat">Montserrat</option>
                  </select>
                </div>
                <div>
                  <Label>Body Font</Label>
                  <select
                    value={theme.font_body}
                    onChange={(e) => setTheme({...theme, font_body: e.target.value})}
                    style={{width: '100%', padding: '0.5rem', borderRadius: '8px', border: '2px solid #e2e8f0'}}
                  >
                    <option value="Inter">Inter</option>
                    <option value="Roboto">Roboto</option>
                    <option value="Open Sans">Open Sans</option>
                    <option value="Lato">Lato</option>
                  </select>
                </div>
              </CardContent>
            </Card>

            <Card className="mb-4">
              <CardHeader>
                <CardTitle>Button Style</CardTitle>
              </CardHeader>
              <CardContent>
                <div style={{display: 'flex', gap: '1rem'}}>
                  {['rounded', 'square', 'pill'].map(style => (
                    <button
                      key={style}
                      onClick={() => setTheme({...theme, button_style: style})}
                      style={{
                        padding: '0.75rem 1.5rem',
                        background: theme.button_style === style ? theme.primary_color : '#f1f5f9',
                        color: theme.button_style === style ? 'white' : '#475569',
                        border: 'none',
                        borderRadius: style === 'rounded' ? '8px' : style === 'square' ? '0' : '999px',
                        cursor: 'pointer',
                        fontWeight: 600
                      }}
                    >
                      {style.charAt(0).toUpperCase() + style.slice(1)}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Button onClick={handleSave} disabled={saving} style={{width: '100%', padding: '1rem'}}>
              <Save size={20} /> {saving ? 'Saving...' : 'Save Theme'}
            </Button>
          </div>

          {/* Preview */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Live Preview</CardTitle>
                <CardDescription>See how your theme looks</CardDescription>
              </CardHeader>
              <CardContent>
                <div style={{
                  background: theme.background_color,
                  padding: '2rem',
                  borderRadius: '8px',
                  border: '2px solid #e2e8f0'
                }}>
                  {/* Hero Preview */}
                  <div style={{
                    background: theme.hero_background,
                    padding: '3rem 2rem',
                    borderRadius: '8px',
                    marginBottom: '2rem',
                    textAlign: 'center'
                  }}>
                    <h1 style={{fontFamily: theme.font_heading, color: 'white', fontSize: '2rem', marginBottom: '1rem'}}>Alexouko's Store</h1>
                    <p style={{fontFamily: theme.font_body, color: 'white', opacity: 0.9}}>Quality Products, Great Prices</p>
                  </div>

                  {/* Content Preview */}
                  <div style={{marginBottom: '2rem'}}>
                    <h2 style={{fontFamily: theme.font_heading, color: theme.text_color, fontSize: '1.5rem', marginBottom: '1rem'}}>Sample Heading</h2>
                    <p style={{fontFamily: theme.font_body, color: theme.text_color, marginBottom: '1rem'}}>This is how your body text will look with the selected font and colors.</p>
                  </div>

                  {/* Button Preview */}
                  <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap'}}>
                    <button style={{
                      padding: '0.75rem 1.5rem',
                      background: theme.primary_color,
                      color: 'white',
                      border: 'none',
                      borderRadius: theme.button_style === 'rounded' ? '8px' : theme.button_style === 'square' ? '0' : '999px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}>Primary Button</button>
                    <button style={{
                      padding: '0.75rem 1.5rem',
                      background: theme.secondary_color,
                      color: 'white',
                      border: 'none',
                      borderRadius: theme.button_style === 'rounded' ? '8px' : theme.button_style === 'square' ? '0' : '999px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}>Secondary Button</button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}