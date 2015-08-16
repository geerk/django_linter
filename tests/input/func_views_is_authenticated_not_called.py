"""
Check for calling is_authenticated instead of using it as attribute
"""
from django.views.generic import UpdateView


def product_create(request):
    if request.user.is_authenticated:
        #  create user
        pass


class ProductUpdateView(UpdateView):

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            #  update user
            pass
