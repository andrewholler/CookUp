from django.shortcuts import render
from django.http import HttpResponse

import psycopg2
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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
