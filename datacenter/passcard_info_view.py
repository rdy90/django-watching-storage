from django.shortcuts import render

from datacenter.models import Passcard


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits = [
        {
            "entered_at": visit.entered_at,
            "duration": visit.format_duration(
                delta=(visit.leaved_at - visit.entered_at)
            ),
            "is_strange": visit.is_strange(),
        }
        for visit in passcard.visit_set.all()
    ]

    return render(
        request,
        "passcard_info.html",
        {
            "passcard": passcard,
            "passcard_visits": passcard_visits,
        },
    )
