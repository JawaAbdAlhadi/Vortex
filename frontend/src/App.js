import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import BuyerMarketplace from './BuyerMarketplace';
import SellerDashboard from './SellerDashboard';
import StationDashboard from './pages/stationDashboard';
import vortexBackground from './Vortex.jpg'; 
import "./App.css";

const MailIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: 0.7 }}>
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
    <polyline points="22,6 12,13 2,6"></polyline>
  </svg>
);

const LockIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: 0.7 }}>
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
  </svg>
);

const EyeIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: 0.7 }}>
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
    <circle cx="12" cy="12" r="3"></circle>
  </svg>
);

const EyeOffIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: 0.7 }}>
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
    <line x1="1" y1="1" x2="23" y2="23"></line>
  </svg>
);

function App() {
  return (
    <div className="vortex-bg">
      <Routes>
        {/* الصفحة الرئيسية هي تسجيل الدخول */}
        <Route path="/" element={<LoginPage />} />
        
        {/* مسار الداشبورد مع النجمة ضروري جداً */}
        <Route path="/dashboard/*" element={<MainSwitch />} />

        {/* حل احتياطي: إذا حاول المستخدم دخول /product مباشرة نوجهه للداشبورد */}
        <Route path="/product/:id" element={<Navigate to="/dashboard/product/:id" replace />} />

        <Route path="/station-dashboard" element={<StationDashboard />} />
      </Routes>
    </div>
  );
}

function MainSwitch() {
  const userType = localStorage.getItem('user_type');
  if (!userType) return <LoginPage />;
  if (userType === 'admin') return <AdminDashboard />;
  if (userType === 'seller') return <SellerDashboard />;
  return <BuyerMarketplace />;
}

