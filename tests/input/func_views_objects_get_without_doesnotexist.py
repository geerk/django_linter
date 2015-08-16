"""
Check calling objects.get inside try-except
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import MultipleObjectsReturned
from django.views.generic import TemplateView

from .models import Product, Category


def product_list_view(request, cat_id):
    if request.is_authenticated():
        ctx = {'products': Product.objects.all(),
               'cat_id': cat_id}
        return render(request, 'product_list.html', context=ctx)
    else:
        return HttpResponseForbidden()


def product_detail_view(request, slug):
    if request.is_authenticated:
        try:
            product = Product.objects.get(slug=slug)
        except MultipleObjectsReturned:
            return HttpResponseNotFound()
        return render(
            request, 'product_detail.html', context={'product': product})
    else:
        return HttpResponseForbidden()


def category_detail_view(request, **kwargs):
    try:
        category = Category.objects.get(pk=kwargs['pk'])
    except Category.DoesNotExist:
        return HttpResponseNotFound()
    return render(
        request, 'category_detail.html', context={'category': category})


class IndexView(TemplateView):

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['cat'] = Category.objects.get(pk=kwargs['cat_id'])
        return ctx
