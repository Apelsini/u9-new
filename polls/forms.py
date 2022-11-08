from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from .models import Urlentry, Leads

# class DateToFromForm(ModelForm):
#     class Meta:
#         model = Urlentry
#         fields = ['datetime_available_from', 'datetime_available_to']

class UrlentryForm(ModelForm):
    class Meta:
        model = Urlentry
        fields = ['url_text', 'author', 'url_id', 'datetime_available_from', 'datetime_available_to', 'partner_ads','qr_code','snapshot']
    def __init__(self, *args, **kwargs):
        hide_condition = kwargs.pop('hide_condition', None)
        super(UrlentryForm, self).__init__(*args, **kwargs)
        if hide_condition:
            self.fields['author'].widget = HiddenInput()
            self.fields['url_id'].widget = HiddenInput()
            self.fields['url_id'].required = False
            self.fields['datetime_available_from'].widget = HiddenInput()
            self.fields['datetime_available_from'].required = False
            self.fields['datetime_available_to'].widget = HiddenInput()
            self.fields['datetime_available_to'].required = False
            self.fields['partner_ads'].widget = HiddenInput()
            self.fields['partner_ads'].required = False
            self.fields['qr_code'].widget = HiddenInput()
            self.fields['qr_code'].required = False
            self.fields['snapshot'].widget = HiddenInput()
            self.fields['snapshot'].required = False
            # or alternately:  del self.fields['fieldname']  to remove it from the form altogether.

class UrlentryFormShort(ModelForm):
    class Meta:
        model = Urlentry
        fields = ['url_text', 'partner_ads']
    def __init__(self, *args, **kwargs):
        super(UrlentryFormShort, self).__init__(*args, **kwargs)
        self.fields['url_text'].widget = HiddenInput()
        self.fields['partner_ads'].widget = HiddenInput()
        #self.fields['datetime_available_from'].required = False
        #self.fields['datetime_available_to'].required = False

class LeadsForm(ModelForm):
    class Meta:
        model = Leads
        fields = ['follower_info']
