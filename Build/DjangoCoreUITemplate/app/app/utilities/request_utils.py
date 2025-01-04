# app/utilities/request_utils.py

def is_ajax(request):
    """
    Check if a request is AJAX
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
