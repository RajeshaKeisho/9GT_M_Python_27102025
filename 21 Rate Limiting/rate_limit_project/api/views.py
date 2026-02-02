from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, throttle_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Product, Order, UserProfile, UserGroup
from .serializers import (
    ProductSerializer, OrderSerializer, 
    UserSerializer, UserProfileSerializer,
    UserGroupSerializer, RegisterSerializer
)
from .throttles import (
    AnonRateThrottleCustom, UserRateThrottleCustom,
    GroupBasedThrottle, ScopedEndpointThrottle,
    CombinedThrottle
)
from .permissions import IsOwnerOrReadOnly, GroupBasedPermission, PremiumProductPermission

# ============ AUTH VIEWS ============

class RegisterView(generics.CreateAPIView):
    """User registration with rate limiting"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    throttle_classes = [AnonRateThrottleCustom]  # Prevent registration spam
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return user data with token
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    """Custom token authentication with rate limiting"""
    throttle_classes = [AnonRateThrottleCustom]  # Prevent brute force
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })

class LogoutView(APIView):
    """Logout view - invalidate token"""
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottleCustom]
    
    def post(self, request):
        try:
            # Delete the token
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)

# ============ PRODUCT VIEWS ============

class ProductListView(generics.ListCreateAPIView):
    """List and create products with different throttling"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Different throttles for different methods
    def get_throttles(self):
        if self.request.method == 'GET':
            # Anonymous users have stricter limits
            if not self.request.user.is_authenticated:
                return [AnonRateThrottleCustom()]
            else:
                return [UserRateThrottleCustom(), GroupBasedThrottle()]
        else:  # POST
            # Stricter limits for creating products
            return [UserRateThrottleCustom(), GroupBasedThrottle()]
    
    # Set throttle scope for ScopedEndpointThrottle
    throttle_scope = 'product_list'
    
    def perform_create(self, serializer):
        # Set the creator to the current user
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering options
        name = self.request.query_params.get('name', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        in_stock = self.request.query_params.get('in_stock', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if in_stock:
            queryset = queryset.filter(in_stock=(in_stock.lower() == 'true'))
        
        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Product detail with owner permissions"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottleCustom, GroupBasedThrottle]
    throttle_scope = 'product_detail'

# ============ ORDER VIEWS ============

class OrderListView(generics.ListCreateAPIView):
    """Order operations with strict throttling"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, GroupBasedPermission]
    
    # Very strict throttling for order creation
    def get_throttles(self):
        if self.request.method == 'GET':
            return [UserRateThrottleCustom(), GroupBasedThrottle()]
        else:  # POST
            # Combined throttle with scoped endpoint throttle
            return [
                UserRateThrottleCustom(),
                GroupBasedThrottle(),
                ScopedEndpointThrottle()
            ]
    
    # Set scope for order creation
    throttle_scope = 'order_create'
    
    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Set the user to the current user
        serializer.save(user=self.request.user)

# ============ USER PROFILE VIEWS ============

class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile management"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottleCustom]
    
    def get_object(self):
        # Get or create profile for the user
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

# ============ USER GROUP VIEWS ============

class UserGroupListView(generics.ListAPIView):
    """List user groups (admin only)"""
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [UserRateThrottleCustom]

# ============ SPECIAL VIEWS WITH CUSTOM THROTTLING ============

class SensitiveOperationView(APIView):
    """View with very strict rate limiting for sensitive operations"""
    permission_classes = [permissions.IsAuthenticated]
    
    # Use combined throttling
    throttle_classes = [
        UserRateThrottleCustom,
        GroupBasedThrottle,
        ScopedEndpointThrottle
    ]
    
    throttle_scope = 'sensitive'  # Very strict limit
    
    def get(self, request):
        # Simulate a sensitive operation
        return Response({
            'message': 'Sensitive operation performed',
            'user': request.user.username,
            'timestamp': request.data.get('timestamp', 'N/A')
        })
    
    def post(self, request):
        # Another sensitive operation
        return Response({
            'message': 'Data processed successfully',
            'data': request.data
        }, status=status.HTTP_201_CREATED)

class PublicDataView(APIView):
    """Public data with anonymous rate limiting"""
    throttle_classes = [AnonRateThrottleCustom]
    
    def get(self, request):
        # Public data accessible to everyone
        public_products = Product.objects.filter(in_stock=True)[:5]
        serializer = ProductSerializer(public_products, many=True)
        
        return Response({
            'message': 'Public product data',
            'products': serializer.data,
            'product_count': Product.objects.count()
        })

# ============ VIEWSET EXAMPLE ============

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet example with rate limiting"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_throttles(self):
        # Different throttling based on action
        if self.action == 'list':
            return [AnonRateThrottleCustom()]
        elif self.action == 'create':
            return [UserRateThrottleCustom(), GroupBasedThrottle()]
        else:
            return [UserRateThrottleCustom()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], throttle_classes=[UserRateThrottleCustom])
    def duplicate(self, request, pk=None):
        """Duplicate a product (special action with its own throttle)"""
        product = self.get_object()
        new_product = Product.objects.create(
            name=f"{product.name} (Copy)",
            description=product.description,
            price=product.price,
            in_stock=product.in_stock,
            created_by=request.user
        )
        serializer = self.get_serializer(new_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ============ FUNCTION-BASED VIEW EXAMPLE ============

@api_view(['GET'])
@throttle_classes([AnonRateThrottleCustom])
def health_check(request):
    """Health check endpoint with rate limiting"""
    return Response({
        'status': 'healthy',
        'timestamp': 'current_time',
        'service': 'Rate Limit API'
    })

@api_view(['POST'])
@throttle_classes([UserRateThrottleCustom, GroupBasedThrottle])
def bulk_create_products(request):
    """Bulk create products with rate limiting"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    products_data = request.data.get('products', [])
    created_products = []
    
    for product_data in products_data:
        product_data['created_by'] = request.user.id
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            created_products.append(serializer.data)
    
    return Response({
        'created': len(created_products),
        'products': created_products
    }, status=status.HTTP_201_CREATED)