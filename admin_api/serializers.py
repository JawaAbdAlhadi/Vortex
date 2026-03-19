from rest_framework import serializers
from .models import Users, SellerRequests

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class SellerRequestSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True) # لجلب اسم المستخدم مع الطلب
    class Meta:
        model = SellerRequests
        fields = '__all__'