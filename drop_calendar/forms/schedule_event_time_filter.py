from django import forms
import datetime


YEAR_CHOICES = []
for y in range(2000, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((y, y))


class EventTimeFilter(forms.Form):
    date_field = forms.DateTimeField(

    )