function LoginPage() {
  const [view, setView] = useState('login'); 
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleAuth = async (e) => {
    if (e) e.preventDefault();
    try {
      if (view === 'login') {
        const res = await axios.post('http://127.0.0.1:8000/api/login/', { email, password });
        if (res.data.message === 'success') {
          localStorage.setItem('user_type', res.data.user_type);
          localStorage.setItem('full_name', res.data.full_name);
          localStorage.setItem('user_id', res.data.user_id);
          navigate('/dashboard');
        }
      } else if (view === 'signup') {
        await axios.post('http://127.0.0.1:8000/api/register/', { full_name: fullName, email, password });
        alert("Account Created! You can login now.");
        setView('login');
      } else if (view === 'forgot') {
        await axios.post('http://127.0.0.1:8000/api/forgot-password/', { email });
        alert("If this email exists, a reset link has been sent.");
        setView('login');
      }
    } catch (err) { 
      alert("Action Failed: " + (err.response?.data?.message || "Check Server")); 
    }
  };

 const isMobile = window.innerWidth <= 768;

const styles = {
    container: {
      minHeight: isMobile ? '100dvh' : '100vh', 
      width: '100vw',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundImage: `url(${vortexBackground})`, 
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundAttachment: 'fixed',
      fontFamily: 'sans-serif',
      color: '#fff',
      position: 'relative',
      top: 0, left: 0,
      overflow: 'hidden' 
    },
    overlay: {
      position: 'absolute',
      top: 0, left: 0, right: 0, bottom: 0,
      background: isMobile 
        ? 'transparent' 
        : 'radial-gradient(circle, transparent 20%, rgba(30,0,60,0.8) 100%)',
      zIndex: 1
    },
    content: {
      position: 'relative',
      zIndex: 2,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      width: isMobile ? '85%' : '90%',
      maxWidth: '380px'
    },
    logoContainer: {
      textAlign: 'center',
      marginBottom: '30px'
    },
    title: {
      fontSize: '28px',
      fontWeight: '600',
      letterSpacing: '1px'
    },
    card: {
      width: '100%',
      background: isMobile ? 'rgba(255, 255, 255, 0.07)' : 'rgba(255, 255, 255, 0.1)',
      backdropFilter: isMobile ? 'blur(20px)' : 'blur(15px)',
      WebkitBackdropFilter: isMobile ? 'blur(20px)' : 'blur(15px)',
      borderRadius: '25px',
      padding: isMobile ? '35px 20px' : '40px 30px',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
    },
    inputGroup: {
      display: 'flex',
      alignItems: 'center',
      background: 'rgba(255, 255, 255, 0.05)',
      borderRadius: '15px',
      marginBottom: '18px',
      padding: '12px 18px',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      position: 'relative'
    },
    input: {
      background: 'transparent',
      border: 'none',
      color: '#fff',
      outline: 'none',
      width: '100%',
      fontSize: '15px',
      marginLeft: '5px'
    },
    eyeButton: {
      background: 'none',
      border: 'none',
      color: '#fff',
      cursor: 'pointer',
      padding: 0,
      display: 'flex',
      alignItems: 'center'
    },
    loginBtn: {
      width: '100%',
      background: 'linear-gradient(45deg, #9c27b0, #673ab7)', 
      color: 'white',
      border: 'none',
      padding: '14px',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      marginTop: '10px',
      boxShadow: '0 4px 15px rgba(156, 39, 176, 0.3)',
    },
    footerLinks: {
      marginTop: '20px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '10px',
      fontSize: '14px',
      opacity: 0.8
    },
    link: {
      cursor: 'pointer',
      textDecoration: 'none',
      color: '#fff'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.overlay}></div>
      <div style={styles.content}>
        <div style={styles.logoContainer}>
             <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
             </svg>
          <h1 style={styles.title}>Vortex Market</h1>
        </div>

        <div style={styles.card} className="login-card">
          <h2 style={{fontSize: '18px', textAlign: 'center', marginBottom: '20px', opacity: 0.9}}>
            {view === 'login' && 'Welcome Back'}
            {view === 'signup' && 'Join Vortex'}
            {view === 'forgot' && 'Reset Password'}
          </h2>

          <form onSubmit={handleAuth}>
            {view === 'signup' && (
              <div style={styles.inputGroup}>
                <input 
                  style={styles.input} 
                  type="text" 
                  placeholder="Full Name" 
                  onChange={e => setFullName(e.target.value)} 
                  required 
                />
              </div>
            )}

            <div style={styles.inputGroup}>
              <MailIcon />
              <input 
                style={styles.input} 
                type="email" 
                placeholder="Email" 
                value={email} 
                onChange={e => setEmail(e.target.value)} 
                required 
                autoComplete="email"
              />
            </div>

            {view !== 'forgot' && (
              <div style={styles.inputGroup}>
                <LockIcon />
                <input 
                  style={styles.input} 
                  type={showPassword ? 'text' : 'password'} 
                  placeholder="Password" 
                  value={password} 
                  onChange={e => setPassword(e.target.value)} 
                  required 
                  autoComplete="current-password"
                />
                <button 
                  type="button" 
                  onClick={() => setShowPassword(!showPassword)} 
                  style={styles.eyeButton}
                >
                  {showPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </div>
            )}

            <button type="submit" style={styles.loginBtn}>
              {view === 'login' ? 'LOGIN' : view === 'signup' ? 'SIGN UP' : 'SEND RESET LINK'}
            </button>
          </form>

          <div style={styles.footerLinks}>
            {view === 'login' && (
              <>
                <span onClick={() => setView('forgot')} style={styles.link}>Forgot Password?</span>
                <span onClick={() => setView('signup')} style={styles.link}>Create New Account</span>
              </>
            )}
            {(view === 'signup' || view === 'forgot') && (
              <span onClick={() => setView('login')} style={styles.link}>Back to Login</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function AdminDashboard() {
  const navigate = useNavigate();
  const userId = localStorage.getItem('user_id');
  const userType = localStorage.getItem('user_type');

  const [activeTab, setActiveTab] = useState('products'); 
  const [sellers, setSellers] = useState([]);
  const [users, setUsers] = useState([]);
  const [qrRequests, setQrRequests] = useState([]);
  const [pendingProds, setPendingProds] = useState([]);
  const [finances, setFinances] = useState({ total_held: "0 $", pending_payouts: "0 $" });
  const [chats, setChats] = useState([]); 
  const [activeChat, setActiveChat] = useState(null); 
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [productFilter, setProductFilter] = useState('all'); 

  // --- 1. التحقق من الصلاحيات ---
  useEffect(() => {
    if (userType !== 'admin') navigate('/');
  }, [userType, navigate]);

  // --- 2. دوال جلب البيانات من الباك إند (محدثة لتطابق الـ URLs الجديدة) ---
  const fetchSellers = () => axios.get('http://127.0.0.1:8000/api/pending-sellers/').then(res => setSellers(res.data)).catch(err => console.error(err));
  const fetchUsers = () => axios.get('http://127.0.0.1:8000/api/users-list/').then(res => setUsers(res.data)).catch(err => console.error(err));
  const fetchQrRequests = () => axios.get('http://127.0.0.1:8000/api/qr-requests/').then(res => setQrRequests(res.data)).catch(err => console.error(err));
  const fetchFinances = () => axios.get('http://127.0.0.1:8000/api/admin/finances/').then(res => setFinances(res.data)).catch(err => console.error(err));
  const fetchAllProducts = () => axios.get('http://127.0.0.1:8000/api/all-products/').then(res => setPendingProds(res.data)).catch(err => console.error(err));
  
  const fetchMyChats = useCallback(async () => {
    if (!userId) return;
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/my-active-chats/${userId}/`);
      setChats(res.data);
    } catch (err) { console.error(err); }
  }, [userId]);

  // --- 3. نظام التنبيهات ---
  useEffect(() => {
    if ('Notification' in window && Notification.permission !== 'granted') {
      Notification.requestPermission();
    }
  }, []);

  const checkNewProducts = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/pending-products/');
      const currentPending = pendingProds.filter(p => p.status === 'pending');
      if (res.data.length > currentPending.length) {
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification("VORTEX Admin", { body: "هناك طلبات منتجات جديدة بانتظار موافقتك!" });
          }
          fetchAllProducts(); // تحديث القائمة
      }
    } catch (err) { console.error(err); }
  };

  useEffect(() => {
    const interval = setInterval(checkNewProducts, 60000);
    return () => clearInterval(interval);
  }, [pendingProds]);

  // --- 4. نظام المحادثات ---
  const fetchMessages = useCallback(async () => {
    if (!activeChat || !userId) return;
    try {
        const res = await axios.get(`http://127.0.0.1:8000/api/chat-history/${userId}/${activeChat.id}/`);
        setMessages(res.data);
    } catch (err) { console.error("Failed to load history:", err); }
  }, [userId, activeChat]);

  useEffect(() => {
    if (activeTab === 'sellers') fetchSellers();
    if (activeTab === 'users') fetchUsers();
    if (activeTab === 'qr') fetchQrRequests();
    if (activeTab === 'products') fetchAllProducts();
    if (activeTab === 'messages') fetchMyChats();
    fetchFinances();
  }, [activeTab, fetchMyChats]);

  useEffect(() => {
    let interval;
    if (activeTab === 'messages' && activeChat) {
      fetchMessages();
      interval = setInterval(fetchMessages, 3000);
    }
    return () => clearInterval(interval);
  }, [activeTab, activeChat, fetchMessages]);

  // --- 5. دوال العمليات (Actions) ---
  const sendMessage = async () => {
    if (!newMessage.trim() || !activeChat) return;
    try {
      await axios.post('http://127.0.0.1:8000/api/send-message/', {
        sender_id: userId, receiver_id: activeChat.id, message_text: newMessage
      });
      setNewMessage("");
      fetchMessages();
    } catch (err) { console.error(err); }
  };

  const startChatWithUser = (user) => {
    const targetId = user.id; // تحديث للباك إند الجديد
    const targetName = user.name;
    const exists = chats.some(c => String(c.id) === String(targetId));
    if (!exists) setChats(prev => [{ id: targetId, full_name: targetName }, ...prev]);
    setActiveChat({ id: targetId, full_name: targetName });
    setActiveTab('messages');
  };

  const handleUpdateBalance = async (id, current) => {
    const val = prompt("Enter new balance:", current);
    if (val) {
      await axios.post('http://127.0.0.1:8000/api/update-balance/', { user_id: id, balance: parseFloat(val) });
      fetchUsers();
    }
  };

  const handleRoleChange = async (id) => {
    const role = prompt("Enter new role (buyer, seller, admin):");
    if (role) {
      await axios.post('http://127.0.0.1:8000/api/update-role/', { user_id: id, role: role });
      fetchUsers();
    }
  };

  const handleProductAction = async (id, status) => {
    try {
        await axios.post('http://127.0.0.1:8000/api/update-product-status/', { product_id: id, status: status });
        fetchAllProducts(); 
    } catch (err) { console.error("Error updating product:", err); }
  };

  const handleSellerAction = async (id, status) => {
    await axios.post('http://127.0.0.1:8000/api/update-seller/', { request_id: id, status: status });
    fetchSellers(); fetchUsers();
  };

  const handleReleaseFunds = async (transaction) => {
    if (window.confirm(`Release ${transaction.amount}$ to seller?`)) {
      try {
        await axios.post('http://127.0.0.1:8000/api/release-funds/', {
          transaction_id: transaction.id, 
          amount: parseFloat(transaction.amount)
        });
        alert("Funds released successfully!");
        fetchQrRequests(); fetchFinances();  
      } catch (err) { alert("Error releasing funds."); }
    }
  };

  // --- ستايلات الثيم الداكن (Dark Theme) المطابق للصورة ---
  const colors = {
    bgMain: '#0f0f1b', // كحلي غامق جداً
    bgSidebar: '#151528', // كحلي أفتح للقائمة
    bgCard: '#1a1a32', // خلفية الجداول
    primary: '#6b4ce6', // البنفسجي الفخم
    textLight: '#e2e8f0',
    textDim: '#94a3b8',
    border: '#2d2d44',
    danger: '#ef4444',
    success: '#10b981'
  };

  const tableHeaderStyle = { padding: '15px', textAlign: 'left', fontWeight: 'bold' };
  const tableCellStyle = { padding: '15px', borderBottom: `1px solid ${colors.border}` };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: colors.bgMain, color: colors.textLight, fontFamily: 'sans-serif' }}>
      
      {/* ---------------- Sidebar ---------------- */}
      <div style={{ width: '250px', background: colors.bgSidebar, borderRight: `1px solid ${colors.border}`, display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ padding: '25px', margin: 0, color: '#a29bfe', fontSize: '22px', borderBottom: `1px solid ${colors.border}` }}>VORTEX Admin</h2>
        
        <ul style={{ listStyle: 'none', padding: '15px', margin: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {[
            { id: 'statistics', label: '📊 Overview' },
            { id: 'users', label: '👥 Users & Roles' },
            { id: 'sellers', label: '🏪 Store Requests' },
            { id: 'products', label: '📦 Product Approval' },
            { id: 'messages', label: '💬 Messages' },
            { id: 'qr', label: '🛡️ QR Transactions' }
          ].map(tab => (
            <li key={tab.id} onClick={() => setActiveTab(tab.id)}
                style={{
                  padding: '12px 15px', borderRadius: '8px', cursor: 'pointer', transition: '0.2s',
                  background: activeTab === tab.id ? colors.primary : 'transparent',
                  color: activeTab === tab.id ? '#fff' : colors.textDim,
                  fontWeight: activeTab === tab.id ? 'bold' : 'normal'
                }}>
              {tab.label}
            </li>
          ))}
          
          <li onClick={() => navigate('/station-dashboard')}
              style={{ marginTop: '20px', padding: '12px 15px', borderRadius: '8px', background: 'rgba(16, 185, 129, 0.1)', color: colors.success, cursor: 'pointer', fontWeight: 'bold' }}>
            🚚 Logistics Dashboard
          </li>
        </ul>
        
        <div onClick={() => { localStorage.clear(); navigate('/'); }}
             style={{ marginTop: 'auto', padding: '20px', color: colors.danger, cursor: 'pointer', borderTop: `1px solid ${colors.border}`, fontWeight: 'bold' }}>
          Logout
        </div>
      </div>

      {/* ---------------- Main Content ---------------- */}
      <div style={{ flex: 1, padding: '30px', overflowY: 'auto' }}>
        
        {/* --- Product Approval Tab (كما في الصورة تماماً) --- */}
        {activeTab === 'products' && (
          <div>
            <div style={{ display: 'flex', gap: '15px', marginBottom: '25px' }}>
              <button onClick={() => setProductFilter('all')}
                      style={{ padding: '10px 20px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: 'bold',
                               background: productFilter === 'all' ? colors.primary : 'transparent', 
                               color: productFilter === 'all' ? '#fff' : colors.textDim,
                               border: productFilter === 'all' ? 'none' : `1px solid ${colors.border}` }}>
                📦 All Products ({pendingProds.length})
              </button>
              <button onClick={() => setProductFilter('pending')}
                      style={{ padding: '10px 20px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: 'bold',
                               background: productFilter === 'pending' ? '#f59e0b' : 'transparent', 
                               color: productFilter === 'pending' ? '#fff' : colors.textDim,
                               border: productFilter === 'pending' ? 'none' : `1px solid ${colors.border}` }}>
                ⏳ Pending Approval ({pendingProds.filter(p => p.status === 'pending').length})
              </button>
            </div>

            <div style={{ background: colors.bgCard, borderRadius: '12px', overflow: 'hidden', border: `1px solid ${colors.border}` }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead style={{ background: colors.primary }}>
                  <tr>
                    <th style={tableHeaderStyle}>Image</th>
                    <th style={tableHeaderStyle}>Product</th>
                    <th style={tableHeaderStyle}>Seller</th>
                    <th style={tableHeaderStyle}>Price</th>
                    <th style={tableHeaderStyle}>Status</th>
                    <th style={tableHeaderStyle}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {pendingProds.filter(p => productFilter === 'all' ? true : p.status === 'pending').map(p => (
                    <tr key={p.id} style={{ transition: '0.2s' }}>
                      <td style={tableCellStyle}>
                        <img src={p.image_url} alt={p.name} style={{ width: '50px', height: '50px', borderRadius: '8px', objectFit: 'cover' }} onError={(e) => { e.target.src = "https://via.placeholder.com/50"; }} />
                      </td>
                      <td style={tableCellStyle}>{p.name}</td>
                      <td style={tableCellStyle}>{p.seller_name || "Unknown"}</td>
                      <td style={{ ...tableCellStyle, color: '#a29bfe', fontWeight: 'bold' }}>{p.price} $</td>
                      <td style={{ ...tableCellStyle, color: colors.success }}>{p.status}</td>
                      <td style={tableCellStyle}>
                        {p.status === 'pending' ? (
                          <div style={{ display: 'flex', gap: '8px' }}>
                            <button onClick={() => handleProductAction(p.id, 'approved')} style={{ background: colors.success, color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Approve</button>
                            <button onClick={() => handleProductAction(p.id, 'rejected')} style={{ background: colors.danger, color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Reject</button>
                          </div>
                        ) : (
                          <button onClick={() => handleProductAction(p.id, 'deleted')} style={{ background: '#475569', color: '#fff', border: 'none', padding: '6px 16px', borderRadius: '6px', cursor: 'pointer' }}>Delete</button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* --- Overview Tab --- */}
        {activeTab === 'statistics' && (
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <div style={{ background: 'linear-gradient(135deg, #6b4ce6, #a29bfe)', padding: '25px', borderRadius: '12px', flex: 1, color: '#fff' }}>
              <h4 style={{ margin: '0 0 10px 0' }}>Escrow Balance</h4>
              <p style={{ fontSize: '28px', fontWeight: 'bold', margin: 0 }}>{finances.total_held}</p>
            </div>
            <div style={{ background: 'linear-gradient(135deg, #059669, #34d399)', padding: '25px', borderRadius: '12px', flex: 1, color: '#fff' }}>
              <h4 style={{ margin: '0 0 10px 0' }}>Total Completed</h4>
              <p style={{ fontSize: '28px', fontWeight: 'bold', margin: 0 }}>{finances.pending_payouts}</p>
            </div>
            <div style={{ background: colors.bgCard, border: `1px solid ${colors.border}`, padding: '25px', borderRadius: '12px', flex: 1 }}>
              <h4 style={{ margin: '0 0 10px 0', color: colors.textDim }}>Active Users</h4>
              <p style={{ fontSize: '28px', fontWeight: 'bold', margin: 0 }}>{users.length}</p>
            </div>
          </div>
        )}

        {/* --- Users Tab --- */}
        {activeTab === 'users' && (
          <div style={{ background: colors.bgCard, borderRadius: '12px', overflow: 'hidden', border: `1px solid ${colors.border}` }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ background: colors.primary }}>
                <tr><th style={tableHeaderStyle}>Name</th><th style={tableHeaderStyle}>Type</th><th style={tableHeaderStyle}>Balance</th><th style={tableHeaderStyle}>Actions</th></tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id}>
                    <td style={tableCellStyle}>{u.name}</td>
                    <td style={tableCellStyle}>{u.role}</td>
                    <td style={{ ...tableCellStyle, color: '#a29bfe', fontWeight: 'bold' }}>{u.balance}</td>
                    <td style={{ ...tableCellStyle, display: 'flex', gap: '8px' }}>
                      <button onClick={() => startChatWithUser(u)} style={{ background: '#0ea5e9', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>💬 Chat</button>
                      <button onClick={() => handleUpdateBalance(u.id, u.balance)} style={{ background: '#f59e0b', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>💰 Balance</button>
                      <button onClick={() => handleRoleChange(u.id)} style={{ background: colors.primary, color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>🎭 Role</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* --- Sellers Tab --- */}
        {activeTab === 'sellers' && (
          <div style={{ background: colors.bgCard, borderRadius: '12px', overflow: 'hidden', border: `1px solid ${colors.border}` }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ background: colors.primary }}>
                <tr><th style={tableHeaderStyle}>Request ID</th><th style={tableHeaderStyle}>Store Name</th><th style={tableHeaderStyle}>Actions</th></tr>
              </thead>
              <tbody>
                {sellers.map(s => (
                  <tr key={s.request_id}>
                    <td style={tableCellStyle}>#{s.request_id}</td>
                    <td style={tableCellStyle}>{s.store_name}</td>
                    <td style={{ ...tableCellStyle, display: 'flex', gap: '8px' }}>
                      <button onClick={() => handleSellerAction(s.request_id, 'approved')} style={{ background: colors.success, color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Approve & Upgrade</button>
                      <button onClick={() => handleSellerAction(s.request_id, 'rejected')} style={{ background: colors.danger, color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Reject</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* --- QR Transactions Tab --- */}
        {activeTab === 'qr' && (
          <div style={{ background: colors.bgCard, borderRadius: '12px', overflow: 'hidden', border: `1px solid ${colors.border}` }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ background: colors.primary }}>
                <tr><th style={tableHeaderStyle}>Store</th><th style={tableHeaderStyle}>Amount</th><th style={tableHeaderStyle}>Status</th><th style={tableHeaderStyle}>Actions</th></tr>
              </thead>
              <tbody>
                {qrRequests.map(q => (
                  <tr key={q.id}>
                    <td style={tableCellStyle}>{q.store || q.store_name}</td>
                    <td style={{ ...tableCellStyle, color: colors.success, fontWeight: 'bold' }}>{q.amount} $</td>
                    <td style={tableCellStyle}>{q.status}</td>
                    <td style={tableCellStyle}>
                      {q.status === 'Pending' && (
                        <button onClick={() => handleReleaseFunds(q)} style={{ background: colors.primary, color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Release Funds</button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* --- Messages Tab --- */}
        {activeTab === 'messages' && (
          <div style={{ display: 'flex', height: '75vh', gap: '20px' }}>
            <div style={{ width: '280px', background: colors.bgCard, borderRadius: '12px', border: `1px solid ${colors.border}`, overflowY: 'auto' }}>
              <h4 style={{ padding: '20px', margin: 0, borderBottom: `1px solid ${colors.border}`, color: '#a29bfe' }}>Chats</h4>
              {chats.map(chat => (
                <div key={chat.id} onClick={() => setActiveChat(chat)} 
                     style={{ padding: '15px 20px', cursor: 'pointer', background: (String(activeChat?.id) === String(chat.id)) ? colors.primary : 'transparent', borderBottom: `1px solid ${colors.border}` }}>
                  {chat.full_name}
                </div>
              ))}
            </div>

            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', background: colors.bgCard, borderRadius: '12px', border: `1px solid ${colors.border}` }}>
              {activeChat ? (
                <>
                  <div style={{ padding: '20px', background: colors.bgSidebar, borderRadius: '12px 12px 0 0', borderBottom: `1px solid ${colors.border}`, fontWeight: 'bold' }}>
                    {activeChat.full_name || activeChat.name}
                  </div>
                  <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {messages.map((m, i) => {
                      const isMe = String(m.sender_id) === String(userId);
                      return (
                        <div key={i} style={{ alignSelf: isMe ? 'flex-end' : 'flex-start', background: isMe ? colors.primary : colors.bgSidebar, padding: '10px 15px', borderRadius: '10px', maxWidth: '70%', border: isMe ? 'none' : `1px solid ${colors.border}` }}>
                          {m.message_text || m.message}
                        </div>
                      );
                    })}
                  </div>
                  <div style={{ padding: '15px', borderTop: `1px solid ${colors.border}`, display: 'flex', gap: '10px' }}>
                    <input type="text" value={newMessage} onChange={e => setNewMessage(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage()} 
                           style={{ flex: 1, padding: '12px', borderRadius: '8px', border: `1px solid ${colors.border}`, background: colors.bgMain, color: '#fff', outline: 'none' }} placeholder="Type a message..." />
                    <button onClick={sendMessage} style={{ padding: '0 25px', background: colors.success, color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>Send</button>
                  </div>
                </>
              ) : <div style={{ margin: 'auto', color: colors.textDim }}>Select a user to start chatting</div>}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

const Table = ({ headers, data, renderRow }) => (
  <table className="main-table">
    <thead><tr>{headers.map(h => <th key={h}>{h}</th>)}</tr></thead>
    <tbody>{data.length > 0 ? data.map(renderRow) : <tr><td colSpan={headers.length} style={{ textAlign: 'center', padding: '20px' }}>No records found</td></tr>}</tbody>
  </table>
);

export default App;