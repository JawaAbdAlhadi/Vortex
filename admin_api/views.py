from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 1. التحقق من الدخول (يجلب الاسم والرتبة وID)
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    with connection.cursor() as cursor:
        cursor.execute("SELECT full_name, user_type, user_id FROM Users WHERE email = %s AND password_hash = %s", [email, password])
        user = cursor.fetchone()
    if user:
        return Response({"message": "success", "full_name": user[0], "user_type": user[1], "user_id": user[2]})
    return Response({"message": "error"}, status=401)

# 2. جلب طلبات المتاجر المعلقة (التجار الجدد)
@api_view(['GET'])
def pending_sellers(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT request_id, store_name, status FROM SellerRequests WHERE status = 'pending'")
        rows = cursor.fetchall()
    return Response([{"request_id": r[0], "store_name": r[1], "status": r[2]} for r in rows])

# 3. تحديث حالة المتجر (قبول أو رفض)
@api_view(['POST'])
def update_seller_status(request):
    req_id = request.data.get('request_id')
    new_status = request.data.get('status')
    with connection.cursor() as cursor:
        cursor.execute("UPDATE SellerRequests SET status = %s WHERE request_id = %s", [new_status, req_id])
    return Response({"message": "success"})

# 4. جلب قائمة المستخدمين كاملة مع الأرصدة والنشاط (QR)
@api_view(['GET'])
def get_all_users(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.user_id, u.full_name, u.user_type, u.balance, 
            (SELECT qr_type FROM QRTransactions WHERE store_name = u.full_name ORDER BY id DESC LIMIT 1) 
            FROM Users u
        """)
        rows = cursor.fetchall()
    return Response([{"id": r[0], "name": r[1], "role": r[2], "balance": f"{r[3]} $", "last_activity": r[4] or "None"} for r in rows])

# 5. جلب بيانات الـ QR الحقيقية
@api_view(['GET'])
def qr_requests_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, store_name, qr_type, amount, status FROM QRTransactions")
        rows = cursor.fetchall()
    return Response([{"id": r[0], "store": r[1], "type": r[2], "amount": f"{r[3]} $", "status": r[4]} for r in rows])

# 6. جلب الإحصائيات المالية للـ Admin
@api_view(['GET'])
def admin_finances_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM(amount) FROM QRTransactions WHERE status = 'Pending'")
        held = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM QRTransactions WHERE status = 'Completed'")
        completed = cursor.fetchone()[0] or 0
    return Response({"total_held": f"{held} $", "pending_payouts": f"{completed} $"})

# 7. تعديل رصيد المستخدم يدوياً
@api_view(['POST'])
def update_user_balance(request):
    user_id = request.data.get('user_id')
    new_balance = request.data.get('balance')
    with connection.cursor() as cursor:
        cursor.execute("UPDATE Users SET balance = %s WHERE user_id = %s", [new_balance, user_id])
    return Response({"message": "success"})

# 8. تعديل رتبة المستخدم (جديد)
@api_view(['POST'])
def update_user_role(request):
    user_id = request.data.get('user_id')
    new_role = request.data.get('role')
    with connection.cursor() as cursor:
        cursor.execute("UPDATE Users SET user_type = %s WHERE user_id = %s", [new_role, user_id])
    return Response({"message": "success"})

# --- إضافات إدارة المنتجات (المنشورات) ---

@api_view(['GET'])
def pending_products(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.description, u.full_name 
            FROM products p 
            JOIN Users u ON p.seller_id = u.user_id 
            WHERE p.status = 'pending'
        """)
        rows = cursor.fetchall()
    return Response([{"id": r[0], "name": r[1], "price": r[2], "desc": r[3], "seller": r[4]} for r in rows])

@api_view(['POST'])
def update_product_status(request):
    prod_id = request.data.get('product_id')
    new_status = request.data.get('status')
    with connection.cursor() as cursor:
        cursor.execute("UPDATE products SET status = %s WHERE id = %s", [new_status, prod_id])
    return Response({"message": "success"})

@api_view(['GET'])
def get_approved_products(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.name, p.description, p.price, p.image_url, u.full_name 
            FROM products p 
            JOIN Users u ON p.seller_id = u.user_id 
            WHERE p.status = 'approved'
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
    return Response([{"id": r[0], "name": r[1], "desc": r[2], "price": r[3], "image": r[4], "seller": r[5]} for r in rows])

@api_view(['POST'])
def add_product(request):
    data = request.data
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO products (seller_id, name, description, price, image_url, status) 
            VALUES (%s, %s, %s, %s, %s, 'pending')
        """, [data.get('seller_id'), data.get('name'), data.get('description'), data.get('price'), data.get('image_url')])
    return Response({"message": "success"})

@api_view(['POST'])
def register_user(request):
    full_name = request.data.get('full_name')
    email = request.data.get('email')
    password = request.data.get('password')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", [email])
        if cursor.fetchone():
            return Response({"message": "Email already exists"}, status=400)
        
        # إنشاء مستخدم جديد برتبة 'buyer' ورصيد 0
        cursor.execute("""
            INSERT INTO Users (full_name, email, password_hash, user_type, balance) 
            VALUES (%s, %s, %s, 'buyer', 0)
        """, [full_name, email, password])
        
    return Response({"message": "success"})

@api_view(['POST'])
def send_message(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id') # سيكون 1 للأدمن دائماً حالياً
    text = request.data.get('message_text')
    is_admin = request.data.get('is_admin', False)

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Messages (sender_id, receiver_id, message_text, is_admin_reply)
            VALUES (%s, %s, %s, %s)
        """, [sender_id, receiver_id, text, is_admin])
    return Response({"message": "sent"})

@api_view(['GET'])
def get_messages(request, user_id):
    with connection.cursor() as cursor:
        # جلب المحادثة بين مستخدم معين والأدمن
        cursor.execute("""
            SELECT sender_id, message_text, is_admin_reply, created_at 
            FROM Messages 
            WHERE sender_id = %s OR receiver_id = %s
            ORDER BY created_at ASC
        """, [user_id, user_id])
        columns = [col[0] for col in cursor.description]
        messages = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return Response(messages)

@api_view(['POST'])
def request_seller(request):
    user_id = request.data.get('user_id')
    store_name = request.data.get('store_name')
    
    with connection.cursor() as cursor:
        # التأكد أن الجدول موجود والبيانات تُحفظ كـ pending
        cursor.execute("""
            INSERT INTO SellerRequests (user_id, store_name, status) 
            VALUES (%s, %s, 'pending')
        """, [user_id, store_name])
        
    return Response({"message": "success"})