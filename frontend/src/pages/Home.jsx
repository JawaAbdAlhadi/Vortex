import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiSearch, FiBell, FiUser, FiGrid } from 'react-icons/fi';
import '../css/Home.css';
import ProductDetail from './ProductDetail';

const categories = ['الكل', 'ملابس', 'إكسسوارات', 'أجهزة ذكية'];

function Home() {
  const [activeCategory, setActiveCategory] = useState('الكل');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    // جلب المنتجات الحقيقية من الـ Backend
    const fetchProducts = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/get_approved_products/');
        setProducts(res.data);
      } catch (err) {
        console.error("خطأ في جلب المنتجات:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (selectedProduct) {
    return <ProductDetail product={selectedProduct} onClose={() => setSelectedProduct(null)} />;
  }

  return (
    <div className="vortex-app-container">
      {/* الشريط العلوي */}
      <header className="vortex-header">
        <div className="notification-wrapper">
          <FiBell className="vortex-icon" />
          <span className="vortex-badge">3</span>
        </div>
        <h1 className="vortex-page-title">البحث عن منتج</h1>
        <div className="placeholder-icon"></div>
      </header>

      <main className="vortex-main-content">
        {/* شريط البحث */}
        <div className="vortex-search-wrapper">
          <FiSearch className="vortex-search-icon" />
          <input
            type="text"
            placeholder="ابحث عن (كنزة سوداء...)"
            className="vortex-search-input"
          />
        </div>

        {/* أزرار الأقسام */}
        <div className="vortex-categories-container hide-scrollbar">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`vortex-category-btn ${activeCategory === cat ? 'active' : ''}`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* شبكة المنتجات الحقيقية */}
        {loading ? (
          <div className="vortex-loading text-white text-center mt-10">جاري تحميل المنتجات...</div>
        ) : (
          <div className="vortex-products-grid">
            {products.map(product => (
              <div 
                key={product.id} 
                className="vortex-product-card"
                onClick={() => setSelectedProduct(product)}
              >
                <div className="product-image-wrapper">
                  {/* استخدام رابط الصورة القادم من الـ Backend */}
                  <img src={product.image} alt={product.name} />
                </div>
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <div className="product-meta">
                    <span className="product-price">${product.price}</span>
                    <div className="product-rating">
                      <span className="star-icon">★</span>
                      <span>4.5</span> {/* يمكن تحديثها لاحقاً ببيانات حقيقية */}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* الشريط السفلي */}
      <nav className="vortex-bottom-nav">
        <div className="nav-item">
          <FiUser className="nav-icon" />
          <span>حسابي</span>
        </div>
        <div className="nav-item active">
          <FiSearch className="nav-icon" />
          <span>البحث</span>
        </div>
        <div className="nav-item">
          <FiGrid className="nav-icon" />
          <span>الرئيسية</span>
        </div>
      </nav>
    </div>
  );
}

export default Home;