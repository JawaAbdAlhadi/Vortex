# from django.db import connection, transaction
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.core.files.storage import default_storage
# import json
# from django.utils import timezone

# from django.views.decorators.csrf import csrf_exempt
# # Stations
# # 1. استلام الغرض من البائع في المحطة (مثال: محطة دمشق)
# @api_view(['POST'])
# def receive_at_station(request):
#     shipment_id = request.data.get('shipment_id')
#     station_id = request.data.get('station_id') # المحطة التي استلمت الغرض

#     with transaction.atomic():
#         # تحديث حالة الشحنة ومكانها الحالي
#         DB.query("""
#             UPDATE Shipments 
#             SET status = 'At Origin Station', current_station_id = %s 
#             WHERE id = %s
#         """, [station_id, shipment_id])
        
#         # جلب معلومات المشتري لإرسال إشعار
#         buyer_info = DB.query("""
#             SELECT u.user_id, u.full_name 
#             FROM Shipments s
#             JOIN QRTransactions t ON s.transaction_id = t.id
#             JOIN Users u ON t.buyer_id = u.user_id
#             WHERE s.id = %s
#         """, [shipment_id], fetch_one=True)
        
#         # هنا يمكنك حفظ الإشعار في جدول Notifications ليقرأه الفرونت إند
#         DB.query("INSERT INTO Notifications (user_id, message) VALUES (%s, %s)", 
#                  [buyer_info[0], f"مرحباً {buyer_info[1]}، منتجك تم استلامه في محطتنا وهو قيد التجهيز للشحن!"])

#     return Response({"message": "تم الاستلام بنجاح وإعلام المشتري."})

# @api_view(['GET'])
# def get_full_station_details(request):
#     try:
#         # جلب جميع المحطات
#         stations = DB.query("SELECT id, name, city, location_details FROM stations")
#         results = []
#         for s in stations:
#             s_id = s[0]
#             # جلب الشاحنات المرتبطة بهذه المحطة
#             trucks = DB.query("SELECT id, plate_number, status FROM trucks WHERE current_station_id = %s", [s_id])
#             # جلب المنتجات المخزنة في هذه المحطة
#             products = DB.query("SELECT id, product_name, quantity FROM station_products WHERE station_id = %s", [s_id])
            
#             results.append({
#                 "id": s_id,
#                 "name": s[1],
#                 "city": s[2],
#                 "location": s[3],
#                 "trucks": [{"id": t[0], "plate": t[1], "status": t[2]} for t in trucks],
#                 "products": [{"id": p[0], "name": p[1], "qty": p[2]} for p in products]
#             })
#         return Response(results)
#     except Exception as e:
#         return Response({"status": "error", "message": str(e)}, status=500)
    
# @api_view(['PUT'])
# def update_station_details(request, station_id):
#     try:
#         data = request.data
#         name = data.get('name')
#         city = data.get('city')
#         location_details = data.get('location_details')

#         # تحديث بيانات المحطة في قاعدة البيانات (تأكد من مطابقة أسماء الحقول في SQL)
#         query = "UPDATE stations SET name=%s, city=%s, location_details=%s WHERE id=%s"
#         DB.query(query, [name, city, location_details, station_id])
        
#         return Response({"status": "success", "message": "تم تحديث بيانات المحطة بنجاح"})
#     except Exception as e:
#         return Response({"status": "error", "message": str(e)}, status=500)
    
# # admin_api/views.py

# @api_view(['GET'])
# def get_station_dashboard_data(request):
#     try:
#         # 1. جلب بيانات المحطات الأساسية
#         stations = DB.query("SELECT id, name, city, location_details FROM stations")
        
#         all_data = []
#         for s in stations:
#             s_id = s[0]
            
#             # 2. جلب الشاحنات المرتبطة بكل محطة (تأكد من وجود عمود current_station_id في جدول trucks)
#             trucks = DB.query("""
#                 SELECT id, plate_number, status 
#                 FROM trucks 
#                 WHERE current_station_id = %s
#             """, [s_id])
            
