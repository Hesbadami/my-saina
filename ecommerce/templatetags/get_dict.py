from django import template
register = template.Library()
@register.filter


def get_subdata(data, key):
    if key in data:
        return data[key]
        
  
    
    
