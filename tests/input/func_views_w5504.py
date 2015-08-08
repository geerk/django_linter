"""Chec for raw access GET and POST dicts"""
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

from .models import Product, Category


def product_list_view(request):
    """product_list_view"""
    if request.is_authenticated():
        ctx = {'products': Product.objects.all(),
               'cat_id': request.GET['cat_id']}
        return render(request, 'product_list.html', context=ctx)
    else:
        return HttpResponseForbidden()


class IndexView(TemplateView):
    """IndexView"""

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        try:
            ctx['cat'] = Category.objects.get(pk=self.request.GET.get('cat_id'))
        except Category.DoesNotExists:
            ctx['cat'] = None
        return ctx