#             # 3. جلب المنتجات الموجودة في مخزن المحطة (جدول station_products)
#             products = DB.query("""
#                 SELECT id, product_name, quantity 
#                 FROM station_products 
#                 WHERE station_id = %s
#             """, [s_id])
            
#             all_data.append({
#                 "id": s_id,
#                 "name": s[1],
#                 "city": s[2],
#                 "location": s[3],
#                 "trucks": [{"id": t[0], "plate": t[1], "status": t[2]} for t in trucks],
#                 "products": [{"id": p[0], "name": p[1], "qty": p[2]} for p in products]
#             })
            
#         return Response(all_data)
#     except Exception as e:
#         # طباعة الخطأ في الكونسول لتسهيل التنقيح
#         print(f"Error in get_station_dashboard_data: {str(e)}")
#         return Response({"status": "error", "message": str(e)}, status=500)

# @api_view(['DELETE'])
# def delete_station(request, station_id):
#     try:
#         # التأكد من عدم وجود شاحنات أو شحنات مرتبطة بالمحطة قبل الحذف (اختياري لكنه أفضل)
#         with transaction.atomic():
#             DB.query("DELETE FROM stations WHERE id = %s", [station_id])
#             return Response({"status": "success", "message": "تم حذف المحطة بنجاح"})
#     except Exception as e:
#         return Response({"status": "error", "message": str(e)}, status=500)
# # 2. تحميل البضائع إلى الشاحنة (تغيير الحالة إلى In Transit)
# @api_view(['POST'])
# def load_to_truck(request):
#     shipment_id = request.data.get('shipment_id')
#     truck_id = request.data.get('truck_id')

#     DB.query("""
#         UPDATE Shipments 
#         SET status = 'In Transit', truck_id = %s 
#         WHERE id = %s
#     """, [truck_id, shipment_id])
    
#     return Response({"message": "تم تحميل المنتج للشاحنة وهو الآن في طريقه."})

# # 3. تفريغ الشاحنة في محطة الوصول (مثال: محطة اللاذقية)
# @api_view(['POST'])
# def unload_at_destination(request):
#     shipment_id = request.data.get('shipment_id')
#     destination_station_id = request.data.get('station_id')

#     with transaction.atomic():
#         DB.query("""
#             UPDATE Shipments 
#             SET status = 'At Destination Station', current_station_id = %s, truck_id = NULL 
#             WHERE id = %s
#         """, [destination_station_id, shipment_id])
        
#         # إرسال إشعار للمشتري أن منتجه وصل لمدينته
#         buyer_info = DB.query("... نفس استعلام جلب المشتري السابق ...", [shipment_id], fetch_one=True)
        
#         DB.query("INSERT INTO Notifications (user_id, message) VALUES (%s, %s)", 
#                  [buyer_info[0], f"منتجك وصل إلى محطة مدينتك (اللاذقية)! يمكنك استلامه الآن."])

#     return Response({"message": "تم تفريغ الشحنة وإعلام المشتري."})
# # 1. جلب قائمة المحطات (يطلبها السيرفر الآن)
# @api_view(['GET'])
# def get_all_stations(request):
#     stations = DB.query("SELECT id, name, city FROM Stations", fetch_all=True)
#     # تحويل البيانات لتنسيق JSON
#     data = [{"id": s[0], "name": s[1], "city": s[2]} for s in stations]
#     return Response(data)

# # 2. جلب الشاحنات المتاحة
# @api_view(['GET'])
# def get_available_trucks(request):
#     trucks = DB.query("SELECT id, plate_number FROM Trucks WHERE status = 'Available'", fetch_all=True)
#     data = [{"id": t[0], "plate_number": t[1]} for t in trucks]
#     return Response(data)

