import React, { useState } from 'react';
import axios from 'axios';
import BuyerMarketplace from './BuyerMarketplace';

function SellerDashboard() {
  const [showAddProduct, setShowAddProduct] = useState(false);
  const [productData, setProductData] = useState({
    name: '',
    price: '',
    description: ''
  });

  const userId = localStorage.getItem('user_id');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddProduct = (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      alert("Please select a product image");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('name', productData.name);
    formData.append('price', productData.price);
    formData.append('description', productData.description);
    formData.append('seller_id', userId);
    formData.append('image', selectedFile); 

    axios.post('http://127.0.0.1:8000/api/add-product/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(res => {
        alert("Your product has been sent for review!");
        // إعادة تعيين الحقول
        setProductData({ name: '', price: '', description: '' });
        setSelectedFile(null);
        setShowAddProduct(false);
    })
    .catch(err => {
        console.error(err);
        alert("Failed to add product. Check console for details.");
    })
    .finally(() => {
        setLoading(false);
    });
};

  return (
    <div className="seller-container">
      {/* شريط علوي خاص بالبائع لتمييز اللوحة */}
      <div style={{ 
        background: '#1a1a2e', 
        padding: '15px 30px', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        borderBottom: '2px solid #6c5ce7' 
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#00ff88' }}></div>
            <h3 style={{ color: '#fff', margin: 0 }}>Seller Workspace</h3>
        </div>
        <button 
            className="login-btn" 
            style={{ width: 'auto', padding: '10px 25px', marginBottom: 0 }} 
            onClick={() => setShowAddProduct(!showAddProduct)}
        >
          {showAddProduct ? "← Back To Market" : "Add New Product +"}
        </button>
      </div>

      {showAddProduct ? (
        <div className="login-card" style={{ margin: '40px auto', maxWidth: '500px' }}>
          <h2 style={{ marginBottom: '25px' }}>Product Details</h2>
          <form onSubmit={handleAddProduct}>
            <label style={{ display: 'block', textAlign: 'left', fontSize: '12px', color: '#a29bfe', marginBottom: '5px' }}>Product Name</label>
            <input 
              type="text" 
              placeholder="e.g. Wireless Headphones" 
              className="input-style" 
              value={productData.name}
              onChange={e => setProductData({...productData, name: e.target.value})} 
              required 
            />

            <label style={{ display: 'block', textAlign: 'left', fontSize: '12px', color: '#a29bfe', marginBottom: '5px' }}>Price ($)</label>
            <input 
              type="number" 
              placeholder="0.00" 
              className="input-style" 
              value={productData.price}
              onChange={e => setProductData({...productData, price: e.target.value})} 
              required 
            />

            <label style={{ display: 'block', textAlign: 'left', fontSize: '12px', color: '#a29bfe', marginBottom: '5px' }}>Description</label>
            <textarea 
              placeholder="Describe your product features..." 
              className="input-style" 
              style={{ height: '100px', paddingTop: '10px' }}
              value={productData.description}
              onChange={e => setProductData({...productData, description: e.target.value})} 
              required 
            />

            <label style={{ display: 'block', textAlign: 'left', fontSize: '12px', color: '#a29bfe', marginBottom: '5px' }}>Product Image</label>
            <input 
              type="file" 
              accept="image/*"
              onChange={(e) => setSelectedFile(e.target.files[0])} 
              className="input-style" 
              style={{ padding: '8px' }}
              required
            />

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? "Sending..." : "Submit for Approval"}
            </button>
          </form>
        </div>
      ) : (
        /* عرض السوق للمشتري ليشاهد البائع كيف تظهر المنتجات */
        <BuyerMarketplace />
      )}
    </div>
  );
}

export default SellerDashboard;