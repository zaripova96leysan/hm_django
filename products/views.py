from django.shortcuts import get_object_or_404, redirect, render

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

