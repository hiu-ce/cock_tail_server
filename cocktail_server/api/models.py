from django.db import models
# from api.validators import check_amount_int

class Glass(models.Model): # 서빙 글라스 모델
    name = models.CharField(primary_key = True,max_length=255)

    def __str__(self):
        return self.name

class Cocktail(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    recipe = models.TextField()
    img_url = models.URLField()
    glass = models.ForeignKey(Glass, on_delete=models.CASCADE, null=True, related_name = 'cocktail')
    
    def __str__(self):
        return self.name
    
class Base(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    alcohol_degree = models.FloatField(default = 0.0)
    cocktail = models.ManyToManyField(Cocktail,through = 'CocktailBase',related_name = 'base')
    
    def __str__(self):
        return self.name
    
class Sub(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    alcohol_degree = models.FloatField(default = 0.0)
    cocktail = models.ManyToManyField(Cocktail,through = 'CocktailSub',related_name = 'sub')
    
class Juice(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    cocktail = models.ManyToManyField(Cocktail,through = 'CocktailJuice',related_name = 'juice')
    
class Other(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    cocktail = models.ManyToManyField(Cocktail,through = 'CocktailOther',related_name = 'other')
    
class CocktailBase(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_base')
    name = models.ForeignKey(Base, on_delete=models.CASCADE, related_name = 'cocktail_base') # base-name
    amount = models.FloatField(default = 0.0)
    
class CocktailSub(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_sub')
    name = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name = 'cocktail_sub') # sub-name
    amount = models.FloatField(default = 0.0)

class CocktailJuice(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_juice')
    name = models.ForeignKey(Juice, on_delete=models.CASCADE, related_name = 'cocktail_juice') # juice-name
    amount = models.FloatField(default = 0.0)
    
class CocktailOther(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_other')
    name = models.ForeignKey(Other, on_delete=models.CASCADE, related_name = 'cocktail_other') # other-name
    amount = models.CharField(max_length = 50, blank = True)
    
class TodayDrink(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name ='today_drink')