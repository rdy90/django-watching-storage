from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    non_closed_visits = [
        {
            "who_entered": visit.passcard.owner_name,
            "entered_at": visit.entered_at,
            "duration": visit.format_duration(delta=visit.get_duration()),
        }
        for visit in Visit.objects.filter(leaved_at=None)
    ]

    return render(
        request,
        "storage_information.html",
        {
            "non_closed_visits": non_closed_visits,
        },
    )
