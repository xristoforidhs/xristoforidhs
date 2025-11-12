import { useEffect, useState, useContext } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API, AuthContext } from "@/App";
import { Package, Plus, Edit, Trash2, ArrowLeft } from "lucide-react";
import { toast } from "sonner";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function AdminDashboard() {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [editingProduct, setEditingProduct] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const { user } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    price: "",
    image_url: "",
    category: "",
    stock: "",
    featured: false
  });

  useEffect(() => {
    fetchProducts();
    fetchOrders();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error("Failed to fetch products", error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API}/orders`);
      setOrders(response.data);
    } catch (error) {
      console.error("Failed to fetch orders", error);
    }
  };

  const handleOpenDialog = (product = null) => {
    if (product) {
      setEditingProduct(product);
      setFormData({
        name: product.name,
        description: product.description,
        price: product.price.toString(),
        image_url: product.image_url,
        category: product.category,
        stock: product.stock.toString(),
        featured: product.featured
      });
    } else {
      setEditingProduct(null);
      setFormData({
        name: "",
        description: "",
        price: "",
        image_url: "",
        category: "",
        stock: "",
        featured: false
      });
    }
    setIsDialogOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock)
      };

      if (editingProduct) {
        await axios.put(`${API}/products/${editingProduct.id}`, payload);
        toast.success("Το προϊόν ενημερώθηκε");
      } else {
        await axios.post(`${API}/products`, payload);
        toast.success("Το προϊόν δημιουργήθηκε");
      }
      setIsDialogOpen(false);
      fetchProducts();
    } catch (error) {
      console.error("Failed to save product", error);
      toast.error("Αποτυχία αποθήκευσης");
    }
  };

  const handleDelete = async (productId) => {
    if (!window.confirm("Είστε σίγουροι;")) return;
    
    try {
      await axios.delete(`${API}/products/${productId}`);
      toast.success("Το προϊόν διαγράφηκε");
      fetchProducts();
    } catch (error) {
      console.error("Failed to delete product", error);
      toast.error("Αποτυχία διαγραφής");
    }
  };

  const updateOrderStatus = async (orderId, status) => {
    try {
      await axios.put(`${API}/orders/${orderId}/status?status=${status}`);
      toast.success("Η κατάσταση ενημερώθηκε");
      fetchOrders();
    } catch (error) {
      console.error("Failed to update order status", error);
      toast.error("Αποτυχία ενημέρωσης");
    }
  };

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand" data-testid="navbar-brand">
            <Package size={28} />
            TechGadgets Admin
          </Link>
        </div>
      </nav>

      <div style={{maxWidth: '1400px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}} data-testid="back-to-shop">
          <ArrowLeft size={20} /> Επιστροφή στο Κατάστημα
        </Link>

        {/* Products Section */}
        <div style={{marginBottom: '4rem'}}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem'}}>
            <h1 className="section-title" style={{marginBottom: 0}}>Διαχείριση Προϊόντων</h1>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button onClick={() => handleOpenDialog()} data-testid="add-product-btn">
                  <Plus size={20} /> Προσθήκη Προϊόντος
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>{editingProduct ? 'Επεξεργασία Προϊόντος' : 'Νέο Προϊόν'}</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Label htmlFor="name">Όνομα</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      required
                      data-testid="product-name-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="description">Περιγραφή</Label>
                    <Textarea
                      id="description"
                      value={formData.description}
                      onChange={(e) => setFormData({...formData, description: e.target.value})}
                      required
                      rows={4}
                      data-testid="product-description-input"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="price">Τιμή ($)</Label>
                      <Input
                        id="price"
                        type="number"
                        step="0.01"
                        value={formData.price}
                        onChange={(e) => setFormData({...formData, price: e.target.value})}
                        required
                        data-testid="product-price-input"
                      />
                    </div>
                    <div>
                      <Label htmlFor="stock">Απόθεμα</Label>
                      <Input
                        id="stock"
                        type="number"
                        value={formData.stock}
                        onChange={(e) => setFormData({...formData, stock: e.target.value})}
                        required
                        data-testid="product-stock-input"
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="category">Κατηγορία</Label>
                    <Input
                      id="category"
                      value={formData.category}
                      onChange={(e) => setFormData({...formData, category: e.target.value})}
                      required
                      data-testid="product-category-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="image_url">URL Εικόνας</Label>
                    <Input
                      id="image_url"
                      value={formData.image_url}
                      onChange={(e) => setFormData({...formData, image_url: e.target.value})}
                      required
                      data-testid="product-image-input"
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="featured"
                      checked={formData.featured}
                      onChange={(e) => setFormData({...formData, featured: e.target.checked})}
                      data-testid="product-featured-checkbox"
                    />
                    <Label htmlFor="featured">Προβεβλημένο</Label>
                  </div>
                  <Button type="submit" className="w-full" data-testid="save-product-btn">
                    Αποθήκευση
                  </Button>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          <div className="products-grid">
            {products.map(product => (
              <div key={product.id} className="product-card" data-testid={`admin-product-${product.id}`}>
                <img src={product.image_url} alt={product.name} className="product-image" />
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-description">{product.description.substring(0, 60)}...</p>
                  <div className="product-price">${product.price}</div>
                  <p style={{fontSize: '0.875rem', color: '#64748b', marginBottom: '1rem'}}>Απόθεμα: {product.stock}</p>
                  <div style={{display: 'flex', gap: '0.5rem'}}>
                    <button 
                      onClick={() => handleOpenDialog(product)}
                      className="btn btn-secondary"
                      style={{flex: 1}}
                      data-testid={`edit-product-${product.id}`}
                    >
                      <Edit size={16} />
                    </button>
                    <button 
                      onClick={() => handleDelete(product.id)}
                      className="btn btn-danger"
                      style={{flex: 1}}
                      data-testid={`delete-product-${product.id}`}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Orders Section */}
        <div>
          <h1 className="section-title">Διαχείριση Παραγγελιών</h1>
          <div>
            {orders.map(order => (
              <div 
                key={order.id}
                style={{
                  background: 'white',
                  borderRadius: '16px',
                  padding: '2rem',
                  marginBottom: '1rem',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
                }}
                data-testid={`admin-order-${order.id}`}
              >
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem'}}>
                  <div>
                    <h3 style={{fontSize: '1.25rem', fontWeight: 600}}>#{order.id.substring(0, 8)}</h3>
                    <p style={{color: '#64748b', fontSize: '0.875rem'}}>{order.user_name} ({order.user_email})</p>
                    <p style={{color: '#64748b', fontSize: '0.875rem'}}>
                      {new Date(order.created_at).toLocaleDateString('el-GR')}
                    </p>
                  </div>
                  <div>
                    <p style={{fontSize: '1.5rem', fontWeight: 700, color: '#2563eb'}}>${order.total_amount.toFixed(2)}</p>
                  </div>
                </div>

                <div style={{marginBottom: '1rem'}}>
                  {order.items.map((item, idx) => (
                    <p key={idx} style={{fontSize: '0.875rem', color: '#64748b'}}>
                      {item.name} × {item.quantity}
                    </p>
                  ))}
                </div>

                <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
                  <label style={{fontWeight: 600, fontSize: '0.875rem'}}>Κατάσταση:</label>
                  <select
                    value={order.status}
                    onChange={(e) => updateOrderStatus(order.id, e.target.value)}
                    style={{
                      padding: '0.5rem 1rem',
                      borderRadius: '8px',
                      border: '2px solid #e2e8f0',
                      fontSize: '0.875rem',
                      fontWeight: 600
                    }}
                    data-testid={`order-status-select-${order.id}`}
                  >
                    <option value="pending">Εκκρεμής</option>
                    <option value="processing">Σε Επεξεργασία</option>
                    <option value="completed">Ολοκληρωμένη</option>
                    <option value="cancelled">Ακυρωμένη</option>
                  </select>
                  <span style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '8px',
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    background: order.payment_status === 'paid' ? '#22c55e20' : '#f59e0b20',
                    color: order.payment_status === 'paid' ? '#22c55e' : '#f59e0b'
                  }}>
                    {order.payment_status === 'paid' ? 'Πληρωμένη' : 'Εκκρεμής'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}