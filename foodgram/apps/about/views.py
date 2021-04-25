from django.shortcuts import render
from django.views.generic.base import TemplateView


class About(TemplateView):
    template_name = 'static_page/about.html'


class About_tech(TemplateView):
    template_name = 'static_page/about_tech.html'


class About_assistant(TemplateView):
    template_name = 'static_page/about_assistant.html'


def page_not_found(request, exception):

    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
