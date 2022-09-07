from django import template
  
register = template.Library()

def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)

@register.filter()
def convert_to_inr(amount):
    return formatINR(amount)

@register.filter()
def deduct_amts(val1, val2):
    return val1 - val2


register.filter('convert_to_inr', convert_to_inr)
register.filter('deduct_amts', deduct_amts)