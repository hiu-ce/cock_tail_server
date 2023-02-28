from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from .models import *
import copy

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
        glass = Glass.objects.get(name = "올드 패션드 글라스")
        Cocktail.objects.create(name = "마이 타이", glass = glass)
        response = self.client.get('/cocktails')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()[0]["name"],"마이 타이")
        
    def test_api_cocktails_post(self):
        request_body = copy.deepcopy(test_cocktail_data)
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json()['name'],"마이 타이")
        
    def test_api_cocktails_put(self):
        request_body = copy.deepcopy(test_cocktail_data)
        response = self.client.put('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"Unallowed http method, Please check http method again")
        
    def test_api_cocktails_delete(self):
        response = self.client.delete('/cocktails')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"Unallowed http method, Please check http method again")
        
    def test_api_cocktails_post_no_glass_error(self):
        request_body = copy.deepcopy(test_cocktail_data)
        request_body['glass'] = "없는 칵테일 잔"
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"glass name is invalid")
        
    def test_api_cocktails_post_no_base_error(self):
        request_body = copy.deepcopy(test_cocktail_data)
        request_body['base'] = [{"name" : "error_data", "amount" : 30.0}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"base name is invalid")
        
    def test_api_cocktails_post_no_sub_error(self):
        request_body = copy.deepcopy(test_cocktail_data)
        request_body['sub'] = [{"name" : "error_data", "amount" : 30.0}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"sub name is invalid")
        
    def test_api_cocktails_post_no_juice_error(self):
        request_body = copy.deepcopy(test_cocktail_data)
        request_body['juice'] = [{"name" : "error_data", "amount" : 30.0}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"juice name is invalid")

    def test_api_cocktails_post_no_other_error(self):
        request_body = copy.deepcopy(test_cocktail_data)
        request_body['other'] = [{"name" : "error_data", "amount" : "error_string"}]
        response = self.client.post('/cocktails',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"other name is invalid")
        
    def test_api_cocktails_post_same_name_cocktail(self):
        glass = Glass.objects.get(name = "올드 패션드 글라스")
        Cocktail.objects.create(name = "마이 타이", glass = glass)
        request_body = copy.deepcopy(test_cocktail_data)
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
        self.assertEqual(response.json()['name'],"마이 타이")
        
    def test_api_cocktail_post(self):
        request_body = copy.deepcopy(test_cocktail_data)
        response = self.client.post('/cocktails/마이 타이',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['error_message'],"Unallowed http method, Please check http method again")
        
    def test_api_cocktail_put(self):
        request_body = copy.deepcopy(test_cocktail_data)
        response = self.client.put('/cocktails/마이 타이',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()["name"],"마이 타이")
        
    def test_api_cocktail_delete(self):
        response = self.client.delete('/cocktails/마이 타이')
        self.assertEqual(response.status_code,200)

class TodayDrinkURLTest(TestCase):
    # def test_api_today_drink_get_without_cocktail(self):
    #     response = self.client.get('/today-drink')
    #     self.assertEqual(response.status_code,400) 
    def test_api_today_drink_get(self):
        glass = Glass.objects.create(name = "올드 패션드 글라스")    
        Cocktail.objects.create(name = "마이 타이",glass = glass)
        response = self.client.get('/today-drink')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()["name"],"마이 타이")        
        
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
        response_data = {
            "base" : [ 
                "골드 럼",
                "다크 럼"
            ],
            "sub" : [
                "오렌지 큐라소"
            ],
            "juice" : [
                "라임 주스", 
                "심플 시럽",
                "오르쟈 시럽"
            ],
            "other" : [
                "라임 필",
                "민트 잎"
            ]
        }
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)
        
