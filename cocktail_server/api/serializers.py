from rest_framework import serializers
from .models import Cocktail, Glass, Ingredient, CocktailIngredient

class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = ('name',)

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

# class CocktailIngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CocktailIngredient
#         fields = ('ingredient', 'amount')
class IngredientListingField(serializers.RelatedField):
    def to_representation(self, value):
        print(value)
        return (value.ingredient_id , value.amount)
    def get_queryset(self,value):
        print(value)
        return (value.ingredient_id , value.amount)
    
# class BaseSerializer(serializers.ModelSerializer):
#     base = IngredientListingField(many = True)
#     class Meta:
#         model = CocktailIngredient
#         fields = ('base',)
        
class CocktailSerializer(serializers.ModelSerializer): #이 방식이 제일 나은듯
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
        cocktail_ingredient = CocktailIngredient.objects.filter(cocktail= cocktail)
        for ingredient in cocktail_ingredient:
            if ingredient.ingredient.category == 'base':
                data[ingredient.ingredient.name] = ingredient.amount #3번참조 -> 비효율적 쿼리 생성하지 않을까?
        return data
    
    def get_sub(self,obj):
        data = {}
        cocktail = obj.name
        cocktail_ingredient = CocktailIngredient.objects.filter(cocktail= cocktail)
        for ingredient in cocktail_ingredient:
            if ingredient.ingredient.category == 'sub':
                data[ingredient.ingredient.name] = ingredient.amount #3번참조 -> 비효율적 쿼리 생성하지 않을까?
        return data
        
    def get_juice(self,obj):
        data = {}
        cocktail = obj.name
        cocktail_ingredient = CocktailIngredient.objects.filter(cocktail= cocktail)
        for ingredient in cocktail_ingredient:
            if ingredient.ingredient.category == 'juice':
                data[ingredient.ingredient.name] = ingredient.amount #3번참조 -> 비효율적 쿼리 생성하지 않을까?
        return data
    
    def get_other(self,obj):
        data = {}
        cocktail = obj.name
        cocktail_ingredient = CocktailIngredient.objects.filter(cocktail= cocktail)
        for ingredient in cocktail_ingredient:
            if ingredient.ingredient.category == 'other':
                data[ingredient.ingredient.name] = ingredient.amount #3번참조 -> 비효율적 쿼리 생성하지 않을까?
        return data
        
    