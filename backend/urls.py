from django.urls import path
from admin_api import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- [1] نظام الهوية والمستخدمين (Identity & Users) ---
    # يغطي: Login, Register
    path('api/auth/<str:action>/', views.AuthController.as_view()),
    
    # يغطي: Users list, Update Role, Update Balance
    path('api/users/', views.UserManagementController.as_view()),
    path('api/users/<int:user_id>/', views.UserManagementController.as_view()),
    
    # يغطي: Addresses & Notifications
    path('api/users/<int:user_id>/addresses/', views.UserManagementController.as_view()),
    path('api/users/<int:user_id>/notifications/', views.UserManagementController.as_view()),
    path('api/users/upgrade-seller/', views.UserManagementController.as_view()),

    # --- [2] نظام المنتجات (Marketplace & Products) ---
    # يغطي: All products, Approved only (via query params), Add product
    path('api/products/', views.ProductController.as_view()),
    path('api/products/<int:pk>/', views.ProductController.as_view()),
    
    # يغطي: Pending products & Status updates (Approved/Rejected)
    path('api/products/review/', views.ProductController.as_view()),

    # --- [3] اللوجستيات والمحطات (Logistics & Stations) ---
    # يغطي: Stations list, Full Details, Station Dashboard
    path('api/logistics/stations/', views.LogisticController.as_view()),
    path('api/logistics/stations/<int:station_id>/', views.LogisticController.as_view()),
    path('api/logistics/trucks/', views.LogisticController.as_view()), # لجلب الشاحنات المتاحة
    
    # يغطي العمليات: (Receive, Load, Unload, Dispatch)
    path('api/logistics/shipments/<str:action>/', views.LogisticController.as_view()),

    # --- [4] النظام المالي (Finances & QR) ---
    # يغطي: Admin Finance Overview, QR Requests list
    path('api/finances/', views.FinanceController.as_view()),
    
    # يغطي العمليات المالية: (Initiate Purchase, Release Funds, Chat Purchase)
    path('api/finances/transactions/<str:action>/', views.FinanceController.as_view()),

    # --- [5] نظام التواصل (Chat & Messages) ---
    # يغطي: Active Chats, Message History
    path('api/chats/user/<int:user_id>/', views.ChatController.as_view()),
    path('api/chats/history/<int:sender_id>/<int:receiver_id>/', views.ChatController.as_view()),
    
    # يغطي الأفعال: (Send message, Chat request, Respond to request, Negotiated Offer)
    path('api/chats/actions/<str:action>/', views.ChatController.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)