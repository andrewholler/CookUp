from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from app.models import Recipes
from django.shortcuts import render_to_response
import psycopg2
from psycopg2 import connect
import sys

# Create your views here.
def index(request):
	return render(request, 'index.html')

def register(request):
	return render(request, 'register.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def profile(request):
	return render(request, 'profile.html')

def submitrecipe(request):
 return render(request, 'submitrecipe.html')

def search(request):
    query = request.GET.get('q')
    try:
        query = int(query)
    except ValueError:
        query = None
        results = None
    print(query)
    if query:
        con = None
        con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
        cur = con.cursor()
        try:
          cur.execute("""SELECT * from recipes WHERE rid = """ + str(query) + ";")
          results = cur.fetchall()
          print(results)
          print(dir(results))
        except Recipes.DoesNotExist:
          results = None
    comment = None
    context = RequestContext(request)
    return render_to_response('results.html', {"results": results,}, )

'''def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})'''