class IngredientsBasesURLTest(TestCase):
    def setUp(self):
        Base.objects.create(name="다크 럼", alcohol_degree = 40.0)
        Base.objects.create(name="골드 럼", alcohol_degree = 40.0)
    def test_api_ingredients_bases_get(self):
        response = self.client.get('/ingredients/bases')
        response_data = [
            {'name': '골드 럼', 'alcohol_degree': 40.0},
            {'name': '다크 럼', 'alcohol_degree': 40.0}
        ]
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)
        
    def test_api_ingredients_bases_post(self):
        request_body = {
            "name" : "잭 다니엘스",
            "alcohol_degree" : 40.0
        }
        response = self.client.post('/ingredients/bases',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertTrue(Base.objects.filter(name="잭 다니엘스").exists())
        
    def test_api_ingredients_bases_delete(self):
        response = self.client.delete('/ingredients/bases/골드 럼',content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertFalse(Base.objects.filter(name="골드 럼").exists())

class IngredientsSubsURLTest(TestCase):
    def setUp(self):
        Sub.objects.create(name = "오렌지 큐라소", alcohol_degree = 20.0)
        
    def test_api_ingredients_subs_get(self):
        response = self.client.get('/ingredients/subs')
        response_data = [{'name': '오렌지 큐라소', 'alcohol_degree': 20.0}]
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)
        
    def test_api_ingredients_subs_post(self):
        request_body = {
            "name" : "블루 큐라소",
            "alcohol_degree" : 20.0
        }
        response = self.client.post('/ingredients/subs',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertTrue(Sub.objects.filter(name="블루 큐라소").exists())
        
    def test_api_ingredients_subs_delete(self):
        response = self.client.delete('/ingredients/subs/오렌지 큐라소',content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertFalse(Sub.objects.filter(name="오렌지 큐라소").exists())
        
class IngredientsJuicesURLTest(TestCase):
    def setUp(self):
        Juice.objects.create(name = "라임 주스")
        Juice.objects.create(name = "오르쟈 시럽")
        Juice.objects.create(name = "심플 시럽")
        
    def test_api_ingredients_juices_get(self):
        response = self.client.get('/ingredients/juices')
        response_data = [
            {"name" : "라임 주스"},
            {"name" : "심플 시럽"},
            {"name" : "오르쟈 시럽"}
        ]
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)

    def test_api_ingredients_juices_post(self):
        request_body = {
            "name" : "콜라"
        }
        response = self.client.post('/ingredients/juices',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertTrue(Juice.objects.filter(name="콜라").exists())
        
    def test_api_ingredients_subs_delete(self):
        response = self.client.delete('/ingredients/juices/라임 주스',content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertFalse(Juice.objects.filter(name="라임 주스").exists())
        
class IngredientsOthersURLTest(TestCase):
    def setUp(self):
        Other.objects.create(name = "라임 필")
        Other.objects.create(name = "민트 잎")

    def test_api_ingredients_others_get(self):
        response = self.client.get('/ingredients/others')
        response_data = [
	        {"name" : "라임 필"},
	        {"name" : "민트 잎"}
        ]
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)

    def test_api_ingredients_others_post(self):
        request_body = {
            "name" : "레몬"
        }
        response = self.client.post('/ingredients/others',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertTrue(Other.objects.filter(name="레몬").exists())
        
    def test_api_ingredients_others_delete(self):
        response = self.client.delete('/ingredients/others/민트 잎',content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertFalse(Other.objects.filter(name="민트 잎").exists())
        
class GlassURLTest(TestCase):
    def setUp(self):
        Glass.objects.create(name = "올드 패션드 글라스")
    def test_api_glasses_get(self):
        response = self.client.get('/glasses')
        response_data = [
	        {"name" : "올드 패션드 글라스"}
        ]
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)
        
    def test_api_glasses_post(self):
        request_body = {
            "name" : "칵테일 잔"
        }
        response = self.client.post('/glasses',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,201)
        self.assertTrue(Glass.objects.filter(name="칵테일 잔").exists())
        
    def test_api_glasses_delete(self):
        response = self.client.delete('/glasses/올드 패션드 글라스',content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertFalse(Glass.objects.filter(name="올드 패션드 글라스").exists())
        
class HashTagURLTest(TestCase):
    def setUp(self):
        HashTag.objects.create(name = "달달한")
        
    def test_api_hashtags_get(self):
        response = self.client.get('/hashtags')
        response_data = [{"name": "달달한"}]
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),response_data)
        
    def test_api_hashtags_post(self):
        request_body = {
            "name" : "과일 향이 나는"
        }
        response = self.client.post('/hashtags',request_body,content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertTrue(HashTag.objects.filter(name="과일 향이 나는").exists())
        
    def test_api_hashtags_delete(self):
        response = self.client.delete('/hashtags/달달한',content_type = 'application/json')
        self.assertEqual(response.status_code,200)
        self.assertFalse(HashTag.objects.filter(name="달달한").exists())
    
class SearchURLTest(TestCase):
    def setUp(self):
        base1 = Base.objects.create(name="다크 럼", alcohol_degree = 40.0)
        base2 = Base.objects.create(name="골드 럼", alcohol_degree = 40.0)
        base3 = Base.objects.create(name="잭 다니엘스", alcohol_degree = 40.0)
        sub1 = Sub.objects.create(name = "오렌지 큐라소", alcohol_degree = 20.0)
        juice1 = Juice.objects.create(name = "콜라")
        juice2 = Juice.objects.create(name = "라임 주스")
        juice3 = Juice.objects.create(name = "오르쟈 시럽")
        juice4 = Juice.objects.create(name = "심플 시럽")
        other1 = Other.objects.create(name = "라임 필")
        other2 = Other.objects.create(name = "민트 잎")
        glass1 = Glass.objects.create(name = "올드 패션드 글라스")
        hashtag1 = HashTag.objects.create(name = "달달한")
        
        cocktail1 = Cocktail.objects.create(name = "마이 타이",glass = glass1)
        cocktail1.base.add("다크 럼", "골드 럼")
        cocktail1.sub.add("오렌지 큐라소")
        cocktail1.juice.add("라임 주스")
        cocktail1.other.add("민트 잎")
        cocktail1.hashtag.add("달달한")
        
        cocktail2 = Cocktail.objects.create(name = "잭 콕",glass = glass1)
        cocktail2.base.add("잭 다니엘스")
        cocktail2.juice.add("콜라")
        cocktail2.other.add("라임 필")
        cocktail2.hashtag.add("달달한")
        
    
    