# # 3. جلب الشحنات الخاصة بمحطة معينة (التي استخدمناها في React)
# @api_view(['GET'])
# def get_station_shipments(request, station_id):
#     query = """
#         SELECT s.id, p.name, s.status 
#         FROM Shipments s
#         JOIN QRTransactions t ON s.transaction_id = t.id
#         JOIN Products p ON t.product_id = p.id
#         WHERE s.current_station_id = %s AND s.status = 'At Origin Station'
#     """
#     shipments = DB.query(query, [station_id], fetch_all=True)
#     data = [{"id": s[0], "product_name": s[1], "status": s[2]} for s in shipments]
#     return Response(data)

# # 4. إضافة عنوان للمستخدم
# @api_view(['POST'])
# def add_user_address(request):
#     user_id = request.data.get('user_id')
#     title = request.data.get('title')
#     address = request.data.get('address')
#     city = request.data.get('city')
    
#     DB.query("INSERT INTO UserAddresses (user_id, address_title, full_address, city) VALUES (%s, %s, %s, %s)", 
#              [user_id, title, address, city])
#     return Response({"message": "Address added successfully"})


# # 2. جلب إشعارات المستخدم (لتجنب الخطأ القادم في الـ URLs)
# @api_view(['GET'])
# def get_user_notifications(request, user_id):
#     notifications = DB.query("""
#         SELECT id, message, created_at 
#         FROM Notifications 
#         WHERE user_id = %s 
#         ORDER BY created_at DESC
#     """, [user_id], fetch_all=True)
    
#     data = [{
#         "id": n[0], 
#         "message": n[1], 
#         "time": n[2]
#     } for n in notifications]
    
#     return Response(data)

# # ==========================================
# # 1. Database & Logic Layer (Services)
# # ==========================================

# class DB:
#     """طبقة وسيطة للتعامل مع قاعدة البيانات لتقليل تكرار الكود"""
#     @staticmethod
#     def query(sql, params=None, fetch_one=False):
#         with connection.cursor() as cursor:
#             cursor.execute(sql, params or [])
#             if sql.strip().upper().startswith("SELECT"):
#                 return cursor.fetchone() if fetch_one else cursor.fetchall()
#             return None

#     @staticmethod
#     def get_columns(cursor):
#         return [col[0] for col in cursor.description]

# class User_Service:
#     @staticmethod
#     def update_balance(user_id, amount, mode='set'):
#         if mode == 'add':
#             sql = "UPDATE Users SET balance = balance + %s WHERE user_id = %s"
#         elif mode == 'subtract':
#             sql = "UPDATE Users SET balance = balance - %s WHERE user_id = %s"
#         else:
#             sql = "UPDATE Users SET balance = %s WHERE user_id = %s"
#         DB.query(sql, [amount, user_id])

# # ==========================================
# # 2. Authentication & User Management
# # ==========================================

# @api_view(['POST'])
# def login_view(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     user = DB.query("SELECT full_name, user_type, user_id FROM Users WHERE email = %s AND password_hash = %s", 
#                     [email, password], fetch_one=True)
#     if user:
#         return Response({"message": "success", "full_name": user[0], "user_type": user[1], "user_id": user[2]})
#     return Response({"message": "error"}, status=401)

# @api_view(['POST'])
# def register_user(request):
#     full_name = request.data.get('full_name')
#     email = request.data.get('email')
#     password = request.data.get('password')
    
#     if DB.query("SELECT user_id FROM Users WHERE email = %s", [email], fetch_one=True):
#         return Response({"message": "Email already exists"}, status=400)
    
#     DB.query("""INSERT INTO Users (full_name, email, password_hash, user_type, balance) 
#                 VALUES (%s, %s, %s, 'buyer', 0)""", [full_name, email, password])
#     return Response({"message": "success"})

# @api_view(['POST'])
# def upgrade_user_to_seller_instant(request):
#     user_id = request.data.get('user_id')
#     DB.query("UPDATE Users SET user_type = 'seller' WHERE user_id = %s", [user_id])
#     DB.query("INSERT INTO SellerRequests (user_id, store_name, status) VALUES (%s, 'Auto-Upgraded Store', 'approved')", [user_id])
#     return Response({"message": "تم ترقية حسابك إلى بائع بنجاح!"})

# # ==========================================
# # 3. Product & Store Management
# # ==========================================

# @api_view(['GET'])
# def get_approved_products(request):
#     rows = DB.query("""
#         SELECT p.id, p.name, p.description, p.price, p.image_url, u.full_name, p.seller_id 
#         FROM products p JOIN Users u ON p.seller_id = u.user_id 
#         WHERE p.status = 'approved' ORDER BY p.created_at DESC
#     """)
#     products = []
#     for r in rows:
#         raw_path = r[4]
#         img_url = f"http://127.0.0.1:8000/media/{raw_path}" if raw_path and not raw_path.startswith('http') else raw_path
#         products.append({
#             "id": r[0], "name": r[1], "desc": r[2], "price": r[3], 
#             "image": img_url, "seller": r[5], "seller_id": r[6]
#         })
#     return Response(products)

# @api_view(['POST'])
# def add_product(request):
#     image_file = request.FILES.get('image')
#     image_url = default_storage.save(f'products/{image_file.name}', image_file) if image_file else "products/default.png"
    
#     DB.query("""INSERT INTO products (name, price, description, image_url, seller_id, status)
#                 VALUES (%s, %s, %s, %s, %s, 'pending')""", 
#              [request.data.get('name'), request.data.get('price'), request.data.get('description'), image_url, request.data.get('seller_id')])
#     return Response({"message": "تم إرسال المنتج بنجاح"})

# @api_view(['GET'])
# def pending_products(request):
#     rows = DB.query("""SELECT p.id, p.name, p.price, p.description, u.full_name 
#                        FROM products p JOIN Users u ON p.seller_id = u.user_id 
#                        WHERE p.status = 'pending'""")
#     return Response([{"id": r[0], "name": r[1], "price": r[2], "desc": r[3], "seller": r[4]} for r in rows])

# @api_view(['POST'])
# def update_product_status(request):
#     DB.query("UPDATE products SET status = %s WHERE id = %s", [request.data.get('status'), request.data.get('product_id')])
#     return Response({"message": "success"})

# # ==========================================
# # 4. Chat & Messaging System
# # ==========================================

# @api_view(['POST'])
# def send_chat_request(request):
#     sid, rid = request.data.get('sender_id'), request.data.get('receiver_id')
#     if DB.query("SELECT id FROM ChatRequests WHERE sender_id=%s AND receiver_id=%s AND status='Pending'", [sid, rid], fetch_one=True):
#         return Response({"message": "طلبك قيد الانتظار بالفعل"}, status=400)
    
#     DB.query("INSERT INTO ChatRequests (sender_id, receiver_id, status) VALUES (%s, %s, 'Pending')", [sid, rid])
#     return Response({"message": "تم إرسال طلب المحادثة بنجاح"})

# @api_view(['GET'])
# def get_chat_requests(request, user_id):
#     rows = DB.query("""SELECT cr.id, cr.sender_id, u.full_name, cr.status FROM ChatRequests cr
#                        JOIN Users u ON cr.sender_id = u.user_id
#                        WHERE cr.receiver_id = %s AND (cr.status = 'Pending' OR cr.status = 'pending')""", [user_id])
#     return Response([{"id": r[0], "sender_id": r[1], "sender_name": r[2], "status": r[3]} for r in rows])

# @api_view(['POST'])
# def respond_to_chat(request):
#     DB.query("UPDATE ChatRequests SET status=%s WHERE id=%s", [request.data.get('status'), request.data.get('request_id')])
#     return Response({"message": f"تم {request.data.get('status')} الطلب"})

# @api_view(['GET'])
# def get_my_active_chats(request, user_id):
#     query = """
#         SELECT DISTINCT u.user_id, u.full_name FROM Users u
#         WHERE u.user_id IN (
#             SELECT CASE WHEN sender_id = %s THEN receiver_id ELSE sender_id END
#             FROM ChatRequests WHERE (sender_id = %s OR receiver_id = %s) AND status = 'Accepted'
#             UNION
#             SELECT CASE WHEN sender_id = %s THEN receiver_id ELSE sender_id END
#             FROM Messages WHERE (sender_id = %s OR receiver_id = %s)
#         ) AND u.user_id != %s
#     """
#     rows = DB.query(query, [user_id, user_id, user_id, user_id, user_id, user_id, user_id])
#     return Response([{"id": row[0], "full_name": row[1]} for row in rows])

# @api_view(['POST'])
# def send_message(request):
#     DB.query("""INSERT INTO Messages (sender_id, receiver_id, message_text, is_admin_reply)
#                 VALUES (%s, %s, %s, %s)""", 
#              [request.data.get('sender_id'), request.data.get('receiver_id'), request.data.get('message_text'), request.data.get('is_admin', False)])
#     return Response({"message": "sent"})

# @api_view(['GET'])
# def get_messages(request, sender_id, receiver_id):
#     with connection.cursor() as cursor:
#         cursor.execute("""SELECT sender_id, receiver_id, message_text, is_admin_reply, created_at FROM Messages 
#                           WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
#                           ORDER BY created_at ASC""", [sender_id, receiver_id, receiver_id, sender_id])
#         cols = DB.get_columns(cursor)
#         return Response([dict(zip(cols, row)) for row in cursor.fetchall()])

# # ==========================================
# # 5. Transactions & Finances
# # ==========================================

# @api_view(['POST'])
# def initiate_purchase(request):
#     bid, pid = request.data.get('buyer_id'), request.data.get('product_id')
    
#     # جلب بيانات المنتج
#     product = DB.query("SELECT price, seller_id, name FROM products WHERE id = %s", [pid], fetch_one=True)
    
#     if not product:
#         return Response({"message": "Product not found"}, status=404)

#     # --- الخطوة الناقصة: تعريف المتغيرات من نتيجة الاستعلام ---
#     price, seller_id, p_name = product 
#     # الآن أصبح 'price' معرفاً ولن يظهر السطر الأصفر

#     # ... التحقق من الرصيد (مثال) ...
#     buyer_balance = DB.query("SELECT balance FROM Users WHERE user_id = %s", [bid], fetch_one=True)[0]
#     if buyer_balance < price:
#         return Response({"message": "رصيدك غير كافٍ"}, status=400)

#     with transaction.atomic():
#         # حجز المبلغ (سيختفي السطر الأصفر هنا)
#         User_Service.update_balance(bid, price, 'subtract')
#         User_Service.update_balance(1, price, 'add')
        
#         # تخزين البيانات في المعاملة
#         DB.query("""INSERT INTO QRTransactions (store_name, amount, status, qr_type, seller_id) 
#                     VALUES (%s, %s, 'Pending', %s, %s)""", 
#                  [p_name, price, f"Purchase from User {bid}", seller_id])
        
#     return Response({"message": "success"})

# @api_view(['POST'])
# def execute_chat_purchase(request):
#     bid, sid, amount = request.data.get('buyer_id'), request.data.get('seller_id'), float(request.data.get('amount'))
#     balance = DB.query("SELECT balance FROM Users WHERE user_id = %s", [bid], fetch_one=True)
    
#     if not balance or balance[0] < amount:
#         return Response({"message": "رصيدك غير كافٍ لإتمام هذا العرض"}, status=400)
    
#     try:
#         with transaction.atomic():
#             User_Service.update_balance(bid, amount, 'subtract')
#             User_Service.update_balance(sid, amount, 'add')
#             DB.query("""INSERT INTO QRTransactions (store_name, amount, status, qr_type) 
#                         VALUES ((SELECT full_name FROM Users WHERE user_id=%s), %s, 'Completed', 'Chat Offer')""", [sid, amount])
#         return Response({"message": "تمت عملية الشراء بنجاح!"})
#     except Exception:
#         return Response({"message": "فشلت العملية، حاول لاحقاً"}, status=500)

# @api_view(['GET'])
# def admin_finances_view(request):
#     held = DB.query("SELECT SUM(amount) FROM QRTransactions WHERE status = 'Pending'", fetch_one=True)[0] or 0
#     completed = DB.query("SELECT SUM(amount) FROM QRTransactions WHERE status = 'Completed'", fetch_one=True)[0] or 0
#     return Response({"total_held": f"{held} $", "pending_payouts": f"{completed} $"})

# # ==========================================
# # 6. Admin & Seller Requests
# # ==========================================

# @api_view(['GET'])
# def pending_sellers(request):
#     # جرب تغيير SellerRequests إلى seller_requests
#     rows = DB.query("SELECT request_id, store_name, status FROM seller_requests WHERE status = 'pending'")
#     return Response([{"request_id": r[0], "store_name": r[1], "status": r[2]} for r in rows])

# @api_view(['POST'])
# def update_seller_status(request):
#     DB.query("UPDATE SellerRequests SET status = %s WHERE request_id = %s", [request.data.get('status'), request.data.get('request_id')])
#     return Response({"message": "success"})

# @api_view(['GET'])
# def get_all_users(request):
#     rows = DB.query("""
#         SELECT u.user_id, u.full_name, u.user_type, u.balance, 
#         (SELECT qr_type FROM QRTransactions WHERE store_name = u.full_name ORDER BY id DESC LIMIT 1) 
#         FROM Users u
#     """)
#     return Response([{"id": r[0], "name": r[1], "role": r[2], "balance": f"{r[3]} $", "last_activity": r[4] or "None"} for r in rows])

# @api_view(['POST'])
# def update_user_balance(request):
#     User_Service.update_balance(request.data.get('user_id'), request.data.get('balance'))
#     return Response({"message": "success"})

# @api_view(['POST'])
# def update_user_role(request):
#     DB.query("UPDATE Users SET user_type = %s WHERE user_id = %s", [request.data.get('role'), request.data.get('user_id')])
#     return Response({"message": "success"})

# @api_view(['POST'])
# def confirm_delivery(request):
#     return Response({"message": "تم تحويل الأموال للبائع بنجاح"})

# @api_view(['POST'])
# def request_seller(request):
#     """إرسال طلب ليصبح المستخدم بائعاً"""
#     user_id = request.data.get('user_id')
#     store_name = request.data.get('store_name')
#     DB.query("INSERT INTO SellerRequests (user_id, store_name, status) VALUES (%s, %s, 'pending')", 
#              [user_id, store_name])
#     return Response({"message": "success"})

# @api_view(['GET'])
# def qr_requests_view(request):
#     """عرض طلبات الـ QRTransactions للآدمن"""
#     rows = DB.query("SELECT id, store_name, qr_type, amount, status FROM QRTransactions")
#     return Response([{"id": r[0], "store": r[1], "type": r[2], "amount": f"{r[3]} $", "status": r[4]} for r in rows])

# @api_view(['POST'])
# def send_negotiated_offer(request):
#     """إرسال عرض سعر متفاوض عليه داخل المحادثة"""
#     sender_id = request.data.get('sender_id')
#     receiver_id = request.data.get('receiver_id')
#     offer_amount = request.data.get('amount')
#     message_text = f"OFFER_PRICE:{offer_amount}"
#     DB.query("INSERT INTO Messages (sender_id, receiver_id, message_text) VALUES (%s, %s, %s)", 
#              [sender_id, receiver_id, message_text])
#     return Response({"message": "تم إرسال العرض بنجاح"})

# @api_view(['POST'])
# def release_funds(request):
#     tid = request.data.get('transaction_id')
#     amount = float(request.data.get('amount'))

#     # جلب الـ seller_id من المعاملة مباشرة
#     transaction_data = DB.query("SELECT seller_id, store_name FROM QRTransactions WHERE id = %s", [tid], fetch_one=True)
    
#     if not transaction_data:
#         return Response({"error": "المعاملة غير موجودة"}, status=404)
    
#     seller_id = transaction_data[0]
#     store_name = transaction_data[1]

#     # إذا كان الـ ID لا يزال فارغاً بعد محاولة الربط
#     if not seller_id:
#         return Response({"error": f"البائع '{store_name}' غير مرتبط بـ ID. تأكد من تطابق الأسماء في قاعدة البيانات."}, status=400)

#     try:
#         with transaction.atomic():
#             # 1. تحديث حالة المعاملة
#             DB.query("UPDATE QRTransactions SET status = 'Completed' WHERE id = %s", [tid])
            
#             # 2. تحويل المال للبائع (الآن لدينا الـ ID الحقيقي)
#             User_Service.update_balance(seller_id, amount, 'add')
            
#             # 3. خصم من حساب الوسيط (الأدمن)
#             User_Service.update_balance(1, amount, 'subtract')

#         return Response({"message": "success"})
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)
    
# # 1. جلب بيانات المنتج للمحطة
# @api_view(['GET'])
# def fetch_product_by_id(request, product_id):
#     # نغير fetch_all إلى fetch_one لأننا نريد منتجاً واحداً فقط
#     product = DB.query("""
#         SELECT id, name, status 
#         FROM Products 
#         WHERE id = %s
#     """, [product_id], fetch_one=True) # التعديل هنا

#     if not product:
#         return Response({"error": "المنتج غير موجود في قاعدة البيانات"}, status=404)

#     # ملاحظة: إذا كانت fetch_one تعيد كائن (Object) أو قاموس (Dict) استخدم المفاتيح مباشرة
#     # أما إذا كانت تعيد صف (Tuple) كما هو معتاد في الاستعلامات اليدوية:
#     data = {
#         "id": product[0],       # العنصر الأول هو id
#         "name": product[1],     # العنصر الثاني هو name
#         "destination_city": "دمشق (افتراضية)", 
#         "buyer_id": 5, 
#         "type": "Local"
#     }
#     return Response(data)

# # 2. إرسال الشحنة مع المندوب وإشعار المشتري
# @api_view(['POST'])
# def dispatch_delivery(request):
#     product_id = request.data.get('product_id')
#     buyer_id = request.data.get('buyer_id')
#     car_id = request.data.get('car_id')

#     # 1. تحديث حالة الشحنة
#     # DB.query("UPDATE Shipments SET status = 'Out for Delivery' WHERE product_id = %s", [product_id])

#     # 2. إرسال إشعار للمشتري
#     message = f"📦 طلبك رقم {product_id} في طريقه إليك الآن مع مندوب التوصيل!"
#     DB.query("""
#         INSERT INTO Notifications (user_id, message, created_at) 
#         VALUES (%s, %s, %s)
#     """, [buyer_id, message, timezone.now()])

#     return Response({"message": "تم التسليم للمندوب وإشعار المشتري"})

# # ابحث عن الدالة التي تجلب كل المنتجات للآدمن وقم بتغيير اسمها إلى:
# @api_view(['GET'])
# def get_all_products_admin(request):
#     # الكود الخاص بجلب المنتجات
#     rows = DB.query("""
#         SELECT p.id, p.name, p.price, p.status, p.image_url, u.full_name as seller_name 
#         FROM products p
#         LEFT JOIN users u ON p.seller_id = u.user_id
#     """)
#     return Response([
#         {
#             "id": r[0], "name": r[1], "price": r[2], 
#             "status": r[3], "image_url": r[4], "seller_name": r[5]
#         } for r in rows
#     ])

