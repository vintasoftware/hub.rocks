def get_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    splitted_auth_header = auth_header.split(' ')
    
    if len(splitted_auth_header):
        __, token = splitted_auth_header
    else:
        token = None
    
    return token
