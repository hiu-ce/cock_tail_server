from django.db import models
# from api.validators import check_amount_int

#pk값 다시 설절하자
class Glass(models.Model): # 서빙 글라스 모델
    name = models.CharField(primary_key = True,max_length=255)

    def __str__(self):
        return self.name
    
# class Ingredient(models.Model): #나중에 상속으로 해결할 수 있지 않을까
#     name = models.CharField(primary_key = True,max_length=255)

class Base(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    alcohol_degree = models.FloatField(default = 0.0)
    
class Sub(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    alcohol_degree = models.FloatField(default = 0.0)
    
class Juice(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    
class Other(models.Model):
    name = models.CharField(primary_key = True,max_length=255)

class Cocktail(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    recipe = models.TextField()
    img_url = models.URLField()
    alcohol_degree = models.FloatField(default = 0.0)
    glass = models.ForeignKey(Glass, on_delete=models.CASCADE, null=True, related_name = 'cocktail')

    def __str__(self):
        return self.name
    
class CocktailBase(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_base')
    base = models.ForeignKey(Base, on_delete=models.CASCADE, related_name = 'cocktail_base')
    amount = models.FloatField(default = 0.0)
    
class CocktailSub(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_sub')
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name = 'cocktail_sub')
    amount = models.FloatField(default = 0.0)
class CocktailJuice(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_juice')
    juice = models.ForeignKey(Juice, on_delete=models.CASCADE, related_name = 'cocktail_juice')
    amount = models.FloatField(default = 0.0)
    
class CocktailOther(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name = 'cocktail_other')
    other = models.ForeignKey(Other, on_delete=models.CASCADE, related_name = 'cocktail_other')
    amount = models.CharField(max_length = 50, blank = True)