from rest_framework import serializers
from .models import Cocktail, Glass,Base,Sub,Juice,Other,CocktailBase,CocktailSub,CocktailJuice,CocktailOther

class CocktailNameSerializer(serializers.ModelSerializer): # 칵테일 이름만 출력
    class Meta:
        model = Cocktail
        fields = ('name',)
    
class GlassSerializer(serializers.ModelSerializer): # 서빙 글라스 이름 출력
    class Meta:
        model = Glass
        fields = ('name',)
        
class BaseSerializer(serializers.ModelSerializer): # 베이스 재료 이름, 도수
    class Meta:
        model = Base
        fields = ('name','alcohol_degree')      
class SubSerializer(serializers.ModelSerializer): # 서브 재료 이름, 도수
    class Meta:
        model = Sub
        fields = ('name','alcohol_degree')
        
class JuiceSerializer(serializers.ModelSerializer): # 주스 이름
    class Meta:
        model = Juice
        fields = ('name',)
        
class OtherSerializer(serializers.ModelSerializer): # 기타 재료 이름
    class Meta:
        model = Other
        fields = ('name',)
        
class CocktailBaseSerializer(serializers.ModelSerializer): # 중간 테이블
    alcohol_degree = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = CocktailBase
        fields = ('name','amount','alcohol_degree')
        
    def get_alcohol_degree(self,obj):
        return obj.name.alcohol_degree
    
class CocktailSubSerializer(serializers.ModelSerializer):
    alcohol_degree = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = CocktailSub
        fields = ('name','amount','alcohol_degree')
        
    def get_alcohol_degree(self,obj):
        print(obj)
        return obj.name.alcohol_degree
        
    
class CocktailJuiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailJuice
        fields = ('name','amount')
        
    def get_name(self,obj):
        return obj.juice
    
class CocktailOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailOther
        fields = ('name','amount')
        
    def get_name(self,obj):
        return obj.other
        
class CocktailSerializer(serializers.ModelSerializer): # 칵테일 레시피 출력 serialzier
    glass = serializers.StringRelatedField(read_only = True)
    base = CocktailBaseSerializer(many = True,read_only = True, source ='cocktail_base')
    sub =  CocktailSubSerializer(many = True, read_only = True, source = 'cocktail_sub')
    juice = CocktailJuiceSerializer(many = True,read_only = True, source = 'cocktail_juice')
    other = CocktailOtherSerializer(many = True,read_only = True, source ='cocktail_other')

    class Meta:
        model = Cocktail
        fields = ('name','base','sub','juice','other','recipe','img_url','glass')
        