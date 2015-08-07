"""
Check for calling is_authenticated instead of using it as attribute
"""
from django.views.generic import UpdateView


def product_create(request):
    """product_create"""
    if request.user.is_authenticated:
        #  create user
        pass


class ProductUpdateView(UpdateView):
    """ProductUpdateView"""

    def post(self, *args, **kwargs):
        """post"""
        if self.request.user.is_authenticated:
            #  update user
            pass
