from django.shortcuts import render
from django.http import HttpResponse
import Security.algorithm as alg

# Create your views here.
def home(request):
    return render(request, 'Security/index.html')

def start(request):
    return render(request, 'Security/start.html')

def about(request):
    return render(request, 'Security/about.html')

def output(request):
    form = request.POST
    hazardList = alg.scrape(form)
    
    for data in hazardList:
        if (data['hazard']['social'] == []):
            data['hazard']['social'] = ['none']
        if (data['hazard']['credit'] == []):
            data['hazard']['credit'] = ['none']
    
    context = {
        'data': hazardList
    }
    
    return render(request, 'Security/output.html', context)