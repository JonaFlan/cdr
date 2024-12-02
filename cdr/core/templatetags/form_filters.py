from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    try:
        return field.as_widget(attrs={"class": css_class})
    except AttributeError:
        return field  # Devuelve el campo sin modificaciones si no es un BoundField.