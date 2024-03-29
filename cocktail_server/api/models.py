from django.db import models

from api.validators import check_amount_int

class Cocktail(models.Model):
    cocktail_name = models.CharField(max_length=30, primary_key=True)
    ddabong = models.IntegerField(default=0)
    recipe = models.CharField(max_length=400, default="")
    img_url = models.URLField(max_length=300, default="", blank=True)

    base = models.JSONField(null = True, blank = True, validators = [check_amount_int])
    sub = models.JSONField(null = True, blank = True, validators = [check_amount_int])
    juice = models.JSONField(null = True, blank = True, validators = [check_amount_int])
    other = models.JSONField(null = True, blank = True)
    
class Base(models.Model):
    drink_name = models.CharField(max_length=30,primary_key=True)
    cocktails = models.ManyToManyField(Cocktail,related_name='base_cocktail')
    alcohol_degree = models.FloatField(null=True)
class Sub(models.Model):
    drink_name = models.CharField(max_length=30)
    cocktails = models.ManyToManyField(Cocktail,related_name = 'sub_cocktail')
    alcohol_degree = models.FloatField(null=True)
class Juice(models.Model):
    drink_name = models.CharField(max_length=30)
    cocktails = models.ManyToManyField(Cocktail, related_name='juice_cocktail')
class Other(models.Model):
    name = models.CharField(max_length=30)
    cocktails = models.ManyToManyField(Cocktail,related_name='other_cocktail')

class TodayDrink(models.Model):
    drink_name = models.ForeignKey(Cocktail, on_delete=models.CASCADE, db_column= 'today_drink')