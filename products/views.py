from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .forms import ProductForm
from .models import Product
from .services import get_products_by_category
from django.core.cache import cache


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = 'products_list'
        products = cache.get(cache_key)
        if products is None:
            products = list(Product.objects.all())
            cache.set(cache_key, products, 60)
        return products


@method_decorator(cache_page(60), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        is_owner = product.owner == user
        is_moderator = user.groups.filter(name='Модератор продуктов').exists()
        return is_owner or is_moderator


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        is_owner = product.owner == user
        is_moderator = user.groups.filter(name='Модератор продуктов').exists()
        return is_owner or is_moderator


class ProductTogglePublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.has_perm('products.can_unpublish_product')

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published
        product.save()
        return redirect('product_detail', pk=pk)

class ProductByCategoryView(ListView):
    model = Product
    template_name = 'products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context