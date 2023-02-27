from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from .models import *

test_cocktail_data = {
	"name" : "마이 타이",
    "base" : [
        {"name" : "다크 럼", "amount" : 30.0},
        {"name" : "골드 럼", "amount" : 30.0}
    ],
    "sub" : [
        {"name" : "오렌지 큐라소", "amount" : 15.0}
    ],
    "juice" : [
        {"name" : "라임 주스", "amount" : 30.0},
        {"name" : "오르쟈 시럽", "amount" : 15.0},
        {"name" : "심플 시럽", "amount" : 7.0}
    ],
    "other": [
        {"name" : "라임 필", "amount" : "1슬라이스"},
        {"name" : "민트 잎", "amount" : "3~4잎"}
    ],
    "recipe" : "위의 재료들을 ......... 완성.",
    "img_url": "https://t1.daumcdn.net/cfile/tistory/9923B0495D66434618",
    "glass" : "올드 패션드 글라스",
    "hashtag" : ["달콤한","과일향이 나는"]
}

class CocktailsURLTest(TestCase):
    def setUp(self):
        Base.objects.create(name="다크 럼", alcohol_degree = 40.0)
        Base.objects.create(name="골드 럼", alcohol_degree = 40.0)
        Sub.objects.create(name = "오렌지 큐라소", alcohol_degree = 20.0)
        Juice.objects.create(name = "라임 주스")
        Juice.objects.create(name = "오르쟈 시럽")
        Juice.objects.create(name = "심플 시럽")
        Other.objects.create(name = "라임 필")
        Other.objects.create(name = "민트 잎")
        Glass.objects.create(name = "올드 패션드 글라스")
        HashTag.objects.create(name = "달달한")
        
    def test_api_cocktails_get(self):
        response = self.client.get('/cocktails')
        self.assertEqual(response.status_code,200)
        
    def test_api_cocktails_post(self):
        request_body = test_cocktail_data
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,201)
        
    def test_api_cocktails_put(self):
        request_body = test_cocktail_data
        response = self.client.put('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        
    def test_api_cocktails_delete(self):
        response = self.client.delete('/cocktails')
        self.assertEqual(response.status_code,400)
        
    def test_api_cocktails_post_no_glass_error(self):
        request_body = test_cocktail_data
        request_body['glass'] = "없는 칵테일 잔"
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        
    def test_api_cocktails_post_no_base_error(self):
        request_body = test_cocktail_data
        request_body['base'] = [{"name" : "error_data", "amount" : 30.0}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        
    def test_api_cocktails_post_no_sub_error(self):
        request_body = test_cocktail_data
        request_body['sub'] = [{"name" : "error_data", "amount" : 30.0}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        
    def test_api_cocktails_post_no_juice_error(self):
        request_body = test_cocktail_data
        request_body['juice'] = [{"name" : "error_data", "amount" : 30.0}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)

    def test_api_cocktails_post_no_other_error(self):
        request_body = test_cocktail_data
        request_body['juice'] = [{"name" : "error_data", "amount" : "error_string"}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        
    def test_cocktailBase(self):
        cocktail = Cocktail.objects.create(name="잭 콕")
        base = Base.objects.create(name = "잭 다니엘스",alcohol_degree = 40.0)
        mapping_table = CocktailBase.objects.create(cocktail = cocktail,name = base,amount = 20.0)
        self.assertTrue((mapping_table.cocktail == cocktail and mapping_table.name == base and mapping_table.amount == 20.0))
        
    def test_cocktailSub(self):
        cocktail = Cocktail.objects.create(name="test_cocktail")
        sub = Sub.objects.create(name = "test_sub",alcohol_degree = 20.0)
        mapping_table = CocktailSub.objects.create(cocktail = cocktail,name = sub,amount = 20.0)
        self.assertTrue((mapping_table.cocktail == cocktail and mapping_table.name == sub and mapping_table.amount == 20.0))
        
    def test_cocktailJuice(self):
        cocktail = Cocktail.objects.create(name="test_cocktail")
        juice = Juice.objects.create(name = "test_juice")
        mapping_table = CocktailJuice.objects.create(cocktail = cocktail,name = juice,amount = 20.0)
        self.assertTrue((mapping_table.cocktail == cocktail and mapping_table.name == juice and mapping_table.amount == 20.0))
        
    def test_cocktailOther(self):
        cocktail = Cocktail.objects.create(name="test_cocktail")
        other = Other.objects.create(name = "test_juice")
        mapping_table = CocktailOther.objects.create(cocktail = cocktail,name = other,amount = 20.0)
        self.assertTrue((mapping_table.cocktail == cocktail and mapping_table.name == other and mapping_table.amount == 20.0))
        

class CocktailURLTest(TestCase):
    def setUp(self):
        Base.objects.create(name="다크 럼", alcohol_degree = 40.0)
        Base.objects.create(name="골드 럼", alcohol_degree = 40.0)
        Sub.objects.create(name = "오렌지 큐라소", alcohol_degree = 20.0)
        Juice.objects.create(name = "라임 주스")
        Juice.objects.create(name = "오르쟈 시럽")
        Juice.objects.create(name = "심플 시럽")
        Other.objects.create(name = "라임 필")
        Other.objects.create(name = "민트 잎")
        HashTag.objects.create(name = "달달한")
        glass = Glass.objects.create(name = "올드 패션드 글라스")
        Cocktail.objects.create(name = "마이 타이",glass = glass)
        
    def test_api_cocktail_get(self):
        response = self.client.get('/cocktails/마이 타이')
        self.assertEqual(response.status_code,200)
        
    def test_api_cocktail_post(self):
        request_body = test_cocktail_data
        response = self.client.post('/cocktails/마이 타이',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        
    def test_api_cocktail_put(self):
        request_body = test_cocktail_data
        response = self.client.put('/cocktails/마이 타이',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        
    def test_api_cocktail_delete(self):
        response = self.client.delete('/cocktails/마이 타이')
        self.assertEqual(response.status_code,200)

class TodayDrinkURLTest(TestCase):
    def setUp(self):
        glass = Glass.objects.create(name = "올드 패션드 글라스")
        Cocktail.objects.create(name = "마이 타이",glass = glass)
    
    def test_api_today_drink_get(self):
        response = self.client.get('/today-drink')
        self.assertEqual(response.status_code,200)
        
class IngredientsURLTest(TestCase):
    def setUp(self):
        Base.objects.create(name="다크 럼", alcohol_degree = 40.0)
        Base.objects.create(name="골드 럼", alcohol_degree = 40.0)
        Sub.objects.create(name = "오렌지 큐라소", alcohol_degree = 20.0)
        Juice.objects.create(name = "라임 주스")
        Juice.objects.create(name = "오르쟈 시럽")
        Juice.objects.create(name = "심플 시럽")
        Other.objects.create(name = "라임 필")
        Other.objects.create(name = "민트 잎")
        Glass.objects.create(name = "올드 패션드 글라스")
        HashTag.objects.create(name = "달달한")
    
    def test_api_ingredients_get(self):
        response = self.client.get('/ingredients')
        self.assertEqual(response.status_code,200)

# class SearchURLTest(TestCase):
#     def setUp(self):
#         Base.objects.create(name="다크 럼", alcohol_degree = 40.0)
#         Base.objects.create(name="골드 럼", alcohol_degree = 40.0)
#         Base.objects.create(name="잭 다니엘스", alcohol_degree = 40.0)
#         Sub.objects.create(name = "오렌지 큐라소", alcohol_degree = 20.0)
#         Juice.objects.create(name = "콜라")
#         Juice.objects.create(name = "라임 주스")
#         Juice.objects.create(name = "오르쟈 시럽")
#         Juice.objects.create(name = "심플 시럽")
#         Other.objects.create(name = "라임 필")
#         Other.objects.create(name = "민트 잎")
#         Glass.objects.create(name = "올드 패션드 글라스")
#         HashTag.objects.create(name = "달달한")
        
    
#     def test_api_ingredients_get(self):
#         response = self.client.get('/ingredients')
#         self.assertEqual(response.status_code,200)
    

