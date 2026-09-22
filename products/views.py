from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .forms import ProductForm
from .models import Product


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "product_form.html", {"form": form})

class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')