from datetime import datetime

from flame_analyzer import DjangoFileFlame

try:
    from django.utils.deprecation import MiddlewareMixin

    class FlameMiddleware(MiddlewareMixin):
        """
        Django Middleware to log flamegraphs to files.
        Requires python manager.py runserver --noreload --nothreading
        """

        def __call__(self, request):
            self.process_request()
            response = self.get_response(request)
            return self.process_response(request, response)

        def process_request(self, request):
            request.flame = DjangoFileFlame(self.file_path(request))
            request.flame.__enter__()

        def process_response(self, request, response):
            if hasattr(request, 'flame'):
                request.flame.__exit__(None, None, None)
            return response

        def file_path(self, request):
            now = datetime.now().strftime(f'%Y-%m-%d-%H:%M:%S')
            path = request.get_full_path().strip('/')
            file_path = f'{now}|{path}'.replace('/', '-')
            file_path += '.svg'
            return file_path


except ImportError:
    FlameMiddleware = None
