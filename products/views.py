from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ProductForm
from .models import Product



class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


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