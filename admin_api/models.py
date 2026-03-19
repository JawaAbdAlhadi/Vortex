# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    seller = models.ForeignKey('Users', models.DO_NOTHING, related_name='orders_seller_set', blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code_token = models.CharField(unique=True, max_length=255)
    order_status = models.CharField(max_length=9, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orders'


class Permissions(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'permissions'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_approved = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'products'


class RolePermissions(models.Model):
    pk = models.CompositePrimaryKey('role_id', 'permission_id')
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'role_permissions'


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'roles'


class SellerRequests(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    store_name = models.CharField(max_length=100, blank=True, null=True)
    store_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    request_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'seller_requests'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password_hash = models.CharField(max_length=255)
    role_id = models.IntegerField(blank=True, null=True)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'
