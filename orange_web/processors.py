"""Here we define custom processors for orange_web"""


def get_current_page(request):
    """
    :param request: Django request object
    :return: Requested page name as defined in views.py
    """
    return {
        'current_page': request.get_full_path().split('/')[1]
    }
