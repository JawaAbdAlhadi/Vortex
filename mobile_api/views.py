from django.shortcuts import render

# Create your views here.
from django.db import connection, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class DB:
    """محرك قاعدة البيانات: يمنع تكرار الكود ويضمن استرجاع البيانات كقواميس (Dicts)"""
    @staticmethod
    def execute(query, params=None, fetch="all"):
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            if query.strip().upper().startswith("SELECT"):
                columns = [col[0] for col in cursor.description]
                if fetch == "one":
                    row = cursor.fetchone()
                    return dict(zip(columns, row)) if row else None
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return cursor.rowcount

class Service:
    """منطق الأعمال المشترك (Notifications & Finance)"""
    @staticmethod
    def notify(user_id, message):
        DB.execute("INSERT INTO Notifications (user_id, message, created_at) VALUES (%s, %s, %s)", 
                  [user_id, message, timezone.now()])

    @staticmethod
    def update_balance(user_id, amount, op='set'):
        if op == 'add': sql = "UPDATE Users SET balance = balance + %s WHERE user_id = %s"
        elif op == 'sub': sql = "UPDATE Users SET balance = balance - %s WHERE user_id = %s"
        else: sql = "UPDATE Users SET balance = %s WHERE user_id = %s"
        DB.execute(sql, [amount, user_id])

@method_decorator(csrf_exempt, name='dispatch')
class AuthController(APIView):
    def post(self, request, action):
        data = request.data
        if action == 'login':
            user = DB.execute("SELECT full_name, user_type, user_id FROM Users WHERE email=%s AND password_hash=%s", 
                             [data.get('email'), data.get('password')], fetch="one")
            return Response(user if user else {"error": "Unauthorized"}, status=200 if user else 401)
        
        if action == 'register':
            if DB.execute("SELECT user_id FROM Users WHERE email=%s", [data.get('email')], fetch="one"):
                return Response({"error": "Email exists"}, status=400)
            DB.execute("INSERT INTO Users (full_name, email, password_hash, user_type, balance) VALUES (%s,%s,%s,'buyer',0)",
                      [data.get('full_name'), data.get('email'), data.get('password')])
            return Response({"status": "success"})

@method_decorator(csrf_exempt, name='dispatch')
class UserManagementController(APIView):
    """إدارة المستخدمين، العناوين، والإشعارات"""
    def get(self, request, user_id=None):
        if user_id: # جلب إشعارات أو عناوين مستخدم محدد
            if 'notifications' in request.path:
                return Response(DB.execute("SELECT * FROM Notifications WHERE user_id=%s ORDER BY created_at DESC", [user_id]))
            return Response(DB.execute("SELECT id, name, details FROM addresses WHERE user_id=%s", [user_id]))
        # للآدمن: جلب كل المستخدمين
        return Response(DB.execute("SELECT u.user_id as id, u.full_name as name, u.user_type as role, u.balance FROM Users u"))

    def post(self, request): # إضافة عنوان أو ترقية بائع
        data = request.data
        if 'address' in request.path:
            DB.execute("INSERT INTO addresses (name, details, user_id) VALUES (%s,%s,%s)", 
                      [data.get('name', data.get('title')), data.get('details', data.get('address')), data.get('user_id')])
        elif 'upgrade' in request.path:
            DB.execute("UPDATE Users SET user_type='seller' WHERE user_id=%s", [data.get('user_id')])
            DB.execute("INSERT INTO SellerRequests (user_id, store_name, status) VALUES (%s, %s, 'approved')", 
                      [data.get('user_id'), data.get('store_name', 'Auto-Upgraded Store')])
        return Response({"status": "success"})

    def put(self, request): # تحديث الرصيد أو الدور
        data = request.data
        if 'balance' in data: Service.update_balance(data.get('user_id'), data.get('balance'))
        if 'role' in data: DB.execute("UPDATE Users SET user_type=%s WHERE user_id=%s", [data.get('role'), data.get('user_id')])
        return Response({"status": "success"})
    
