from django import forms
CHOICES = [
    ("FRESHMAN", 'Freshman'),
    ("SOPHOMORE", 'Sophomore'),
    ("JUNIOR", 'Junior'),
    ("SENIOR", 'Senior'),
    ("GRADUATE", 'Graduate'),
]


class GroupOrClass(forms.Form):
    group_or_class = forms.ChoiceField(
        choices=CHOICES
    )
    fields = [
        "group_or_class"
    ]
