import requests
from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def proxy(request, path):
    print(f"Proxying request from {request.get_full_path()} to {settings.ORIGIN}/{path}")
    origin_url = f"{settings.ORIGIN}/{path}"
    cache_key = request.get_full_path()
    cached_response = cache.get(cache_key)
    if cached_response:
        print(f"Response found in cache for {cache_key}")
        response_body, response_status, response_headers = cached_response
        print(f"Response headers: {response_headers}")
        response_headers['X-Cache'] = 'HIT'
        print("Sending cached response")
       
        
        return HttpResponse(response_body, status=response_status, headers=response_headers)
    
    
    try:
        print(f"Forwarding request to {origin_url}")
        response = requests.request(
            method=request.method,
            url=origin_url,
            headers={key: value for key, value in request.headers.items() if key.lower() not in ['host', 'connection']},
            data=request.body,
            allow_redirects=False,
        )
       
        response_headers = dict(response.headers)
      
        response_headers.pop('Connection', None)
        response_headers.pop('Keep-Alive', None)
        response_headers.pop('Proxy-Authenticate', None)
        response_headers.pop('Proxy-Authorization', None)
        
        print(f"Response headers: {response_headers}")
        
        cache_data = (response.content, response.status_code, response_headers)
        cache.set(cache_key, cache_data)
        
        response_headers['X-Cache'] = 'MISS'
        print(f"Stored response in cache for {cache_key}")
        

        return HttpResponse(response.content, status=response.status_code, headers=response_headers)
    except requests.RequestException as e:
        print(f"Error forwarding request: {e}")
       
        return HttpResponse("Internal Server Error", status=500)

@csrf_exempt
def clear_cache(request):
    cache.clear()  
    return HttpResponse("Cache cleared", status=200)
