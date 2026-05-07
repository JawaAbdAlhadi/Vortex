import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import '../css/ProductDetails.css';

function ProductDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);

  const product = {
    id: id,
    name: 'سماعات عازلة للضوضاء',
    price: 85,
    seller: 'الصوت النقي',
    desc: 'سماعات رأس لاسلكية توفر تجربة صوتية محيطية مع خاصية إلغاء الضجيج النشط.',
    image: '/path-to-headphones.jpg'
  };

  const handlePurchase = () => {
    axios.post('http://127.0.0.1:8000/api/initiate-purchase/', {
      buyer_id: 1, 
      product_id: product.id
    }).then(() => {
      setShowModal(false);
      navigate('/profile'); 
    }).catch(err => console.error(err));
  };

  return (
    <div className="min-h-screen relative flex flex-col bg-[#120A21]">
      <div className="h-80 bg-[#E8D455] relative flex items-center justify-center rounded-b-[40px]">
        <img src={product.image} className="h-64 object-contain" alt={product.name} />
        <div className="absolute bottom-4 bg-black/40 px-4 py-1 rounded-full text-xs flex items-center backdrop-blur-md">
          <span className="mr-2">اسحب لرؤية المزيد</span>
          <div className="flex gap-1">
            <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
            <div className="w-1.5 h-1.5 bg-white/50 rounded-full"></div>
          </div>
        </div>
      </div>

      <div className="p-6 flex-1">
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-2xl font-bold">{product.name}</h1>
          <span className="text-3xl font-bold text-blue-400">${product.price}</span>
        </div>

        <div className="glass-panel p-4 rounded-2xl flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gray-500 overflow-hidden">
              <img src="/avatar.jpg" alt="Seller" className="w-full h-full object-cover" />
            </div>
            <span className="font-medium text-gray-200">البائع: {product.seller}</span>
          </div>
          <span className="text-2xl text-blue-400">🏪</span>
        </div>

        <div className="flex text-yellow-400 mb-6 text-xl">
          ★★★★★
        </div>

        <div>
          <h3 className="text-xl font-bold mb-2">الوصف</h3>
          <p className="text-gray-300 leading-relaxed text-sm">
            {product.desc}
          </p>
        </div>
      </div>

      <div className="p-6">
        <button 
          onClick={() => setShowModal(true)}
          className="w-full bg-[#5B39A0] py-4 rounded-2xl font-bold text-lg shadow-lg"
        >
          شراء الآن
        </button>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-6 z-50">
          <div className="glass-panel w-full max-w-sm rounded-3xl p-6 flex flex-col items-center border border-gray-600">
            <h2 className="text-xl font-bold mb-4">تأكيد الشراء</h2>
            <p className="text-center text-gray-300 mb-8">
              هل تود إرسال طلب شراء رسمي لهذا المنتج؟
              <br/>سيتم إشعار البائع فوراً.
            </p>
            <button 
              onClick={handlePurchase}
              className="w-full bg-transparent border border-blue-500 py-3 rounded-xl mb-3 font-bold hover:bg-blue-500/20 transition-all"
            >
              إرسال الطلب
            </button>
            <button 
              onClick={() => setShowModal(false)}
              className="w-full bg-red-500/20 text-red-400 py-3 rounded-xl font-bold hover:bg-red-500/30 transition-all"
            >
              إلغاء
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProductDetails;