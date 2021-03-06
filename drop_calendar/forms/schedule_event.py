from django import forms
from drop_calendar.models import (
    ScheduleEvent,
    ClassScheduleEvent
)


class ScheduleEventForm(forms.ModelForm):
    class Meta:
        model = ScheduleEvent
        fields = [
            "name",
            "start_date",
            "end_date",
            "allDay",
            "description",
            "event_type"
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 2
            }),

        }

    def __init__(self, *args, **kwargs):
        super(ScheduleEventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['name'].required = True
        self.fields['event_type'].required = True
        self.fields['start_date'].widget.attrs[
            'placeholder'
        ] = 'Start Date (YY-MM-DD H:M)'
        self.fields['end_date'].widget.attrs[
            'placeholder'
        ] = 'End Date (YY-MM-DD H:M)'


class ClassScheduleEventForm(forms.ModelForm):
    class Meta:
        model = ClassScheduleEvent
        fields = [
            "name",
            "start_date",
            "end_date",
            'schedule_class',
            'class_sanction',
            "event_type"
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 2
            }),

        }

    def __init__(self, *args, **kwargs):
        super(ClassScheduleEventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['name'].required = True
        self.fields['event_type'].required = True
        self.fields['class_sanction'].required = True
        self.fields['schedule_class'].required = True
        self.fields['start_date'].widget.attrs[
            'placeholder'
        ] = 'Start Date (YY-MM-DD H:M)'
        self.fields['end_date'].widget.attrs[
            'placeholder'
        ] = 'End Date (YY-MM-DD H:M)'
