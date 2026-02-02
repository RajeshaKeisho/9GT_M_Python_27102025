from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products-viewset', views.ProductViewSet, basename='product-viewset')

urlpatterns = [
    # Auth endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Product endpoints
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Order endpoints
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    
    # User endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('groups/', views.UserGroupListView.as_view(), name='group-list'),
    
    # Special endpoints
    path('sensitive/', views.SensitiveOperationView.as_view(), name='sensitive-operation'),
    path('public/', views.PublicDataView.as_view(), name='public-data'),
    
    # Function-based views
    path('health/', views.health_check, name='health-check'),
    path('bulk-products/', views.bulk_create_products, name='bulk-create-products'),
    
    # Include router URLs
    path('', include(router.urls)),
]