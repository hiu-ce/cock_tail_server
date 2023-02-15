from django.contrib import admin
from .models import Cocktail,Glass,Base,Sub,Juice,Other,CocktailBase,CocktailSub,CocktailJuice,CocktailOther

admin.site.register(Cocktail)
admin.site.register(Base)
admin.site.register(Sub)
admin.site.register(Juice)
admin.site.register(Other)
admin.site.register(CocktailBase)
admin.site.register(CocktailSub)
admin.site.register(CocktailJuice)
admin.site.register(CocktailOther)
admin.site.register(Glass)

# Register your models here.
