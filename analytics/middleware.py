from django.http import HttpResponse

from analytics.models import Counter


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        counter = Counter.objects.get(pk=4)
        # Code to be executed for each request before

        response = self.get_response(request)
        if request.path == '/api/v1/members/':
            counter.counter += 1
            counter.save()
        # Code to be executed for each request/response after

        return response
