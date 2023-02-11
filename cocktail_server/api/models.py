from django.db import models
# from api.validators import check_amount_int

class Glass(models.Model): #칵테일 세팅 잔 정보
    name = models.CharField(max_length =40, primary_key=True)
    
class Cocktail(models.Model): #칵테일 레시피 정보
    name = models.CharField(max_length =40, primary_key=True)
    recipe = models.CharField(max_length=400, default="")
    img_url = models.URLField(max_length=300, default="", blank=True)
    alcohol_degree = models.FloatField(null=True)
    glass_name = models.ForeignKey(Glass, on_delete=models.CASCADE, db_column= 'glass_name')
    
class Base(models.Model): # 베이스 술 정보
    name = models.CharField(max_length=30,primary_key=True)
    alcohol_degree = models.FloatField(null=True)
class Sub(models.Model): # 서브 리큐르 정보
    name = models.CharField(max_length=30,primary_key=True)
    alcohol_degree = models.FloatField(null=True)
class Juice(models.Model): # 주스 정보
    name = models.CharField(max_length=30,primary_key=True)
class Other(models.Model): # 기타 재료 정보 ex) 민트, 라임 등등..
    name = models.CharField(max_length=30,primary_key=True)

class CocktailBase(models.Model): #베이스,칵테일레시피 다대다 연결 중간 테이블
    cocktail_name = models.ForeignKey(Cocktail, on_delete=models.CASCADE, db_column= 'cocktail_name')
    base_name = models.ForeignKey(Base, on_delete=models.CASCADE, db_column= 'base_name')
    oz = models.FloatField(null=True) # 베이스 양 (온즈)
    
class CocktailSub(models.Model): #서브 중간 테이블
    cocktail_name = models.ForeignKey(Cocktail, on_delete=models.CASCADE, db_column= 'cocktail_name')
    sub_name = models.ForeignKey(Sub, on_delete=models.CASCADE, db_column= 'sub_name')
    oz = models.FloatField(null=True) # 서브 양
    
class CocktailJuice(models.Model):
    cocktail_name = models.ForeignKey(Cocktail, on_delete=models.CASCADE, db_column= 'cocktail_name')
    juice_name = models.ForeignKey(Juice, on_delete=models.CASCADE, db_column= 'juice_name')
    oz = models.FloatField(null=True) # 주스 양
    
class CocktailOther(models.Model):
    cocktail_name = models.ForeignKey(Cocktail, on_delete=models.CASCADE, db_column= 'cocktail_name')
    other_name = models.ForeignKey(Other, on_delete=models.CASCADE, db_column= 'other_name')
    amount = models.CharField(max_length =40, default = "", blank=True) # 기타 재료 양 ex) 민트 - 한 장 등등...
    
class TodayDrink(models.Model): # 오늘의 드링크 추천용
    drink_name = models.ForeignKey(Cocktail, on_delete=models.CASCADE, db_column= 'today_drink')