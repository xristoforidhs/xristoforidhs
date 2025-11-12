import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API } from "@/App";
import { ArrowLeft, Upload, X, Image as ImageIcon } from "lucide-react";
import Navbar from "@/components/Navbar";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function ImageUploadPage() {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [imageUrl, setImageUrl] = useState("");
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API}/products?limit=200`);
      setProducts(response.data);
    } catch (error) {
      console.error("Failed to fetch products", error);
      toast.error("Failed to load products");
    }
  };

  const handleAddImage = async (productId) => {
    if (!imageUrl) {
      toast.error("Please enter an image URL");
      return;
    }

    setUploading(true);
    try {
      const product = products.find(p => p.id === productId);
      const updatedImages = [...(product.images || []), imageUrl];
      
      await axios.put(`${API}/products/${productId}`, {
        ...product,
        images: updatedImages
      });

      toast.success("Image added successfully!");
      setImageUrl("");
      fetchProducts();
    } catch (error) {
      console.error("Failed to add image", error);
      toast.error("Failed to add image");
    } finally {
      setUploading(false);
    }
  };

  const handleRemoveImage = async (productId, imageIndex) => {
    try {
      const product = products.find(p => p.id === productId);
      const updatedImages = product.images.filter((_, idx) => idx !== imageIndex);
      
      await axios.put(`${API}/products/${productId}`, {
        ...product,
        images: updatedImages
      });

      toast.success("Image removed successfully!");
      fetchProducts();
    } catch (error) {
      console.error("Failed to remove image", error);
      toast.error("Failed to remove image");
    }
  };

  const handleSetMainImage = async (productId, newImageUrl) => {
    try {
      const product = products.find(p => p.id === productId);
      
      await axios.put(`${API}/products/${productId}`, {
        ...product,
        image_url: newImageUrl
      });

      toast.success("Main image updated!");
      fetchProducts();
    } catch (error) {
      console.error("Failed to update main image", error);
      toast.error("Failed to update main image");
    }
  };

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            <Package size={28} />
            Image Upload Tool
          </Link>
        </div>
      </nav>

      <div style={{maxWidth: '1400px', margin: '3rem auto', padding: '2rem'}}>
        <Link to="/admin" className="navbar-link" style={{marginBottom: '2rem', display: 'inline-flex'}}>
          <ArrowLeft size={20} /> Back to Admin
        </Link>

        <div style={{display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '2rem', marginBottom: '2rem'}}>
          <ImageIcon size={32} />
          <h1 className="section-title" style={{marginBottom: 0}}>Product Image Management</h1>
        </div>

        <Card style={{marginBottom: '3rem'}}>
          <CardHeader>
            <CardTitle>How to Use</CardTitle>
            <CardDescription>
              Upload and manage product images. You can add multiple images per product and set the main display image.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ol style={{paddingLeft: '1.5rem', lineHeight: 2}}>
              <li>Select a product from the list below</li>
              <li>Add image URLs to create a gallery for the product</li>
              <li>Click on any image to set it as the main product image</li>
              <li>Remove unwanted images using the X button</li>
            </ol>
          </CardContent>
        </Card>

        <div style={{display: 'grid', gap: '2rem'}}>
          {products.map(product => (
            <Card key={product.id}>
              <CardHeader>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                  <div>
                    <CardTitle>{product.name}</CardTitle>
                    <CardDescription>Category: {product.category}</CardDescription>
                  </div>
                  <div style={{textAlign: 'right'}}>
                    <p style={{fontSize: '0.875rem', color: '#64748b'}}>Main Image</p>
                    <img 
                      src={product.image_url} 
                      alt={product.name}
                      style={{
                        width: '80px',
                        height: '80px',
                        objectFit: 'cover',
                        borderRadius: '8px',
                        border: '3px solid #2563eb'
                      }}
                    />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {/* Current Images Gallery */}
                {product.images && product.images.length > 0 && (
                  <div style={{marginBottom: '1.5rem'}}>
                    <Label>Image Gallery ({product.images.length} images)</Label>
                    <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', gap: '1rem', marginTop: '1rem'}}>
                      {product.images.map((img, idx) => (
                        <div key={idx} style={{position: 'relative', borderRadius: '8px', overflow: 'hidden', border: '2px solid #e2e8f0'}}>
                          <img 
                            src={img} 
                            alt={`${product.name} ${idx + 1}`}
                            onClick={() => handleSetMainImage(product.id, img)}
                            style={{
                              width: '100%',
                              height: '120px',
                              objectFit: 'cover',
                              cursor: 'pointer'
                            }}
                            title="Click to set as main image"
                          />
                          <button
                            onClick={() => handleRemoveImage(product.id, idx)}
                            style={{
                              position: 'absolute',
                              top: '0.25rem',
                              right: '0.25rem',
                              background: 'rgba(239, 68, 68, 0.9)',
                              color: 'white',
                              border: 'none',
                              borderRadius: '4px',
                              padding: '0.25rem',
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center'
                            }}
                          >
                            <X size={16} />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Add New Image */}
                <div>
                  <Label>Add New Image</Label>
                  <div style={{display: 'flex', gap: '0.5rem', marginTop: '0.5rem'}}>
                    <Input
                      type="url"
                      placeholder="Enter image URL"
                      value={selectedProduct === product.id ? imageUrl : ""}
                      onChange={(e) => {
                        setSelectedProduct(product.id);
                        setImageUrl(e.target.value);
                      }}
                    />
                    <Button
                      onClick={() => handleAddImage(product.id)}
                      disabled={uploading || selectedProduct !== product.id || !imageUrl}
                    >
                      <Upload size={18} /> Add
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
