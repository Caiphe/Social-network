from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def home_view(request):
  user = request.user
  hello = 'hello social'
  
  context = {
    'user_t': user
  }
  
  return render(request, 'main/home.html', context)