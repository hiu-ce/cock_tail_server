from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from .models import *

class CocktailModelTest(TestCase):
    def setUp(self):
        base = Base.objects.create(name="잭 다니엘스", alcohol_degree = 40.0)
        juice = Juice.objects.create(name = "콜라")
        glass = Glass.objects.create(name = "올드 패션드 글라스")
        hashtag = HashTag.objects.create(name = "달달한")
        cocktail = Cocktail.objects.create(name = "잭 콕",glass = glass)
    def test_mapping_table(self):
        cocktail = Cocktail.objects.get(name = "잭 콕")
        base = Base.objects.get(name="잭 다니엘스")
        cocktail_base = CocktailBase.objects.create(cocktail = cocktail,name = base,amount = 20.0)
    #     self.assertTrue(cocktail_base)
    # def test_hashtag_mapping(self):
    #     cocktail = Cocktail.objects.get(name = "잭 콕")
    #     hashtag = hashtag = HashTag.objects.all()
    #     cocktail.hashtag.add(hashtag)
        
    #     self.assertEqual(cocktail.hashtag, hashtag)
    def test_api_cocktails_get(self):
        response = self.client.get('/cocktails')
        print(response.json())
        self.assertEqual(response.status_code,200)
        
    def test_api_cocktails_post(self):
        request = {
	        "name" : "Hashtest2",
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
        response = self.client.post('/cocktails',request,content_type = 'application/json')
        self.assertEqual(response.status_code,400)
    
    
# factory = APIRequestFactory()
# request = factory.post('/cocktails',json.dumps({
# 	"name" : "Hashtest2",
# 	 "base" : [
# 			{"name" : "다크 럼", "amount" : 30.0},
# 			{"name" : "골드 럼", "amount" : 30.0}
# 	],
# 	"sub" : [
# 		{"name" : "오렌지 큐라소", "amount" : 15.0}
# 	],
# 	"juice" : [
# 		{"name" : "라임 주스", "amount" : 30.0},
# 		{"name" : "오르쟈 시럽", "amount" : 15.0},
# 		{"name" : "심플 시럽", "amount" : 7.0}
# 	],
# 	"other": [
# 		{"name" : "라임 필", "amount" : "1슬라이스"},
# 		{"name" : "민트 잎", "amount" : "3~4잎"}
# 	],
# 	"recipe" : "위의 재료들을 ......... 완성.",
# 	"img_url": "https://t1.daumcdn.net/cfile/tistory/9923B0495D66434618",
# 	"glass" : "올드 패션드 글라스",
#     "hashtag" : ["달콤한","과일향이 나는"]
# }),content_type='application/json')

# request = factory.get('/cocktails/Hashtest2')
