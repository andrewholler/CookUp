from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'index.html')

def register(request):
	return render(request, 'register.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def profile(request):
	return render(request, 'profile.html')

'''def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})'''