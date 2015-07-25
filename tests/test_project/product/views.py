from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from django.shortcuts import render
from django.http import HttpResponseForbidden

import test_project.settings
from .models import Product


def list_view(request):
    if request.is_authenticated():
        ctx = {'products': Product.objects.all()}
        return render('product_list.html', context=ctx)
    else:
        return HttpResponseForbidden()


def detail_view(request, slug):
    if request.is_authenticated:
        p = Product.objects.get(slug=slug)
        return render('product_detail.html', context={'product': p})
    else:
        return HttpResponseForbidden()
