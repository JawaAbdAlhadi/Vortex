from django.urls import path
from admin_api import views 

urlpatterns = [
    # الدخول والمستخدمين
    path('api/login/', views.login_view),
    path('api/users-list/', views.get_all_users),
    path('api/update-balance/', views.update_user_balance),
    path('api/update-role/', views.update_user_role),

    # إدارة المتاجر (SellerRequests)
    path('api/pending-sellers/', views.pending_sellers),
    path('api/update-seller/', views.update_seller_status),
    
    # إدارة الـ QR والمالية (القديم)
    path('api/qr-requests/', views.qr_requests_view),
    path('api/admin/finances/', views.admin_finances_view),

    # إدارة المنتجات (الجديد)
    path('api/pending-products/', views.pending_products),
    path('api/update-product-status/', views.update_product_status),
    path('api/approved-products/', views.get_approved_products),
    path('api/add-product/', views.add_product),
    path('api/register/', views.register_user),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/messages/<int:user_id>/', views.get_messages, name='get_messages'),
    # بدل السطر القديم بهذا:
    path('api/request-seller/', views.request_seller, name='request_seller'),
]