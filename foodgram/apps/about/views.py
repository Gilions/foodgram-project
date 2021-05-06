from django.views.generic.base import TemplateView


class About(TemplateView):
    template_name = 'static_page/about.html'


class AboutTech(TemplateView):
    template_name = 'static_page/about_tech.html'


class AboutAssistant(TemplateView):
    template_name = 'static_page/about_assistant.html'
