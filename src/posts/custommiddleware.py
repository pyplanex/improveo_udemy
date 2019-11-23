from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.http import Http404


class CustomMiddlewareExample(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = resolve(request.path).url_name
        if not ip == '127.0.0.1' and path == 'post-list':
            raise Http404("No acess for you")
        else:
            print('this path is ok')
            return None
