from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from contact.forms import ContactForm


class ContactView(SuccessMessageMixin, FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:thanks')
    success_message = "Thanks %(name)s, your message has been sent! I will try to answer as soon as possible."
    initial = {}

    def form_valid(self, form):
        # TODO set and retrieve cookie data, write custom get_initial() method
        response = super().form_valid(form)
        form.send_email()
        # self.initial['name'] = form.cleaned_data.get('name')
        # self.initial['email'] = form.cleaned_data.get('email')
        return response


class ThanksView(TemplateView):
    template_name = 'thanks.html'

