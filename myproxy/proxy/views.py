import requests

from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy(request, url):
     origin_url = f"{settings.ORIGIN}/{path}"
    