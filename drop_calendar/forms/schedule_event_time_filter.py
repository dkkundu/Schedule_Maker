from django import forms
import datetime
from drop_calendar.models import (
    ClassScheduleEvent,
    AdmissionClass,
    ClassSanction
)


YEAR_CHOICES = []
for y in range(2000, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((y, y))


class EventTimeFilter(forms.Form):
    date_field = forms.DateTimeField(

    )


class ClassScheduleEventFilter(forms.ModelForm):

    class Meta:
        model = ClassScheduleEvent
        fields = [
            "schedule_class",
            "class_sanction",
        ]
        widgets = {
            'schedule_class': forms.Select(attrs={
                'id': 'schedule_class',
                'class': 'form-control',
                'style': 'display: inline-block; width:99%',
            }),
            'class_sanction': forms.Select(attrs={
                'id': 'class_sanction',
                'class': 'form-control',
                'style': 'display: inline-block; width:99%',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ClassScheduleEventFilter, self).__init__(*args, **kwargs)
        choices_schedule_class = [(None, "Select Class")]
        choices_class_sanction = [(None, "Select Sanction")]

        sanction = ClassSanction.objects.all()
        admission_class = AdmissionClass.objects.all()

        sanction_model_choices = [(dep.pk, dep.name) for dep in sanction]
        class_model_choices = [(obj.pk, obj.name) for obj in admission_class]

        choices_schedule_class.extend(class_model_choices)
        choices_class_sanction.extend(sanction_model_choices)

        self.fields['schedule_class'].choices = choices_schedule_class
        self.fields["class_sanction"].choices = choices_class_sanction
