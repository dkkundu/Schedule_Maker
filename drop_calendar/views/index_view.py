import json
from django.views.generic import TemplateView  # View,
from drop_calendar.models import ScheduleEvent, Events
from drop_calendar.forms import GroupOrClass
import datetime
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse


class CalenderIndexPage(TemplateView):
    template_name = "drop_calendar/calendar.html"
    model = ScheduleEvent

    def get_context_data(self, **kwargs):
        context = super(CalenderIndexPage, self).get_context_data(**kwargs)
        query = self.model.objects.custom_filter()
        event_arr = []
        if query:
            for i in query:
                event_sub_arr = {}
                start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%S")
                end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%S")
                print(start_date)
                event_sub_arr['title'] = i.name
                event_sub_arr['start'] = start_date
                event_sub_arr['end'] = end_date
                event_arr.append(event_sub_arr)
                # return HttpResponse(json.dumps(event_arr))

        print("data----", event_arr)
        context["event_data"] = json.dumps(event_arr)
        print(context["event_data"])
        context["events"] = GroupOrClass
        return context



class CalenderIndexPage2(TemplateView):
    template_name = "drop_calendar/calendar2.html"


def event(request):
    all_events = Events.objects.all()
    get_event_types = Events.objects.only('event_type')

    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:
        event_arr = []
        if request.GET.get('event_type') == "all":
            all_events = Events.objects.all()
        else:
            all_events = Events.objects.filter(event_type__icontains=request.GET.get('event_type'))

        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.event_name
            start_date = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    context = {
        "events":all_events,
        "get_event_types":get_event_types,

    }
    return render(request, 'admin/poll/event_management.html', context)


def calendar(request):
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'drop_calendar/calendar2.html', context)


def add_event(request):
    name = request.GET.get("name", None)
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)
    allDay = request.GET.get("allDay", None)
    description = request.GET.get("description", None)
    # end = request.GET.get("end", None)
    # title = request.GET.get("title", None)
    # event = Events(name=str(title), start=start, end=end)
    # event.save()
    print("name--------", name)
    print("start_date--------", start_date)
    print("end_date--------", end_date)
    print("allDay--------", allDay)
    print("description--------", description)
    data = {}
    return JsonResponse(data)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)