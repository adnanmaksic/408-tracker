import os

from django.contrib import messages
from django.shortcuts import render

from .canvas_api import CanvasAPIError, CanvasClient


def dashboard(request):
    client = CanvasClient(
        os.getenv(
            "CANVAS_BASE_URL",
            "https://boisestatecanvas.instructure.com",
        ),
        os.getenv("CANVAS_API_TOKEN", ""),
    )

    try:
        courses = client.get_courses()
    except CanvasAPIError as error:
        messages.error(request, str(error))
        return render(
            request,
            "tracker/dashboard.html",
            {"courses": []},
        )

    assignments = []
    selected_course = request.GET.get("course_id")

    if selected_course:
        try:
            assignments = client.get_assignments(selected_course)
        except CanvasAPIError as error:
            messages.error(request, str(error))

    return render(
        request,
        "tracker/dashboard.html",
        {
            "courses": courses,
            "assignments": assignments,
            "selected_course": selected_course,
        },
    )