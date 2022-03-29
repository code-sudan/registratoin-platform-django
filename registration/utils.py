from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import csv


#for get_quote function
from .models import *
from random import randint

def download_csv(request, queryset):

  if not request.user.is_staff:
    raise PermissionDenied

  model = queryset.model
  model_fields = model._meta.fields + model._meta.many_to_many
  field_names = [field.name for field in model_fields]

  response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
  response['Content-Disposition'] = 'attachment; filename="export.csv"'

  # the csv writer
  writer = csv.writer(response, delimiter=",")
  # Write a first row with header information
  writer.writerow(field_names)
  # Write data rows
  for row in queryset:
      values = []
      for field in field_names:
          value = getattr(row, field)
          if callable(value):
              try:
                  value = value() or ''
              except:
                  value = 'Error retrieving value'
          if value is None:
              value = ''
          values.append(value)
      writer.writerow(values)
  return response


def get_quote():
    try: 
        count = CodeSudanQuote.objects.count()
        quote = CodeSudanQuote.objects.all()[randint(0, count -1)]
    except Exception as e:
        print(e)
        return None
    return 1
