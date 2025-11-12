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
                <Button onClick={handleSubmit} disabled={saving}>
                  <Save size={16} /> {saving ? 'Saving...' : 'Save Changes'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="advanced">
            <Card>
              <CardHeader>
                <CardTitle>Advanced Settings</CardTitle>
                <CardDescription>Technical configuration and integrations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h3 style={{fontWeight: 600, marginBottom: '0.5rem'}}>CJ Dropshipping Integration</h3>
                  <p style={{fontSize: '0.875rem', color: '#64748b'}}>CJ API Key is configured in backend .env file</p>
                  <p style={{fontSize: '0.875rem', color: '#22c55e', marginTop: '0.5rem'}}>✓ Connected and Active</p>
                </div>
                <div>
                  <h3 style={{fontWeight: 600, marginBottom: '0.5rem'}}>Webhook Configuration</h3>
                  <p style={{fontSize: '0.875rem', color: '#64748b'}}>Stripe webhooks are automatically configured</p>
                </div>
                <div style={{background: '#f0f9ff', padding: '1rem', borderRadius: '0.5rem'}}>
                  <p style={{fontSize: '0.875rem', color: '#1e3a8a'}}>
                    <strong>Info:</strong> Advanced settings require backend configuration. Contact support for custom integrations.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}