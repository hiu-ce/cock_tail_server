from .models import Cocktail,TodayDrink

def todayDrink():
    today_drink = Cocktail.objects.order_by("?").first()
    last_drink = TodayDrink.objects.all().first()
    
    if last_drink:
        last_drink.cocktail = today_drink
        last_drink.save()
    else:
        new_obj = TodayDrink.objects.create(cocktail = today_drink)
        new_obj.save()

    