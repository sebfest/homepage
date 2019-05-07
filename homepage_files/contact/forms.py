from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=100,
        label='Your name:',
        help_text='Your name',
        widget=forms.TextInput(attrs={'placeholder': ''}),
    )
    email = forms.EmailField(
        required=True,
        label='Your e-mail:',
        help_text='A valid email address, please.',
        widget = forms.TextInput(attrs={'placeholder': ''}),
    )
    message = forms.CharField(
        required=True,
        label='Your message:',
        help_text='Your message',
        widget=forms.Textarea(attrs={'placeholder': ''}),
    )

    def send_email(self):
        """
        Sends an e-mail
        :return: None
        """
        send_mail(
            self.cleaned_data.get('name'),
            self.cleaned_data.get('message'),
            self.cleaned_data.get('email'),
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
