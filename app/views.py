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
    
  recipes = None
  cur.execute("""SELECT * FROM recipes, userrecipe
                 WHERE uid_id=""" + str(request.user.id) + """ AND rid_id=rid;""")
  recipes = cur.fetchall()
  
  for i, recipe in enumerate(recipes):
    rid = recipe[0]
    cur.execute("""select quantity, measure, name
                   from recipecontains, ingredient
                   where rid_id='""" + str(rid) + """' and iid_id = iid;""")
    recipes[i] = recipes[i], tuple(cur.fetchall())
  
  cur.close()
  con.close()
  return render(request, 'profile.html', {"rating": "%.2f" % user_rating, "recipes": recipes})

@login_required
def submitrecipe(request):
 return render(request, 'submitrecipe.html')

@login_required
def search(request):
    keyword = request.GET.get('q')
    maxcalories = request.GET.get('cal')
    ingredient = request.GET.get('ingr')
    user = request.GET.get('user')
    if keyword or maxcalories or ingredient or user:
        con = None
        con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
        cur = con.cursor()
        try:
          querystring = """SELECT * from recipes
                         WHERE 1=1"""
          if keyword:
            querystring += """ AND name ILIKE '%""" + str(keyword) + "%'"
          if maxcalories:
            querystring += """ AND calories <= """ + str(maxcalories)
          if ingredient:
            querystring += """ INTERSECT SELECT * from recipes WHERE rid IN (SELECT rid_id FROM recipecontains, ingredient WHERE (ingredient.name ILIKE '%""" + ingredient + """%' OR recipecontains.measure ILIKE '%"""+ ingredient +"""%') AND ingredient.iid = recipecontains.iid_id)"""
          if user:
            querystring += """ INTERSECT SELECT * from recipes WHERE rid IN (SELECT rid FROM recipes, userrecipe, auth_user WHERE rid=rid_id AND uid_id=id AND username='"""+ user +"""')"""
          querystring += ";"
          print(querystring)
          cur.execute(querystring)
          results = cur.fetchall()
          
          for i, result in enumerate(results):
            rid = result[0]
            cur.execute("""select quantity, measure, name
                           from recipecontains, ingredient
                           where rid_id='""" + str(rid) + """' and iid_id = iid;""")
            results[i] = results[i], tuple(cur.fetchall())
        except Recipes.DoesNotExist:
          results = None
    else:
      results = None
    
    comment = None
    context = RequestContext(request)
    return render_to_response('results.html', {"results": results, "keyword": keyword, "maxcalories": maxcalories, "ingredient": ingredient}, )

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
  calories = request.GET.get('calories')
  con = None
  con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
  cur = con.cursor()
  querystring = """UPDATE Recipes
                   SET name = '""" + name + "', appliances='" + appliances + "', description='" + description + "', youtubevid='" + videourl + "', instructions='" + instructions + "', calories='" + calories + "' "
  try:
      cooktime = int(cooktime)
  except ValueError:
      cooktime = 0
  querystring += ",cooktime='" + str(cooktime) + "'"
  print(querystring)
  
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
  calories = request.GET.get('calories')
  con = None
  con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
  cur = con.cursor()
  querystring = """INSERT INTO Recipes (name, appliances, description, youtubevid, instructions, calories, cooktime, servings) VALUES (
                   '""" + name + "', '" + appliances + "', '" + description + "', '" + videourl + "', '" + instructions + "', '" + calories + "' "
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
  querystring += ") RETURNING rid;"
  cur.execute(querystring)
  
  rid = cur.fetchall()[0][0]
  ingredients = request.GET.getlist("ingredient")
  ingredientAmounts = request.GET.getlist("ingredient-amount")
  ingredientMeasures = request.GET.getlist("ingredient-measure")
  
  for i, ingredient in enumerate(ingredients):
    print(i, ingredient)
    ingredient = ingredient.replace("'", "")
    ingredient = ingredient.replace('"', "")
    ingredient_exists_query = """SELECT EXISTS(SELECT 1 FROM ingredient WHERE name='""" + ingredient + """');"""
    cur.execute(ingredient_exists_query)
    iid = 0
    if not cur.fetchall()[0][0]:
      ingredient_insert_query = """INSERT INTO ingredient (name) VALUES ('""" + ingredient + """')
                                   RETURNING iid;"""
      cur.execute(ingredient_insert_query)
      iid = cur.fetchall()[0][0]
    else:
      get_ingredient_iid_query = """SELECT iid FROM ingredient WHERE name='""" + ingredient + """';"""
      cur.execute(get_ingredient_iid_query)
      iid = cur.fetchall()[0][0]
    recipecontains_query = """INSERT INTO recipecontains (iid_id, rid_id, quantity, measure)
                              VALUES ('"""+str(iid)+"""', '"""+str(rid)+"""', '"""+str(ingredientAmounts[i])+"""', '"""+ingredientMeasures[i]+"""');"""
    cur.execute(recipecontains_query)
  
  userrecipe_query = """INSERT INTO userrecipe (rid_id, uid_id)
                        VALUES ('""" + str(rid) + """', '""" + str(request.user.id) + """');"""
  cur.execute(userrecipe_query)
  
  cur.close()
  con.commit()
  con.close()
  return redirect(dashboard)
