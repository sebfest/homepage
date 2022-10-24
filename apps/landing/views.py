from django.views.generic import TemplateView


class WelcomeView(TemplateView):
    template_name = 'landing/welcome.html'
    extra_context = {'header': 'Welcome'}


class DisclaimerView(TemplateView):
    template_name = 'landing/disclaimer.html'
    extra_context = {'header': 'Disclaimer'}
