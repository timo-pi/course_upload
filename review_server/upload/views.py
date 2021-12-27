from django.shortcuts import render
from django.http import HttpResponse
from .models import Course

def home(request):
    # courses = Course.objects.all()
    courses = Course.objects.order_by('-deletion_date')[:5]
    return render(request, 'upload/home.html', {'courses':courses})
