# from django.template.defaulttags import register
from django import template
from ast import literal_eval
register = template.Library()

@register.filter
def get_item(dictionary, key):
    # print('\n\n in get_item \n\n')
    # print(dictionary, key)
    return dictionary.get(key)

@register.filter
def get_item_difference(dictionary, keys):
    key1, key2 = literal_eval(keys)
    
    return (dictionary.get(key1) - dictionary.get(key2))

# #(b-d)-(c-a)
# def get_profit(keyword, vals)