from django.urls import path
from .views import ProductList, ProductListView

urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('products-lists/', ProductListView.as_view(), name='product-list'),
]
