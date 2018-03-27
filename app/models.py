from django.db import models


class Ingredient(models.Model):
    iid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    calperounce = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ingredient'


class Recipechanges(models.Model):
    chid = models.AutoField(primary_key=True)
    rid = models.ForeignKey('Recipes', models.DO_NOTHING, blank=True, null=True)
    numvotes = models.IntegerField(blank=True, null=True)
    amounts = models.CharField(max_length=30)
    ingredients = models.CharField(max_length=50)

    class Meta:
        db_table = 'recipechanges'


class Recipecontains(models.Model):
    iid = models.ForeignKey(Ingredient, models.DO_NOTHING, primary_key=True)
    rid = models.ForeignKey('Recipes', models.DO_NOTHING)
    amount = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'recipecontains'
        unique_together = (('iid', 'rid'),)


class Recipes(models.Model):
    rid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    appliances = models.TextField(blank=True, null=True)
    description = models.TextField()
    youtubevid = models.CharField(max_length=11, blank=True, null=True)
    timesrated = models.IntegerField(blank=True, null=True)
    instructions = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    cooktime = models.IntegerField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'recipes'


class Userrecipe(models.Model):
    rid = models.ForeignKey(Recipes, models.DO_NOTHING, primary_key=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'userrecipe'


class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'users'