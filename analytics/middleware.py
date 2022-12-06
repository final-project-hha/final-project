from django.http import HttpResponse

from analytics.models import Counter


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        counter = Counter.objects.first()
        # Code to be executed before each request
        if not counter:
            counter = Counter.objects.create(name="Members-counter")

        response = self.get_response(request)
        if request.path == '/api/v1/members/':
            counter.counter += 1
            counter.save()
        # Code to be executed after each request/response

        return response
