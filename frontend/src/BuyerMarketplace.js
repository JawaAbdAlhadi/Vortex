import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ProductDetails from './pages/ProductDetails';
import Profile from './pages/Profile';
import Chat from './pages/Chat';
import "./css/BuyerMarketplace.css";

function BuyerMarketplace() {
  return (
    <div className="buyer-content">
      <Routes>
  {/* المسار الرئيسي للمتجر */}
  <Route path="/" element={<Home />} /> 
  
  {/* صفحة المنتج - ستصبح تلقائياً /dashboard/product/:id */}
  <Route path="product/:id" element={<ProductDetails />} />
  
  {/* صفحة البروفايل - ستصبح /dashboard/profile */}
  <Route path="profile" element={<Profile />} />
  
  {/* صفحة المحادثة */}
  <Route path="chat/:userId" element={<Chat />} />
</Routes>
    </div>
  );
}

export default BuyerMarketplace;