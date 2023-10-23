from django import template
register = template.Library()
@register.filter


def get_subdata(data, key):
    try:
        return data[int(key)]
    except:
        try:
            
            return data.key
            
        except:
            try:
                return data[key]
            except:
                pass
        

def get_field(model, field):
    try:
        return model.field
    except:
        pass
    
