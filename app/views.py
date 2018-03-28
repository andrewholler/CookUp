from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from app.models import Recipes
from django.shortcuts import render_to_response
from django.shortcuts import redirect
import psycopg2
from psycopg2 import connect
import sys

def index(request):
	print(request.POST.get('email'))
	if (request.method == "POST"):
		return render(request, 'dashboard.html')
	else:
		return render(request, 'index.html')

def register(request):
	# print(request.POST)
	type(request.POST)
	myDict = dict(request.POST)
	# print(myDict)
	if (request.method == "POST"):
		con = None
		con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
		cur = con.cursor()
		print("""INSERT INTO Users (firstname, lastname, username, email, password) VALUES
   						('"""+myDict.get('firstname')[0]+"""','"""+myDict.get('lastname')[0]+"""','"""+myDict.get('username')[0]+"""','"""+myDict.get('email')[0]+"""','"""+myDict.get('password')[0]+"""');""")
		cur.execute("""INSERT INTO Users (firstname, lastname, username, email, password) VALUES
  						('"""+myDict.get('firstname')[0]+"""','"""+myDict.get('lastname')[0]+"""','"""+myDict.get('username')[0]+"""','"""+myDict.get('email')[0]+"""','"""+myDict.get('password')[0]+"""');""")
		con.commit()
		cur.close()
		con.close()
		return render(request, 'dashboard.html')
	else:
		return render(request, 'register.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def profile(request):
	return render(request, 'profile.html')

def submitrecipe(request):
 return render(request, 'submitrecipe.html')

def search(request):
    query = request.GET.get('q')
    if query:
        con = None
        con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
        cur = con.cursor()
        try:
          cur.execute("""SELECT * from recipes
                         WHERE name ILIKE '%""" + str(query) + "%';")
          results = cur.fetchall()
          print(results)
          print(dir(results))
        except Recipes.DoesNotExist:
          results = None
    else:
      results = None
    
    comment = None
    context = RequestContext(request)
    return render_to_response('results.html', {"results": results, "keyword": query}, )

def edit(request):
  query = request.GET.get('q')
  print(query)
  if query:
      con = None
      con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
      cur = con.cursor()
      try:
        cur.execute("""SELECT * from recipes WHERE rid = """ + query + ";")
        results = cur.fetchall()
        print(results)
        print(dir(results))
      except Recipes.DoesNotExist:
        results = None
  comment = None
  context = RequestContext(request)
  return render_to_response('edit.html', {"results": results,}, )

def submitedit(request):
  rid = request.GET.get('rid')
  name = request.GET.get('name')
  appliances = request.GET.get('appliances')
  description = request.GET.get('description')
  videourl = request.GET.get('videourl')
  instructions = request.GET.get('instructions')
  cooktime = request.GET.get('cooktime')
  servings = request.GET.get('servings')
  con = None
  con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
  cur = con.cursor()
  querystring = """UPDATE Recipes
                   SET name = '""" + name + "', appliances='" + appliances + "', description='" + description + "', youtubevid='" + videourl + "', instructions='" + instructions + "' "
  try:
      cooktime = int(cooktime)
  except ValueError:
      cooktime = 0
  querystring += ",cooktime='" + str(cooktime) + "'"
  
  try:
      servings = int(servings)
  except ValueError:
      servings = 'None'
  if servings != 'None':
    querystring += ",servings='" + str(servings) + "'"
  
  querystring += "WHERE rid = """ + rid + ";"
  print(querystring)
  cur.execute(querystring)
  cur.close()
  con.commit()
  con.close()
  
  return redirect(dashboard)

def deleterecipe(request):
  q = request.GET.get('q')
  con = None
  con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
  cur = con.cursor()
  querystring = """DELETE FROM Recipes
                   WHERE rid = """ + q + ";"
  cur.execute(querystring)
  cur.close()
  con.commit()
  con.close()
  return redirect(dashboard)

def addrecipe(request):
  name = request.GET.get('name')
  appliances = request.GET.get('appliances')
  description = request.GET.get('description')
  videourl = request.GET.get('videourl')
  instructions = request.GET.get('instructions')
  cooktime = request.GET.get('cooktime')
  servings = request.GET.get('servings')
  con = None
  con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
  cur = con.cursor()
  querystring = """INSERT INTO Recipes (name, appliances, description, youtubevid, instructions, cooktime, servings) VALUES (
                   '""" + name + "', '" + appliances + "', '" + description + "', '" + videourl + "', '" + instructions + "' "
  try:
      cooktime = int(cooktime)
  except ValueError:
      cooktime = 0
  querystring += ",'" + str(cooktime) + "'"
  try:
      servings = int(servings)
  except ValueError:
      servings = 1
  querystring += ",'" + str(servings) + "'"
  
  querystring += ");"
  print(querystring)
  cur.execute(querystring)
  cur.close()
  con.commit()
  con.close()
  
  return redirect(dashboard)
