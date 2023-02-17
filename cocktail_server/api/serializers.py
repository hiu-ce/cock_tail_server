from rest_framework import serializers
from .models import Cocktail, Glass,Base,Sub,Juice,Other,CocktailBase,CocktailSub,CocktailJuice,CocktailOther

class CocktailNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ('name',)
    
class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = ('name',)
        
    def update(self,obj,validated_data): #잔 이름 수정 함수 -> PK 수정 불가능하므로 새로 만든 후 테이블 다시 연결
        new_glass = Glass.objects.create(name = validated_data['name'])
        for cocktail in Cocktail.objects.filter(glass = obj):
            cocktail.glass = new_glass
            cocktail.save()
        obj.delete()
        return new_glass

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = '__all__'
        
class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub
        fields = '__all__'
        
class JuiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juice
        fields = '__all__'
        
class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = '__all__'
        
class CocktailSerializer(serializers.ModelSerializer): 
    glass = serializers.StringRelatedField(read_only = True)
    base = serializers.SerializerMethodField(read_only = True)
    sub = serializers.SerializerMethodField(read_only = True)
    juice = serializers.SerializerMethodField(read_only = True)
    other = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Cocktail
        fields = ('name','base','sub','juice','other','recipe','img_url','glass','alcohol_degree')
    
    def get_base(self,obj):
        data = {}
        cocktail = obj.name
        # cocktail_ingredient = CocktailIngredient.objects.filter(cocktail= cocktail)#N+1 Problem
        for cocktail_base in CocktailBase.objects.filter(cocktail = cocktail).select_related('base'):
            data[cocktail_base.base.name] = cocktail_base.amount
        return data
    
    def get_sub(self,obj):
        data = {}
        cocktail = obj.name
        for cocktail_sub in CocktailSub.objects.filter(cocktail = cocktail).select_related('sub'):
            data[cocktail_sub.sub.name] = cocktail_sub.amount 
        return data
        
    def get_juice(self,obj):
        data = {}
        cocktail = obj.name
        for cocktail_juice in CocktailJuice.objects.filter(cocktail = cocktail).select_related('juice'):
            data[cocktail_juice.juice.name] = cocktail_juice.amount 
        return data
    
    def get_other(self,obj):
        data = {}
        cocktail = obj.name
        for cocktail_other in CocktailOther.objects.filter(cocktail = cocktail).select_related('other'):
            data[cocktail_other.other.name] = cocktail_other.amount 
        return data
    