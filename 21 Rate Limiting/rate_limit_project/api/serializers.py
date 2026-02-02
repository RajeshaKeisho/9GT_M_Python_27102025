from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserGroup, Product, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    rate_limit_tier = serializers.CharField(source='group.rate_limit_tier', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'group', 'group_name', 'rate_limit_tier', 'bio']
        read_only_fields = ['id']

class UserGroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserGroup
        fields = ['id', 'name', 'description', 'rate_limit_tier', 'member_count']
    
    def get_member_count(self, obj):
        return obj.userprofile_set.count()

class ProductSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_stock', 'created_at', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'user', 'username', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at', 'total_price']
    
    def create(self, validated_data):
        # Calculate total price
        product = validated_data['product']
        quantity = validated_data['quantity']
        validated_data['total_price'] = product.price * quantity
        return super().create(validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    bio = serializers.CharField(write_only=True, required=False, allow_blank=True)
    group_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'bio', 'group_id']
    
    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        group_id = validated_data.pop('group_id', None)
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # Create profile
        profile = UserProfile.objects.create(user=user, bio=bio)
        
        # Assign group if provided
        if group_id:
            try:
                group = UserGroup.objects.get(id=group_id)
                profile.group = group
                profile.save()
            except UserGroup.DoesNotExist:
                pass
        
        return user