from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    if request.method == 'POST':
        selected_date = request.POST.get('date-input', '')
        return HttpResponseRedirect(reverse('two', args=[selected_date]))

    return render(request, 'home/home.html')



