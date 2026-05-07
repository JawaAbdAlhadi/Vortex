import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Profile.css';

function Profile() {
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const navigate = useNavigate();

  const menuItems = [
    { title: 'منتجاتي المعروضة', icon: '📦' },
    { title: 'الرسائل', icon: '💬' },
    { title: 'تقييماتي', icon: '⭐' },
    { title: 'إعدادات الحساب', icon: '⚙️' },
  ];

  return (
    <div className="min-h-screen p-6 flex flex-col items-center">
      <div className="w-24 h-24 mt-12 mb-4 relative">
        <div className="absolute inset-0 bg-[#5B39A0] rounded-3xl blur-md opacity-50"></div>
        <img src="/vortex-logo.png" alt="Vortex" className="relative w-full h-full object-contain" />
        <div className="absolute top-0 right-0 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center cursor-pointer">
          <span className="text-xs">✏️</span>
        </div>
      </div>

      <h1 className="text-2xl font-bold mb-1">أحمد علي</h1>
      <p className="text-gray-400 text-sm mb-10">ahmad.ali@vortex.com</p>

      <div className="w-full flex flex-col gap-3">
        {menuItems.map((item, index) => (
          <div key={index} className="glass-panel p-4 rounded-2xl flex items-center justify-between cursor-pointer">
            <div className="flex items-center gap-3">
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.title}</span>
            </div>
            <span className="text-gray-500">›</span>
          </div>
        ))}
      </div>

      <div 
        onClick={() => setShowLogoutModal(true)}
        className="w-full glass-panel p-4 rounded-2xl flex items-center justify-between mt-auto mb-8 cursor-pointer text-red-400 border-red-500/30"
      >
        <span className="font-medium">تسجيل الخروج</span>
        <span className="text-xl">🚪</span>
      </div>

      {showLogoutModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-6 z-50">
          <div className="glass-panel w-full max-w-sm rounded-3xl p-6 flex flex-col items-center border border-gray-600 bg-[#1A102E]">
            <h2 className="text-xl font-bold mb-4">تسجيل الخروج</h2>
            <p className="text-center text-gray-300 mb-8">
              هل أنت متأكد أنك تريد الخروج من Vortex؟
            </p>
            <div className="flex w-full gap-4">
              <button 
                onClick={() => setShowLogoutModal(false)}
                className="flex-1 bg-transparent border border-gray-500 py-3 rounded-xl font-bold hover:bg-gray-500/20 transition-all"
              >
                إلغاء
              </button>
              <button 
                onClick={() => navigate('/login')}
                className="flex-1 bg-red-500/20 text-red-400 border border-red-500/50 py-3 rounded-xl font-bold hover:bg-red-500/30 transition-all"
              >
                خروج
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile;