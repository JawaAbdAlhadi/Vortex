from django.db import models

class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return self.role_name


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=150)
    password_hash = models.CharField(max_length=255)
    # ربط الـ role_id كـ ForeignKey بدلاً من Integer لمزيد من القوة في البيانات
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, db_column='role_id', blank=True, null=True)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.full_name


class Permissions(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'permissions'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='seller_id', blank=True, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # استخدام BooleanField أو IntegerField حسب رغبتك، هنا أبقيتها متوافقة مع طلبك
    is_approved = models.IntegerField(default=0, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'products'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders_as_buyer', db_column='buyer_id', blank=True, null=True)
    seller = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders_as_seller', db_column='seller_id', blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, db_column='product_id', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code_token = models.CharField(unique=True, max_length=255)
    order_status = models.CharField(max_length=20, default='pending', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'orders'


class SellerRequests(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', blank=True, null=True)
    store_name = models.CharField(max_length=100, blank=True, null=True)
    store_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'seller_requests'