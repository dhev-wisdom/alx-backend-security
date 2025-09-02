from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from .utils import user_based_rate_limit

# Create your views here.
@csrf_exempt
@user_based_rate_limit
# @ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "invalid credentials"}, status=401)
    return JsonResponse({"error": "POST required"}, status=405)