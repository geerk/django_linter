from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import MultipleObjectsReturned
from django.views.generic import TemplateView

import test_project.settings
from .models import Product, Category


def product_list_view(request):
    if request.is_authenticated():
        ctx = {'products': Product.objects.all(),
               'categories_count': len(Category.objects.all()),
               'cat_id': request.GET['cat_id']}
        return render('product_list.html', context=ctx)
    else:
        return HttpResponseForbidden()


def product_detail_view(request, slug):
    if request.is_authenticated:
        try:
            p = Product.objects.get(slug=slug)
        except MultipleObjectsReturned:
            return HttpResponseNotFound()
        return render('product_detail.html', context={'product': p})
    else:
        return HttpResponseForbidden()


def category_detail_view(request, pk):
    try:
        p = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponseNotFound()
    return render('product_detail.html', context={'product': p})


class IndexView(TemplateView):

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['cat'] = Category.objects.get(pk=self.request.GET.get('cat_id'))
        return ctx
