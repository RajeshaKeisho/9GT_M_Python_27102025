from typing import Any
from django.shortcuts import render
from .models import Product
from django.db.models import Q
from .serializers import ProductSerializer
from .filters import ProductFilter
import django_filters
from django.views.generic import ListView
from rest_framework import generics, filters

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [ django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    ]

    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['name']


class ProductListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = ProductFilter(self.request.GET, queryset=queryset)
        queryset = self.filter.qs

        # 🔍 Handle search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # 🧭 Handle ordering
        ordering = self.request.GET.get('ordering', 'name')
        queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        # 👇 Pass the search term back to the template so it stays in the input box
        context['search_query'] = self.request.GET.get('q', '')
        return context
