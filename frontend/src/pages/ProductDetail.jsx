import React, { useState } from 'react';
import { FiArrowRight, FiShoppingCart, FiPhone, FiMessageCircle, FiGrid, FiStar } from 'react-icons/fi';
import axios from 'axios'; // تأكد من تثبيت axios: npm install axios
import '../css/Home.css';

function ProductDetail({ product, onClose }) {
  const [loading, setLoading] = useState(false);
  // استرجاع بيانات المستخدم المسجل من الـ LocalStorage (الذي تم حفظه عند تسجيل الدخول)
  const userId = localStorage.getItem('user_id'); 

  // 1. وظيفة طلب المحادثة
  const handleChatRequest = async () => {
    if (!userId) return alert("يرجى تسجيل الدخول أولاً");
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/send_chat_request/', {
        sender_id: userId,
        receiver_id: product.seller_id // نحتاج التأكد أن الـ API يرسل seller_id
      });
      alert(response.data.message);
    } catch (error) {
      alert(error.response?.data?.message || "حدث خطأ في إرسال الطلب");
    }
    setLoading(false);
  };

  // 2. وظيفة بدء الشراء
  const handlePurchase = async () => {
    if (!userId) return alert("يرجى تسجيل الدخول أولاً");
    if (!window.confirm("هل أنت متأكد من رغبتك في شراء هذا المنتج وحجز المبلغ؟")) return;

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/initiate_purchase/', {
        buyer_id: userId,
        product_id: product.id
      });
      alert(response.data.message);
    } catch (error) {
      alert(error.response?.data?.message || "فشلت عملية الشراء");
    }
    setLoading(false);
  };

  return (
    <div className="vortex-app-container product-detail-container">
      <div className="detail-image-section">
        <button className="back-button-top" onClick={onClose}>
          <FiArrowRight /> 
        </button>
        <div className="drag-handle"></div>
        <img src={product.image} className="product-detail-img" alt={product.name} />
      </div>

      <div className="detail-info-section">
        <div className="price-container">
          <h1 className="text-2xl font-bold text-white">{product.name}</h1>
          <div className="price-tag-bubble">${product.price}</div>
        </div>

        <div className="seller-card-modern">
          <div className="bg-white/5 p-3 rounded-xl ml-4">
            <FiGrid className="text-blue-400 text-xl" />
          </div>
          <div className="seller-text-info text-right">
            <p className="text-xs text-gray-400 mb-1">البائع المعتمد</p>
            <p className="text-white font-bold">{product.seller}</p>
          </div>
          {/* يمكنك وضع صورة افتراضية للبائع هنا */}
          <div className="w-[50px] h-[50px] bg-blue-500 rounded-2xl flex items-center justify-center text-white font-bold">
             {product.seller?.charAt(0)}
          </div>
        </div>

        <div className="text-right">
          <h3 className="text-lg font-bold text-white mb-2">الوصف</h3>
          <p className="text-gray-400 text-sm leading-relaxed">{product.desc}</p>
        </div>
      </div>

      {/* شريط الأزرار المفعل */}
      <nav className="mobile-actions-bar">
        <button 
          className="main-contact-btn" 
          onClick={handleChatRequest}
          disabled={loading}
        >
          <FiMessageCircle />
          <span>{loading ? "جاري الإرسال..." : "تواصل مباشر الآن"}</span>
        </button>
        
        <button className="action-icon-btn phone">
          <FiPhone />
        </button>

        <button 
          className="action-icon-btn cart" 
          onClick={handlePurchase}
          disabled={loading}
        >
          <FiShoppingCart />
        </button>
      </nav>
    </div>
  );
}

export default ProductDetail;