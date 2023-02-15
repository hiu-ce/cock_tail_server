from django.db import models
# from api.validators import check_amount_int

#pk값 다시 설절하자
class Glass(models.Model):
    name = models.CharField(primary_key = True,max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Cocktail(models.Model):
    name = models.CharField(primary_key = True,max_length=255)
    recipe = models.TextField()
    img_url = models.URLField()
    alcohol_degree = models.FloatField()
    glass = models.ForeignKey(Glass, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    
class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()