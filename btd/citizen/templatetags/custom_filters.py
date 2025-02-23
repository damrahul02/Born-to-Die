from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='add_years')
def add_years(date, years):
    """Add years to a date"""
    try:
        return date.replace(year=date.year + int(years))
    except ValueError:
        # Handle leap years
        return date + timedelta(days=365 * int(years)) 