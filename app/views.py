from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	print(request.POST.get('email'))
	if (request.method == "POST"):
		return render(request, 'dashboard.html')
	else:
		return render(request, 'index.html')

def register(request):
	print(request.POST)
	if (request.method == "POST"):
		return render(request, 'dashboard.html')
	else:
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