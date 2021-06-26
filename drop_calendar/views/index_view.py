import json
import logging
from django.views.generic import  View
from drop_calendar.models import ScheduleEvent, Events
from drop_calendar.forms import GroupOrClass, ScheduleEventForm
import datetime
from django.contrib import messages
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
logger = logging.getLogger(__name__)


class CalenderIndexPage(View):
    template_name = "drop_calendar/calendar.html"
    model = ScheduleEvent

    def get(self, request, **kwargs):
        query = self.model.objects.custom_filter()
        event_arr = []
        if query:
            for i in query:
                if i.name and i.start_date and i.end_date:
                    event_sub_arr = {'id': i.pk}
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%S")
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%S")
                    print(start_date)
                    event_sub_arr['title'] = i.name
                    event_sub_arr['start'] = start_date
                    event_sub_arr['end'] = end_date
                    event_arr.append(event_sub_arr)

        context = {
            "event_data": json.dumps(event_arr),
            "event": query,
            "form": ScheduleEventForm,
            "events": GroupOrClass
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        query = self.model.objects.custom_filter()
        form = ScheduleEventForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            # save_form.created_user = self.request.user
            save_form.save()
        else:
            print(form.errors)
            messages.warning(request, "Unable to Save Data")
            logger.debug(request,"Unable to Save Data")

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

        context = {
            "event_data": json.dumps(event_arr),
            "form": ScheduleEventForm,
            "events": GroupOrClass,
            "event": query,
        }

        return render(request, self.template_name, context)



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
        "events": all_events,
        "get_event_types": get_event_types,

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