from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from django.shortcuts import render

from .models import Product


def list_view(request):
    ctx = {'products': Product.objects.all()}
    return render('product_list.html', context=ctx)


def detail_view(request, slug):
    p = Product.objects.get(slug=slug)
    return render('product_detail.html', context={'product': p})
