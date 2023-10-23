from django import template
register = template.Library()
@register.filter


def get_subdata(data, key):
    if key in data:
        return data[key]
        

def get_field(model, field):
    try:
        return model.field
    except:
        pass
    
