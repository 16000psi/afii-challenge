# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name="instrument_type_prettifier")
def instrument_type_prettifier(value):
    replacements = {
        "bond": "Bond",
        "cds": "CDS",
        "fx": "FX",
        "futures": "Futures",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


@register.filter(name="strategy_prettifier")
def strategy_prettifier(value):
    replacements = {
        "active_short": "Active Short",
        "relval": "RelVal",
        "slbs": "SLBS",
        "use_of_proceeds": "Use of Proceeds",
        "curves": "Curves",
        "hedge": "Hedge",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value
