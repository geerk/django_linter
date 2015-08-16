"""Check for uneffecient query to get number of objects using len"""
from django.shortcuts import render
from django.http import HttpResponseForbidden

from .models import Product, Category


def product_list_view(request):
    if request.is_authenticated():
        ctx = {'products': Product.objects.all(),
               'categories_count': len(Category.objects.all())}
        return render(request, 'product_list.html', context=ctx)
    else:
        return HttpResponseForbidden()
