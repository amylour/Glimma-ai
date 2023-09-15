
from django.shortcuts import render, HttpResponse



def index(request):
    return render(request, 'GLIMMA_AI/index.html')