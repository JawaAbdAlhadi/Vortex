import React, { useState } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import '../css/station.css';

// إصلاح أيقونات الخريطة
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

function StationDashboard() {
    // --- البيانات الأولية للأسطول ---
    const initialFleet = [
        { id: 'T1', name: 'شاحنة العملاق 01', type: 'truck', load: [], status: 'available' },
        { id: 'T2', name: 'شاحنة النسر 02', type: 'truck', load: [], status: 'available' },
        { id: 'T3', name: 'شاحنة البرق 03', type: 'truck', load: [], status: 'available' },
        { id: 'C1', name: 'سيارة السريع 01', type: 'car', load: [], status: 'available' },
        { id: 'C2', name: 'سيارة الرعد 02', type: 'car', load: [], status: 'available' },
        { id: 'C3', name: 'سيارة الفهد 03', type: 'car', load: [], status: 'available' },
    ];

    // --- State Management ---
    const [warehouse, setWarehouse] = useState([]); // الطرود في المستودع
    const [fleet, setFleet] = useState(initialFleet); // الأسطول الكامل
    const [activeVehicleId, setActiveVehicleId] = useState('C1'); // المركبة المختارة حالياً للتحميل
    const [newProductId, setNewProductId] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [toast, setToast] = useState({ show: false, message: '', type: 'success' });
    const [trackingInfo, setTrackingInfo] = useState({ isTracking: false, vehicle: null });

    const stationCoords = [33.5138, 36.2765];
    const buyerCoords = [33.5300, 36.2900];

    const showToast = (message, type = 'success') => {
        setToast({ show: true, message, type });
        setTimeout(() => setToast({ show: false, message: '', type: 'success' }), 3000);
    };

    // 1. إضافة مركبة جديدة للأسطول
    const addNewVehicle = (type) => {
        const newId = `${type === 'truck' ? 'T' : 'C'}${fleet.length + 1}`;
        const newName = `${type === 'truck' ? 'شاحنة' : 'سيارة'} جديدة ${fleet.length + 1}`;
        setFleet([...fleet, { id: newId, name: newName, type, load: [], status: 'available' }]);
        showToast(`تم إضافة ${newName} للأسطول`);
    };

    // 2. تحميل منتج من المستودع إلى المركبة المختارة
    const loadToActiveVehicle = (product) => {
        const vehicle = fleet.find(v => v.id === activeVehicleId);
        if (vehicle.status !== 'available') return showToast("هذه المركبة في رحلة الآن!", "error");

        setWarehouse(warehouse.filter(p => p.id !== product.id));
        setFleet(fleet.map(v => 
            v.id === activeVehicleId ? { ...v, load: [...v.load, product] } : v
        ));
        showToast(`تم تحميل ${product.name} في ${vehicle.name}`);
    };

    // 3. إعادة المنتج للمستودع (Unload)
    const unloadFromVehicle = (vehicleId, product) => {
        setFleet(fleet.map(v => 
            v.id === vehicleId ? { ...v, load: v.load.filter(p => p.id !== product.id) } : v
        ));
        setWarehouse([...warehouse, product]);
        showToast("تم إعادة الطرد إلى المستودع");
    };

    // 4. انطلاق المركبة
    const dispatchVehicle = async (vehicleId) => {
        const vehicle = fleet.find(v => v.id === vehicleId);
        if (vehicle.load.length === 0) return showToast("المركبة فارغة!", "error");

        setIsProcessing(true);
        try {
            const mainProduct = vehicle.load[0];
            await axios.post('http://127.0.0.1:8000/api/station/dispatch/', {
                product_id: mainProduct.id,
                buyer_id: mainProduct.buyer_id,
                car_id: vehicle.id
            });

            setFleet(fleet.map(v => v.id === vehicleId ? { ...v, status: 'on-trip' } : v));
            showToast(`🚀 انطلقت ${vehicle.name}! تم إرسال التنبيهات`);
            
            if (vehicle.type === 'car') {
                setTrackingInfo({ isTracking: true, vehicle: vehicle });
            }
        } catch (err) {
            showToast("خطأ في الاتصال بالسيرفر", "error");
        } finally { setIsProcessing(false); }
    };

    const activeVehicle = fleet.find(v => v.id === activeVehicleId);

    return (
        <div className="station-layout">
            {toast.show && <div className={`toast-notification ${toast.type}`}>{toast.message}</div>}

            <header className="station-header">
                <h2>مركز العمليات اللوجستية المطور</h2>
                <div className="header-actions">
                    <button onClick={() => addNewVehicle('truck')}>+ إضافة شاحنة</button>
                    <button onClick={() => addNewVehicle('car')}>+ إضافة سيارة</button>
                </div>
            </header>

            <div className="main-dashboard-grid">
                
                {/* 1. قائمة الأسطول (على اليمين) */}
                <aside className="fleet-sidebar">
                    <h3>📁 إدارة الأسطول</h3>
                    <div className="fleet-list">
                        {fleet.map(v => (
                            <div 
                                key={v.id} 
                                className={`fleet-item ${activeVehicleId === v.id ? 'active' : ''} ${v.status}`}
                                onClick={() => setActiveVehicleId(v.id)}
                            >
                                <span className="icon">{v.type === 'truck' ? '🚛' : '🚗'}</span>
                                <div className="info">
                                    <p>{v.name}</p>
                                    <small>{v.load.length} طرود | {v.status === 'available' ? 'جاهزة' : 'في رحلة'}</small>
                                </div>
                            </div>
                        ))}
                    </div>
                </aside>

                {/* 2. منطقة العمليات (الوسط) */}
                <main className="ops-center">
                    <section className="warehouse-section action-card">
                        <h3>📦 المستودع المركزى</h3>
                        <div className="scan-box">
                            <input type="number" placeholder="ID المنتج..." value={newProductId} onChange={e => setNewProductId(e.target.value)} />
                            <button onClick={async () => {
                                setIsProcessing(true);
                                try {
                                    const res = await axios.get(`http://127.0.0.1:8000/api/station/get-product/${newProductId}/`);
                                    setWarehouse([...warehouse, res.data]);
                                    setNewProductId('');
                                } catch { showToast("غير موجود", "error"); }
                                finally { setIsProcessing(false); }
                            }}>استلام</button>
                        </div>
                        <div className="p-grid">
                            {warehouse.map(p => (
                                <div key={p.id} className="p-card">
                                    <p>{p.name}</p>
                                    <button onClick={() => loadToActiveVehicle(p)}>تحميل في {activeVehicle?.name}</button>
                                </div>
                            ))}
                        </div>
                    </section>
                </main>

                {/* 3. منطقة التحميل النشطة (اليسار) */}
                <section className="loading-bay-advanced">
                    <h3>🚚 منطقة التحميل النشطة</h3>
                    {activeVehicle && (
                        <div className="active-vehicle-card">
                            <div className="av-header">
                                <h4>{activeVehicle.name}</h4>
                                <span className={`status-tag ${activeVehicle.status}`}>{activeVehicle.status}</span>
                            </div>
                            <div className="loaded-items">
                                {activeVehicle.load.map(p => (
                                    <div key={p.id} className="loaded-item">
                                        <span>{p.name}</span>
                                        <button className="unload-btn" onClick={() => unloadFromVehicle(activeVehicle.id, p)}>↩</button>
                                    </div>
                                ))}
                                {activeVehicle.load.length === 0 && <p className="empty-msg">المركبة فارغة</p>}
                            </div>
                            <button className="dispatch-main-btn" onClick={() => dispatchVehicle(activeVehicle.id)} disabled={isProcessing}>
                                إعطاء أمر الانطلاق 🚀
                            </button>
                        </div>
                    )}
                </section>
            </div>

            {/* الخريطة */}
            {trackingInfo.isTracking && (
                <div className="tracking-overlay">
                    <div className="tracking-modal">
                        <header>
                            <h3>📍 تتبع: {trackingInfo.vehicle.name}</h3>
                            <button onClick={() => setTrackingInfo({ ...trackingInfo, isTracking: false })}>✖</button>
                        </header>
                        <div className="map-frame">
                            <MapContainer center={stationCoords} zoom={13} style={{ height: '100%', width: '100%' }}>
                                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                                <Marker position={stationCoords}><Popup>المحطة</Popup></Marker>
                                <Marker position={buyerCoords}><Popup>وجهة العميل</Popup></Marker>
                                <Polyline positions={[stationCoords, buyerCoords]} color="#3b82f6" weight={5} dashArray="10, 10" />
                            </MapContainer>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default StationDashboard;