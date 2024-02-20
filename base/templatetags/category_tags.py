from django import template
from ..models import Category

register = template.Library()

@register.filter(name='get_uncategorized')
def get_uncategorized(categories):
    return categories.filter(is_uncategorized=True).first()
