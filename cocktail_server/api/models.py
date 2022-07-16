from django.db import models

class Cocktail(models.Model):
    cocktail_name = models.CharField(max_length=30, primary_key=True)
    ddabong = models.IntegerField(default=0)
    recipe = models.CharField(max_length=200, default="")

    base = models.JSONField(null = True, blank = True)
    sub = models.JSONField(null = True, blank = True)
    juice = models.JSONField(null = True, blank = True)
    other = models.JSONField(null = True, blank = True)
    
class Base(models.Model):
    drink_name = models.CharField(max_length=30,primary_key=True)
    cocktails = models.ManyToManyField(Cocktail,related_name='base_cocktail')
class Sub(models.Model):
    drink_name = models.CharField(max_length=30)
    cocktails = models.ManyToManyField(Cocktail,related_name = 'sub_cocktail')
class Juice(models.Model):
    drink_name = models.CharField(max_length=30)
    cocktails = models.ManyToManyField(Cocktail, related_name='juice_cocktail')
class Other(models.Model):
    name = models.CharField(max_length=30)
    cocktails = models.ManyToManyField(Cocktail,related_name='other_cocktail')