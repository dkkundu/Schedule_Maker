import json
from django.views.generic import TemplateView
from .get_pdf import render_pdf
from drop_calendar.models import ClassScheduleEvent


class ClassScheduleEventCalenderPDFView(
    TemplateView
):
    template_name = "drop_calendar/download/get_calender_copy.html"
    model = ClassScheduleEvent

    def get(self, request, **kwargs):
        quarry_object = self.model.objects.get(
            pk=self.kwargs['pk']
        )
        query = self.model.objects.custom_filter().filter(
            schedule_class=quarry_object.schedule_class,
            class_sanction=quarry_object.class_sanction
        )
        event_arr = []
        if query:
            for i in query:
                if i.name and i.start_date and i.end_date:
                    event_sub_arr = {'id': i.pk}
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print('i.start_date----', i.start_date)
                    print('i.start_date formet --------------', start_date)
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    event_sub_arr['title'] = i.name
                    event_sub_arr['start'] = start_date
                    event_sub_arr['end'] = end_date
                    event_arr.append(event_sub_arr)

        context = {
            "event_data": json.dumps(event_arr),
            "event": query,
            "object": quarry_object,
            "load_date": quarry_object.start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "schedule_class": quarry_object.schedule_class.name,
            "class_sanction": quarry_object.class_sanction.name,
        }

        return render_pdf(
            request, self.template_name, context, 'appname'
        )
