from django import forms
from .models import Client, Message, Mailing

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment'] # owner не включаем


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body'] # owner не включаем


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['first_send_time', 'end_time', 'message', 'clients']
        widgets = {
            'first_send_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.owner_id = kwargs.pop('owner_id', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        if self.owner_id:
            # Фильтруем queryset для message и clients по владельцу
            self.fields['message'].queryset = self.fields['message'].queryset.filter(owner_id=self.owner_id)
            self.fields['clients'].queryset = self.fields['clients'].queryset.filter(owner_id=self.owner_id)



