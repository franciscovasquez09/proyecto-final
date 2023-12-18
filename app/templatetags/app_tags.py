from django import template
import locale
register = template.Library()

def currency_format(value):
  locale.setlocale(locale.LC_ALL, 'es_CL.utf-8') 
  return locale.currency(value, grouping=True)

register.filter('currency_format',currency_format)