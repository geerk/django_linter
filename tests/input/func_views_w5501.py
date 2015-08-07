"""
Check for calling is_authenticated instead of using it as attribute
"""


def product_create(request):
    """product_create"""
    if request.user.is_authenticated:
        #  create user
        pass