# @api_view(['POST'])
# def add_new_address(request):
#     user_id = request.data.get('user_id')
#     address_name = request.data.get('name')
#     details = request.data.get('details')

#     if not user_id or not address_name:
#         return Response({"error": "يرجى تزويد معرف المستخدم واسم العنوان"}, status=400)

#     try:
#         DB.query("""
#             INSERT INTO addresses (name, details, user_id) 
#             VALUES (%s, %s, %s)
#         """, [address_name, details, user_id])
#         return Response({"message": "تمت إضافة العنوان بنجاح"})
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

# @api_view(['GET'])
# def get_user_addresses(request, user_id):

#     """جلب كافة العناوين المرتبطة بمستخدم معين"""
#     rows = DB.query("SELECT id, name, details FROM addresses WHERE user_id = %s", [user_id])
#     addresses = [{"id": r[0], "name": r[1], "details": r[2]} for r in rows]
#     return Response(addresses)

from django.db import connection, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.utils import timezone

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
    
class LogisticController(APIView):
    """إدارة المحطات والشحنات وحركتها"""
    def get(self, request, station_id=None):
        if 'trucks' in request.path:
            return Response(DB.execute("SELECT id, plate_number FROM Trucks WHERE status='Available'"))
        
        if station_id: # تفاصيل محطة معينة (شاحنات، منتجات، شحنات)
            data = DB.execute("SELECT * FROM stations WHERE id=%s", [station_id], fetch="one")
            data['trucks'] = DB.execute("SELECT id, plate_number, status FROM trucks WHERE current_station_id=%s", [station_id])
            data['products'] = DB.execute("SELECT id, product_name, quantity FROM station_products WHERE station_id=%s", [station_id])
            data['pending_shipments'] = DB.execute("SELECT s.id, p.name FROM Shipments s JOIN QRTransactions t ON s.transaction_id=t.id JOIN Products p ON t.product_id=p.id WHERE s.current_station_id=%s AND s.status='At Origin Station'", [station_id])
            return Response(data)
        
        return Response(DB.execute("SELECT id, name, city, location_details FROM stations"))

    def post(self, request, action):
        data = request.data
        s_id = data.get('shipment_id', data.get('product_id'))
        
        with transaction.atomic():
            if action == 'receive':
                DB.execute("UPDATE Shipments SET status='At Origin Station', current_station_id=%s WHERE id=%s", [data.get('station_id'), s_id])
                msg = "منتجك تم استلامه في محطتنا!"
            elif action == 'load':
                DB.execute("UPDATE Shipments SET status='In Transit', truck_id=%s WHERE id=%s", [data.get('truck_id'), s_id])
                return Response({"message": "Loaded"})
            elif action == 'unload':
                DB.execute("UPDATE Shipments SET status='At Destination Station', current_station_id=%s, truck_id=NULL WHERE id=%s", [data.get('station_id'), s_id])
                msg = "وصل منتجك إلى محطة مدينتك!"
            elif action == 'dispatch':
                Service.notify(data.get('buyer_id'), f"📦 طلبك رقم {s_id} مع المندوب الآن!")
                return Response({"status": "dispatched"})
            
            # إشعار تلقائي للمشتري في عمليات الاستلام والتفريغ
            buyer = DB.execute("SELECT u.user_id FROM Shipments s JOIN QRTransactions t ON s.transaction_id=t.id JOIN Users u ON t.buyer_id=u.user_id WHERE s.id=%s", [s_id], fetch="one")
            if buyer: Service.notify(buyer['user_id'], msg)
        
        return Response({"status": "success"})

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
    
