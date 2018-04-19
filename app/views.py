from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from app.models import Recipes
from app.forms import SignUpForm
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import psycopg2
from psycopg2 import connect
import sys


def register(request):
  type(request.POST)
  myDict = dict(request.POST)
  if (request.method == "POST"):
    '''con = None
    con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
    cur = con.cursor()
    print("""INSERT INTO Users (firstname, lastname, username, email, password) VALUES
           ('"""+myDict.get('firstname')[0]+"""','"""+myDict.get('lastname')[0]+"""','"""+myDict.get('username')[0]+"""','"""+myDict.get('email')[0]+"""','"""+myDict.get('password')[0]+"""');""")
    cur.execute("""INSERT INTO Users (firstname, lastname, username, email, password) VALUES
          ('"""+myDict.get('firstname')[0]+"""','"""+myDict.get('lastname')[0]+"""','"""+myDict.get('username')[0]+"""','"""+myDict.get('email')[0]+"""','"""+myDict.get('password')[0]+"""');""")
    con.commit()
    cur.close()
    con.close()
    return render(request, 'dashboard.html')'''
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('login')
  else:
		  form = SignUpForm()
  return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
	return render(request, 'dashboard.html')

@login_required
def profile(request):
  username = None
  if request.user.is_authenticated:
    username = request.user.username
  con = None
  con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
  cur = con.cursor()
  cur.execute(""" SELECT avg(Recipes.rating) 
                  FROM ((Userrecipe
                    INNER JOIN auth_user ON Userrecipe.uid_id = auth_user.id)
                    INNER JOIN Recipes ON Userrecipe.rid_id = recipes.rid)
                  WHERE Userrecipe.uid_id = """ + str(request.user.id) + ";")
  user_rating = cur.fetchall()[0][0]
  if user_rating == None:
    user_rating = 0.0
  cur.close()
  con.close()
  return render(request, 'profile.html', {"rating": "%.2f" % user_rating})

@login_required
def submitrecipe(request):
 return render(request, 'submitrecipe.html')

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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
