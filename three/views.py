# three/views.py

from django.shortcuts import render

def three_view(request):
    return render(request, 'three/three.html')
