from django.core.exceptions import ValidationError

def check_amount_int(value_dict):
    for key in value_dict:
        if type(value_dict[key]) != int:
            value_dict[key] = int(value_dict[key])