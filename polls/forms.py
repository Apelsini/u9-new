from django import forms
from django.forms import ModelForm, Textarea
from django.forms.widgets import HiddenInput, TextInput
from .models import Urlentry, Leads

# class DateToFromForm(ModelForm):
#     class Meta:
#         model = Urlentry
#         fields = ['datetime_available_from', 'datetime_available_to']

class UrlentryForm(ModelForm):
    class Meta:
        model = Urlentry
        fields = ['url_text', 'author', 'url_id', 'datetime_available_from', 'datetime_available_to', 'partner_ads','qr_code','snapshot']
        widgets = {'url_text': Textarea(attrs={'style':'width: 100%; border-color:#d3dce5; border-radius: 20px; border: 2px solid #d3dce5;'})   #, 'cols': 40
                   }
    def __init__(self, *args, **kwargs):
        hide_condition = kwargs.pop('hide_condition', None)
        limited_condition = kwargs.pop('limited_condition', None)
        super(UrlentryForm, self).__init__(*args, **kwargs)
        if hide_condition:
            self.fields['author'].widget = HiddenInput()
            self.fields['url_id'].widget = HiddenInput()
            self.fields['url_id'].required = False
            self.fields['url_text'].widget = TextInput()
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
        if limited_condition:
            del self.fields['author']
            #self.fields['author'].widget = HiddenInput()
            #self.fields['author'].required = False
            self.fields['url_id'].widget = HiddenInput()
            self.fields['url_id'].required = False
            self.fields['qr_code'].widget = HiddenInput()
            self.fields['qr_code'].required = False
            self.fields['snapshot'].widget = HiddenInput()
            self.fields['snapshot'].required = False
            self.fields['partner_ads'].widget = HiddenInput()
            self.fields['partner_ads'].required = False

class UrlentryFormShort(ModelForm):
    class Meta:
        model = Urlentry
        fields = ['url_text', 'partner_ads']
    def __init__(self, *args, **kwargs):
        super(UrlentryFormShort, self).__init__(*args, **kwargs)
        self.fields['url_text'].widget = HiddenInput()
        self.fields['partner_ads'].widget = HiddenInput()
        self.fields['partner_ads'].required = False
        #self.fields['datetime_available_from'].required = False
        #self.fields['datetime_available_to'].required = False

# iterable
POLLING_CHOICES =(
("1", "Every 15 min"),
("2", "Every 30 min"),
("3", "Every 60 min"),
("4", "Every 2 hours"),
("5", "Every 4 hours"),
("6", "Every 8 hours"),
("7", "Every 24 hours"),
("8", "Every 2 days"),
("9", "Every 4 days"),
("10", "Every 7 days"),
)

class WebrecordsForm(forms.Form):
    url = forms.CharField(max_length=1000, label='')
    polling_frequency = forms.ChoiceField(label='', choices = POLLING_CHOICES)
    notifycb = forms.BooleanField(label='', required=False)
    code100cb = forms.BooleanField(label='Codes 1xx: 100 Continue, 101 Switching Protocols, 102 Processing (WebDAV), 103 Early Hints', required=False)
    code200cb = forms.BooleanField(label='Codes 2xx: 200 OK, 201 Created, 202 Accepted, 203 Non-Authoritative Information, etc.', required=False)
    code300cb = forms.BooleanField(label='Codes of redirection 3xx: 300 Multiple Choices, 301 Moved Permanently, 302 Found, etc.', required=False)
    code400cb = forms.BooleanField(
        label='Error Codes 4xx: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, etc.', required=False)
    code500cb = forms.BooleanField(
        label='Error Codes 5xx: 500 Internal Server Error, 501 Not Implemented, 502 Bad Gateway, 503 Service Unavailable, etc.', required=False)
    widgets = {'url': Textarea(attrs={'rows': 3, 'style': 'width: 100%;'}),
               }

class LeadsForm(ModelForm):
    class Meta:
        model = Leads
        fields = ['follower_info']



