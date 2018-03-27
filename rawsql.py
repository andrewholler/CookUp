import psycopg2
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = None
con = connect(user='fyrxqvffutzuth', host='ec2-174-129-26-203.compute-1.amazonaws.com', password='81fd164e25fc7569030612fa5a67d1460e534db4289aeef761114c6746429d9b', dbname='d1au6je7k25ijn', port='5432')
cur = con.cursor()

'''
cur.execute("""INSERT INTO ingredient (name) VALUES
  ('cornstarch'),
  ('cold water'),
  ('white sugar'),
  ('soy sauce'),
  ('cider vinegar'),
  ('clove garlic, minced'),
  ('ground ginger'),
  ('ground black pepper'),
  ('skinless chicken thighs');
""")
'''
'''
cur.execute("""INSERT INTO recipes (name, appliances, description, instructions, rating, cooktime, servings) VALUES
  ('Baked Teriyaki Chicken', 'saucepan,baking dish,oven,brush', 'A much requested chicken recipe! Easy to double for a large group. Delicious!', 'In a small saucepan over low heat, combine the cornstarch, cold water, sugar, soy sauce, vinegar, garlic, ginger and ground black pepper. Let simmer, stirring frequently, until sauce thickens and bubbles.%%%Preheat oven to 425 degrees F (220 degrees C).%%%Place chicken pieces in a lightly greased 9x13 inch baking dish. Brush chicken with the sauce. Turn pieces over, and brush again.%%%Bake in the preheated oven for 30 minutes. Turn pieces over, and bake for another 30 minutes, until no longer pink and juices run clear. Brush with sauce every 10 minutes during cooking.', 4.5, 60, 6);
""")
'''

cur.execute("""INSERT INTO recipecontains (iid_id, rid_id, amount) VALUES
  (1,1,'1 tablespoon'),
  (2,1,'1 tablespoon'),
  (3,1,'1/2 cup'),
  (4,1,'1/2 cup'),
  (5,1,'1/4 cup'),
  (6,1,'1'),
  (7,1,'1/2 teaspoon'),
  (8,1,'1/4 teaspoon'),
  (9,1,'12');
  """)

'''
cur.execute("""CREATE TABLE Ingredient (
	IID		serial,
	name		varchar(30) NOT NULL,
	calperounce	integer,
	PRIMARY KEY (IID) );

CREATE TABLE Recipes (
	RID		serial,
	name		varchar(30) NOT NULL,
	appliances	text,
	description	text NOT NULL,
	youtubevid	char(11),
	timesrated	integer DEFAULT 0,
	instructions	text NOT NULL,
	rating		integer DEFAULT 0,
	cooktime	integer DEFAULT 0,
	servings	integer DEFAULT 1,
	PRIMARY KEY (RID) );

CREATE TABLE RecipeContains(
	IID	integer,
	RID	integer,
        amount  varchar(30),
	PRIMARY KEY (IID, RID),
	FOREIGN KEY (IID) REFERENCES Ingredient (IID),
	FOREIGN KEY (RID) REFERENCES Recipes (RID) );

CREATE TABLE Users (
	UID		serial,
	firstname	varchar(30),
	lastname	varchar(30),
	username	varchar(20) NOT NULL,
	email		varchar(40) NOT NULL,
	password	varchar(30) NOT NULL,
	rating		integer DEFAULT 0,
	PRIMARY KEY (UID) );

CREATE TABLE UserRecipe (
	RID		serial,
	UID		integer,
	PRIMARY KEY (RID),
	FOREIGN KEY (RID) REFERENCES Recipes (RID),
	FOREIGN KEY (UID) REFERENCES Users (UID) );

CREATE TABLE RecipeChanges (
	CHID		serial,
	RID		integer,
	numvotes	integer DEFAULT 0,
	amounts		varchar(30) NOT NULL,
	ingredients	varchar(50) NOT NULL,
	PRIMARY KEY (CHID),
	FOREIGN KEY (RID) REFERENCES Recipes (RID) );""")
'''
'''
cur.execute("""INSERT INTO test_table VALUES ('doggy', 'What I Do Is My Own Business', 59)""")
'''
'''
cur.execute("""SELECT ingredient.name
                FROM recipecontains, ingredient, recipes
                WHERE iid = iid_id AND rid_id = rid;""")
'''

cur.close()
con.commit()
con.close()