@method_decorator(csrf_exempt, name='dispatch')
class ProductController(APIView):
    def get(self, request, pk=None):
        if pk: return Response(DB.execute("SELECT id, name, status FROM Products WHERE id=%s", [pk], fetch="one"))
        
        status_filter = request.query_params.get('status', 'approved')
        query = "SELECT p.*, u.full_name as seller_name FROM products p LEFT JOIN users u ON p.seller_id=u.user_id"
        if status_filter != 'all': query += f" WHERE p.status='{status_filter}'"
        return Response(DB.execute(query))

    def post(self, request):
        data, img = request.data, request.FILES.get('image')
        path = default_storage.save(f'products/{img.name}', img) if img else "products/default.png"
        DB.execute("INSERT INTO products (name, price, description, image_url, seller_id, status) VALUES (%s,%s,%s,%s,%s,'pending')",
                  [data.get('name'), data.get('price'), data.get('description'), path, data.get('seller_id')])
        return Response({"status": "success"})

    def patch(self, request): # تحديث الحالة
        DB.execute("UPDATE products SET status=%s WHERE id=%s", [request.data.get('status'), request.data.get('product_id')])
        return Response({"status": "updated"})
    
@method_decorator(csrf_exempt, name='dispatch')    
class FinanceController(APIView):
    def get(self, request): # للآدمن فقط
        summary = {
            "held": DB.execute("SELECT SUM(amount) as total FROM QRTransactions WHERE status='Pending'", fetch="one")['total'] or 0,
            "completed": DB.execute("SELECT SUM(amount) as total FROM QRTransactions WHERE status='Completed'", fetch="one")['total'] or 0,
            "transactions": DB.execute("SELECT * FROM QRTransactions")
        }
        return Response(summary)

    def post(self, request, action):
        data = request.data
        if action == 'purchase':
            prod = DB.execute("SELECT price, seller_id, name FROM products WHERE id=%s", [data.get('product_id')], fetch="one")
            buyer_bal = DB.execute("SELECT balance FROM Users WHERE user_id=%s", [data.get('buyer_id')], fetch="one")['balance']
            
            if buyer_bal < prod['price']: return Response({"error": "No balance"}, status=400)
            
            with transaction.atomic():
                Service.update_balance(data.get('buyer_id'), prod['price'], 'sub')
                Service.update_balance(1, prod['price'], 'add') # حساب الوسيط
                DB.execute("INSERT INTO QRTransactions (store_name, amount, status, qr_type, seller_id) VALUES (%s,%s,'Pending',%s,%s)",
                          [prod['name'], prod['price'], f"Purchase by {data.get('buyer_id')}", prod['seller_id']])
            return Response({"status": "success"})

        if action == 'release':
            with transaction.atomic():
                DB.execute("UPDATE QRTransactions SET status='Completed' WHERE id=%s", [data.get('transaction_id')])
                Service.update_balance(data.get('seller_id'), data.get('amount'), 'add')
                Service.update_balance(1, data.get('amount'), 'sub')
            return Response({"status": "released"})

@method_decorator(csrf_exempt, name='dispatch')    
class ChatController(APIView):
    def get(self, request, user_id):
        if 'requests' in request.path:
            return Response(DB.execute("SELECT cr.*, u.full_name FROM ChatRequests cr JOIN Users u ON cr.sender_id=u.user_id WHERE cr.receiver_id=%s AND cr.status='Pending'", [user_id]))
        # جلب المحادثات النشطة
        return Response(DB.execute("SELECT DISTINCT u.user_id, u.full_name FROM Users u WHERE u.user_id IN (SELECT CASE WHEN sender_id=%s THEN receiver_id ELSE sender_id END FROM Messages WHERE sender_id=%s OR receiver_id=%s)", [user_id, user_id, user_id]))

    def post(self, request, action):
        data = request.data
        if action == 'send':
            DB.execute("INSERT INTO Messages (sender_id, receiver_id, message_text) VALUES (%s,%s,%s)", 
                      [data.get('sender_id'), data.get('receiver_id'), data.get('message_text')])
        elif action == 'request':
            DB.execute("INSERT INTO ChatRequests (sender_id, receiver_id, status) VALUES (%s,%s,'Pending')", 
                      [data.get('sender_id'), data.get('receiver_id')])
        return Response({"status": "success"})
    
