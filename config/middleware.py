from django.http import JsonResponse
from users.models import CustomUser
from utils import decode_jwt

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        request.user = None

        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
            user_id = decode_jwt(token)
            if user_id:
                try:
                    user = CustomUser.objects.get(id=user_id, is_active=True)
                    request.user = user
                except CustomUser.DoesNotExist:
                    pass

        response = self.get_response(request)
        return response