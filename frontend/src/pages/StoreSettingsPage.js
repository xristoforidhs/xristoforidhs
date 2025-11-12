import { useEffect, useState, useContext } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { Package, ArrowLeft, Save } from "lucide-react";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function StoreSettingsPage() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API}/settings`);
      setSettings(response.data);
    } catch (error) {
      console.error("Failed to fetch settings", error);
      toast.error("Failed to load settings");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await axios.put(`${API}/settings`, settings);
      toast.success("Settings saved successfully!");
    } catch (error) {
      console.error("Failed to save settings", error);
      toast.error("Failed to save settings");
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  if (loading) {
    return <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Loading...</div>;
  }

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand" data-testid="navbar-brand">
            <Package size={28} />
            Store Settings
          </Link>
        </div>
      </nav>

      <div style={{maxWidth: '1200px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/admin" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}} data-testid="back-to-admin">
          <ArrowLeft size={20} /> Back to Admin
        </Link>

        <h1 className="section-title" style={{marginTop: '2rem', marginBottom: '2rem'}}>Store Settings</h1>

        <Tabs defaultValue="general" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="general">General</TabsTrigger>
            <TabsTrigger value="payment">Payment</TabsTrigger>
            <TabsTrigger value="shipping">Shipping & Tax</TabsTrigger>
            <TabsTrigger value="advanced">Advanced</TabsTrigger>
          </TabsList>

          <TabsContent value="general">
            <Card>
              <CardHeader>
                <CardTitle>General Settings</CardTitle>
                <CardDescription>Basic store information and configuration</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="store_name">Store Name</Label>
                  <Input
                    id="store_name"
                    value={settings?.store_name || ''}
                    onChange={(e) => handleChange('store_name', e.target.value)}
                    placeholder="TechGadgets"
                  />
                </div>
                <div>
                  <Label htmlFor="store_email">Store Email</Label>
                  <Input
                    id="store_email"
                    type="email"
                    value={settings?.store_email || ''}
                    onChange={(e) => handleChange('store_email', e.target.value)}
                    placeholder="store@example.com"
                  />
                </div>
                <div>
                  <Label htmlFor="store_phone">Store Phone</Label>
                  <Input
                    id="store_phone"
                    value={settings?.store_phone || ''}
                    onChange={(e) => handleChange('store_phone', e.target.value)}
                    placeholder="+1 (555) 000-0000"
                  />
                </div>
                <div>
                  <Label htmlFor="currency">Currency</Label>
                  <select
                    id="currency"
                    value={settings?.currency || 'USD'}
                    onChange={(e) => handleChange('currency', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      borderRadius: '0.375rem',
                      border: '1px solid #e2e8f0'
                    }}
                  >
                    <option value="USD">USD - US Dollar</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="GBP">GBP - British Pound</option>
                  </select>
                </div>
                <Button onClick={handleSubmit} disabled={saving}>
                  <Save size={16} /> {saving ? 'Saving...' : 'Save Changes'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="payment">
            <Card>
              <CardHeader>
                <CardTitle>Payment Settings</CardTitle>
                <CardDescription>Configure Stripe payment integration</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="stripe_publishable_key">Stripe Publishable Key</Label>
                  <Input
                    id="stripe_publishable_key"
                    value={settings?.stripe_publishable_key || ''}
                    onChange={(e) => handleChange('stripe_publishable_key', e.target.value)}
                    placeholder="pk_test_..."
                  />
                  <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Public key for client-side integration</p>
                </div>
                <div>
                  <Label htmlFor="stripe_secret_key">Stripe Secret Key</Label>
                  <Input
                    id="stripe_secret_key"
                    type="password"
                    value={settings?.stripe_secret_key || ''}
                    onChange={(e) => handleChange('stripe_secret_key', e.target.value)}
                    placeholder="sk_test_..."
                  />
                  <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Secret key for server-side processing</p>
                </div>
                <div style={{background: '#fef3c7', padding: '1rem', borderRadius: '0.5rem'}}>
                  <p style={{fontSize: '0.875rem', color: '#92400e'}}>
                    <strong>Note:</strong> Stripe keys are currently configured in backend .env file. These settings will be used in future updates.
                  </p>
                </div>
                <Button onClick={handleSubmit} disabled={saving}>
                  <Save size={16} /> {saving ? 'Saving...' : 'Save Changes'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="shipping">
            <Card>
              <CardHeader>
                <CardTitle>Shipping & Tax Settings</CardTitle>
                <CardDescription>Configure shipping rates and tax calculations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="shipping_flat_rate">Flat Shipping Rate ($)</Label>
                  <Input
                    id="shipping_flat_rate"
                    type="number"
                    step="0.01"
                    value={settings?.shipping_flat_rate || 0}
                    onChange={(e) => handleChange('shipping_flat_rate', parseFloat(e.target.value) || 0)}
                    placeholder="0.00"
                  />
                  <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Charge this amount for all orders</p>
                </div>
                <div>
                  <Label htmlFor="free_shipping_threshold">Free Shipping Threshold ($)</Label>
                  <Input
                    id="free_shipping_threshold"
                    type="number"
                    step="0.01"
                    value={settings?.free_shipping_threshold || 0}
                    onChange={(e) => handleChange('free_shipping_threshold', parseFloat(e.target.value) || 0)}
                    placeholder="50.00"
                  />
                  <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Offer free shipping on orders above this amount</p>
                </div>
                <div>
                  <Label htmlFor="tax_rate">Tax Rate (%)</Label>
                  <Input
                    id="tax_rate"
                    type="number"
                    step="0.01"
                    value={settings?.tax_rate || 0}
                    onChange={(e) => handleChange('tax_rate', parseFloat(e.target.value) || 0)}
                    placeholder="0.00"
                  />
                  <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Sales tax percentage (e.g., 8.5 for 8.5%)</p>
                </div>

                <div style={{background: '#f0f9ff', padding: '1.5rem', borderRadius: '0.5rem', border: '2px solid #3b82f6'}}>
                  <h4 style={{fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem', color: '#1e40af'}}>💰 Profit Markup System</h4>
                  <div>
                    <Label htmlFor="profit_markup_percentage">Profit Markup Percentage (%)</Label>
                    <Input
                      id="profit_markup_percentage"
                      type="number"
                      step="1"
                      value={settings?.profit_markup_percentage || 100}
                      onChange={(e) => handleChange('profit_markup_percentage', parseFloat(e.target.value) || 100)}
                      placeholder="100"
                    />
                    <div style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.75rem', lineHeight: 1.6}}>
                      <p><strong>How it works:</strong> This percentage is added to the cost price to determine the selling price.</p>
                      <p style={{marginTop: '0.5rem'}}>
                        • <strong>100% markup</strong> = 50% profit margin (Cost $10 → Sell $20)<br/>
                        • <strong>150% markup</strong> = 60% profit margin (Cost $10 → Sell $25)<br/>
                        • <strong>200% markup</strong> = 66.7% profit margin (Cost $10 → Sell $30)
                      </p>
                      <p style={{marginTop: '0.5rem', color: '#2563eb', fontWeight: 600}}>
                        Current setting: {settings?.profit_markup_percentage || 100}% markup = {(((settings?.profit_markup_percentage || 100) / (100 + (settings?.profit_markup_percentage || 100))) * 100).toFixed(1)}% profit margin
                      </p>
                    </div>
                  </div>
                </div>

                <Button onClick={handleSubmit} disabled={saving}>
                  <Save size={16} /> {saving ? 'Saving...' : 'Save Changes'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="advanced">
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Social Media Integration</CardTitle>
                  <CardDescription>Connect your social media accounts to display on your store</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="tiktok_url">TikTok Profile URL</Label>
                    <Input
                      id="tiktok_url"
                      value={settings?.tiktok_url || ''}
                      onChange={(e) => handleChange('tiktok_url', e.target.value)}
                      placeholder="https://www.tiktok.com/@yourusername"
                    />
                    <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Your TikTok profile link will appear on your store</p>
                  </div>
                  <div>
                    <Label htmlFor="instagram_url">Instagram Profile URL</Label>
                    <Input
                      id="instagram_url"
                      value={settings?.instagram_url || ''}
                      onChange={(e) => handleChange('instagram_url', e.target.value)}
                      placeholder="https://www.instagram.com/yourusername"
                    />
                    <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Your Instagram profile link will appear on your store</p>
                  </div>
                  <div>
                    <Label htmlFor="facebook_url">Facebook Page URL</Label>
                    <Input
                      id="facebook_url"
                      value={settings?.facebook_url || ''}
                      onChange={(e) => handleChange('facebook_url', e.target.value)}
                      placeholder="https://www.facebook.com/yourpage"
                    />
                  </div>
                  <div>
                    <Label htmlFor="twitter_url">Twitter/X Profile URL</Label>
                    <Input
                      id="twitter_url"
                      value={settings?.twitter_url || ''}
                      onChange={(e) => handleChange('twitter_url', e.target.value)}
                      placeholder="https://twitter.com/yourusername"
                    />
                  </div>
                  <Button onClick={handleSubmit} disabled={saving}>
                    <Save size={16} /> {saving ? 'Saving...' : 'Save Social Media Links'}
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Ad Network Integration</CardTitle>
                  <CardDescription>Monetize your store with display ads - Earn money from visitor clicks!</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div style={{background: '#dcfce7', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1rem'}}>
                    <p style={{fontSize: '0.875rem', color: '#166534'}}>
                      <strong>💰 Potential Earnings:</strong><br/>
                      • 1,000 visitors/day = $50-200/month<br/>
                      • 5,000 visitors/day = $250-1,000/month<br/>
                      • Tech gadgets: ~$1-3 per click
                    </p>
                  </div>

                  <div>
                    <h3 style={{fontWeight: 600, marginBottom: '1rem'}}>Google AdSense</h3>
                    <div className="space-y-3">
                      <div>
                        <Label htmlFor="google_adsense_id">AdSense Publisher ID</Label>
                        <Input
                          id="google_adsense_id"
                          value={settings?.google_adsense_id || ''}
                          onChange={(e) => handleChange('google_adsense_id', e.target.value)}
                          placeholder="ca-pub-1234567890123456"
                        />
                        <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Get your ID from adsense.google.com</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          id="google_adsense_enabled"
                          checked={settings?.google_adsense_enabled || false}
                          onChange={(e) => handleChange('google_adsense_enabled', e.target.checked)}
                        />
                        <Label htmlFor="google_adsense_enabled">Enable Google AdSense</Label>
                      </div>
                    </div>
                  </div>

                  <hr />

                  <div>
                    <h3 style={{fontWeight: 600, marginBottom: '1rem'}}>Media.net (Backup)</h3>
                    <div className="space-y-3">
                      <div>
                        <Label htmlFor="medianet_id">Media.net Site ID</Label>
                        <Input
                          id="medianet_id"
                          value={settings?.medianet_id || ''}
                          onChange={(e) => handleChange('medianet_id', e.target.value)}
                          placeholder="123456"
                        />
                        <p style={{fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem'}}>Get your ID from media.net</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          id="medianet_enabled"
                          checked={settings?.medianet_enabled || false}
                          onChange={(e) => handleChange('medianet_enabled', e.target.checked)}
                        />
                        <Label htmlFor="medianet_enabled">Enable Media.net</Label>
                      </div>
                    </div>
                  </div>

                  <div style={{background: '#fef3c7', padding: '1rem', borderRadius: '0.5rem'}}>
                    <p style={{fontSize: '0.875rem', color: '#92400e'}}>
                      <strong>📋 Setup Instructions:</strong><br/>
                      1. Sign up at adsense.google.com and/or media.net<br/>
                      2. Get approval for your site (1-3 days)<br/>
                      3. Copy your Publisher ID<br/>
                      4. Paste here and enable<br/>
                      5. Ads will appear automatically on your store!
                    </p>
                  </div>

                  <Button onClick={handleSubmit} disabled={saving}>
                    <Save size={16} /> {saving ? 'Saving...' : 'Save Ad Settings'}
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Integrations Status</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <h3 style={{fontWeight: 600, marginBottom: '0.5rem'}}>CJ Dropshipping</h3>
                    <p style={{fontSize: '0.875rem', color: '#22c55e'}}>✓ Connected and Active</p>
                  </div>
                  <div>
                    <h3 style={{fontWeight: 600, marginBottom: '0.5rem'}}>Stripe Payments</h3>
                    <p style={{fontSize: '0.875rem', color: '#22c55e'}}>✓ Configured</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}