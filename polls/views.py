from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Urlentry, Leads, Webrecords
from django.utils import timezone
from .forms import UrlentryForm, LeadsForm, UrlentryFormShort, WebrecordsForm
#limiting user view for users not logged in
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.utils.decorators import method_decorator
from authentication.decorators import allowed_users
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from datetime import datetime, date
from django.shortcuts import render
from django.contrib.auth import get_user_model
import json
import os

#supporting functions
def countme(iter):
    count=0
    for i in iter:
        count=count+1
    return count

# Create your views here.
class IndexView(generic.ListView):    #Class-Based View
    template_name = 'polls/index.html'
    # context_object_name = 'questions_list'
    # def get_queryset(self):
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context_object_name = 'links_list'
    paginate_by = 15
    #def get_queryset(self):
    #    return Urlentry.objects.filter(create_date__lte=timezone.now()).order_by('-create_date') #[:10]
    def get_queryset(self):
        filter_url = self.request.GET.get('filter_url', '')
        all_users = get_user_model().objects.all()
        filter_authorcheck = self.request.GET.get('filter_author', '')
        filter_author = self.request.user  #deafult - existing user

        #User.objects.get(username=self.request.GET.get('filter_author', self.request.user))
        datfromm = timezone.now().replace(year=2022).strftime("%Y-%m-%d %H:%M")
        filter_datefrom =datetime.strptime(self.request.GET.get('filter_datefrom', datfromm),"%Y-%m-%d %H:%M")
        dattom = timezone.now().strftime("%Y-%m-%d %H:%M")
        filter_dateto = datetime.strptime(self.request.GET.get('filter_dateto', dattom), "%Y-%m-%d %H:%M")
        order = self.request.GET.get('orderby', '-create_date')
        page = self.request.GET.get('page', 1)
        if self.request.user.is_superuser:    #is superuser
            if filter_authorcheck == '' or filter_authorcheck == ' ' or filter_authorcheck == '/':
                new_context = Urlentry.objects.filter(
                    #author=filter_author,
                    url_text__contains=filter_url,  # __contains lookup
                    create_date__gte=filter_datefrom,
                    create_date__lte=filter_dateto,
                ).order_by(order)
            else:
                for usrr in all_users:
                    if filter_authorcheck in usrr.username:
                        filter_author = usrr  # if there is request for another user - then switch to another user
                new_context = Urlentry.objects.filter(
                    author=filter_author,
                    url_text__contains=filter_url,  # __contains lookup
                    create_date__gte=filter_datefrom,
                    create_date__lte=filter_dateto,
                    ).order_by(order)
        else:
            if not self.request.user.is_anonymous:
                new_context = Urlentry.objects.filter(
                        author=filter_author,
                        url_text__contains=filter_url,   #__contains lookup
                        create_date__gte=filter_datefrom,
                        create_date__lte=filter_dateto,
                        ).order_by(order)
            else:
                new_context = Urlentry.objects.filter(
                        #author=filter_author,
                        url_text__contains=filter_url,   #__contains lookup
                        create_date__gte=filter_datefrom,
                        create_date__lte=filter_dateto,
                        ).order_by(order)
        return new_context
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['filter_url'] = self.request.GET.get('filter_url', '')
        all_users = get_user_model().objects.all()

        allusrss = all_users[1].username
        context['filter_author'] = self.request.GET.get('filter_author', self.request.user.username)

        datfrom = timezone.now().replace(year=2022).strftime("%Y-%m-%d %H:%M")
        context['filter_datefrom'] = self.request.GET.get('filter_datefrom', datfrom)
        datto = timezone.now().strftime("%Y-%m-%d %H:%M")
        context['filter_dateto'] = self.request.GET.get('filter_dateto', datto )
        context['orderby'] = self.request.GET.get('orderby', '-create_date')
        if self.request.user.is_superuser:
            context['userlist'] = ''
        else:
            context['userlist'] = ''
        return context

@method_decorator(allowed_users(allowed_roles=['customer','admin']), name='dispatch')
class CreateUrlentry(generic.CreateView):
    model = Urlentry
    fields = ['url_text']
    template_name = 'polls/new_link.html'
    def form_valid(self, form):
        cd = form.cleaned_data
        form.instance.create_date = timezone.now()
        form.instance.author = self.request.user
        form.instance.url_id = countme(Urlentry.objects.all())
        if is_customer(self.request.user.id):
            form.instance.url_short = Urlentry.num_to_sym_registered(form.instance.url_id)
        else:
            form.instance.url_short = Urlentry.num_to_sym_unregistered(form.instance.url_id)
        form.instance.snapshot = 'https://api.screenshotmachine.com?key=7a0150&url='+cd['url_text']+'&dimension=1024x768'
        form.instance.qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='+cd['url_text']
        self.urlentry = form.save()
        form.instance.datetime_available_from = timezone.now()
        form.instance.datetime_available_to = timezone.now()
        form.instance.partner_ads = ''
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('polls:detail', args=(self.urlentry.id,))

class DetailView(generic.DetailView):
    model = Urlentry
    fields = ['url_text', 'author', 'url_id', 'datetime_available_from', 'datetime_available_to', 'partner_ads','qr_code','snapshot']
    template_name = 'polls/detail.html'

def detailview_urlentry(request, pk):
    urlentry = get_object_or_404(Urlentry, pk=pk)
    leads_list = [i for i in Leads.objects.all()]
    return      render(request, 'polls/results.html',{
    })

class ResultsView(generic.DetailView):
    model = Urlentry
    template_name = 'polls/results.html'

class ClicksView(generic.DetailView):
    model = Urlentry
    template_name = 'polls/clicks.html'

class AppsView(generic.ListView):    #Class-Based View
    model = Urlentry
    template_name = 'polls/apps.html'

class DeleteUrlentry(generic.DeleteView):
    model = Urlentry
    template_name = 'polls/delete_question.html'
    def get_success_url(self):
        return reverse('polls:index')

# create Url
@login_required(login_url=reverse_lazy('auth:login'))
def create_urls(request):
    urlentry_formset = inlineformset_factory(Urlentry, Leads, fields=['follower_info'], extra=0)
    formset = urlentry_formset()
    if request.method == "POST":
        urlentry_form = UrlentryForm(request.POST, hide_condition=True)
        if urlentry_form.is_valid():
            urlentry = urlentry_form.save(commit=False)
            urlentry.create_date = timezone.now()
            urlentry.author = request.user
            urlentry.url_id = countme(Urlentry.objects.all())
            urlentry.datetime_available_from = timezone.now()
            urlentry.datetime_available_to = urlentry.datetime_available_from
            urlentry.partner_ads = ''
            #urlentry.save()
            urlentry.url_short = Urlentry.num_to_sym_unregistered(urlentry.url_id)
            if request.user.is_staff:
                urlentry.url_short = Urlentry.num_to_sym_registered(urlentry.url_id)
            urlentry.snapshot = 'https://api.screenshotmachine.com?key=7a0150&url=' + str(urlentry_form[
                'url_text'])[73:].rstrip('</textarea>') + '&dimension=1024x768'
            urlentry.qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + str(urlentry_form[
                'url_text'])[73:].rstrip('</textarea>')
            urlentry.save()
           ############

            formset = urlentry_formset(request.POST, instance=urlentry)
            if formset.is_valid():
                formset.save()
                return redirect('polls:detail', pk=urlentry.pk)
    else:
        urlentry_form = UrlentryForm(hide_condition=True)
        formset = urlentry_formset()
        return render(request, 'polls/new_link.html',{
        'urlentry_form': urlentry_form,
        'formset': formset
        })

@login_required(login_url=reverse_lazy('auth:login'))
def update_urlentry(request, pk):
    urlentry = get_object_or_404(Urlentry, pk=pk)
    urlentry_formset=inlineformset_factory(Urlentry, Leads, fields=[], extra=0)
    #urlentry_formset = formset_factory(Urlentry)
    formset=urlentry_formset(request.POST, instance=urlentry)
    #, fields=['url_text', 'partner_ads', 'qr_code', 'snapshot',
    #'datetime_available_from', 'datetime_available_to', 'follower_info',
    #'url_text', 'url_short', 'author', 'url_id', 'create_date', 'datetime_available_to',
    #'partner_ads', 'qr_code', 'snapshot'])
    if request.method == "POST":
        urlentry_form = UrlentryForm(request.POST, instance=urlentry, limited_condition=True)
        if urlentry_form.is_valid():
            urlentry = urlentry_form.save(commit=False)
            urlentry.snapshot = 'https://api.screenshotmachine.com?key=7a0150&url=' + str(urlentry_form[
                'url_text'])[73:].rstrip('</textarea>') + '&dimension=1024x768'
            urlentry.qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + str(urlentry_form[
                'url_text'])[73:].rstrip('</textarea>')
            urlentry.save()
        else:
            messages.error(request, urlentry_form.errors)
        redirect('polls:detail', pk=urlentry.pk)
        #else:
         #   messages.error(request, urlentry_form.error)
    else:
        urlentry_form = UrlentryForm(instance=urlentry)
        formset = urlentry_formset(instance=urlentry)
        #datfromm = urlentry.datetime_available_from.strftime("%Y-%m-%d %H:%M")
        #urlentry_form.fields['datetime_available_from'] = datetime.strptime(datfromm, "%Y-%m-%d %H:%M")
        #dattomm = urlentry.datetime_available_to.strftime("%Y-%m-%d %H:%M")
        #urlentry_form.fields['datetime_available_to'] = datetime.strptime(dattomm, "%Y-%m-%d %H:%M")
        redirect('polls:detail', pk=urlentry.pk)
    #         render(request, 'polls/question_choices.html',{
    #    'question_form': urlentry_form,
    #    'formset': formset
    # })
    return     redirect('polls:detail', pk=urlentry.pk)


# view to process short links like  localhost:8000/addb
def add_lead_and_redirect(request, hash):
    if 'reset_password_sent' in hash:
        return render(request, 'authentication/reset_password_sent.html', {
        })
    if 'reset_password_complete' in hash:
        return render(request, 'authentication/reset_password_complete.html', {
        })
    urlentry = get_object_or_404(Urlentry, url_short=hash)
    d = urlentry.datetime_available_from
    datefromdig = int(time.mktime(d.timetuple())) * 1000
    fol_info=''
    dateto = urlentry.datetime_available_to.strftime("%Y-%m-%d %H:%M")
    try:
        if request.META['HTTP_REFERER']!=None:
            fol_info = request.META['HTTP_REFERER']
    except:
        pass
    if request.META['HTTP_HOST']!=None:
        fol_info = request.META['HTTP_HOST']
    Leads(urlentry=urlentry,
          follower_info=fol_info,
          follower_os_info = request.headers.get('User-Agent'),
          follower_fromwhere = request.META['REMOTE_ADDR']).save() # standard analytics
    render(request, 'polls/matomo.html', {})
    if urlentry.datetime_available_from != urlentry.datetime_available_to:
        #if there is need for redirection to 'premiere.html' or 'deprecated.html'
        if urlentry.datetime_available_from > timezone.now() and urlentry.datetime_available_to > timezone.now():
            # the urlentry has Premiere date
            return render(request, 'polls/premiere.html', {
                'datefromdig': datefromdig
            })
        if urlentry.datetime_available_from < timezone.now() and urlentry.datetime_available_to < timezone.now():
            # the urlentry already deprecated
            return render(request, 'polls/deprecated.html', {
                'dateto': dateto
            })

    if urlentry.partner_ads=="" or urlentry.partner_ads==" ":  #redirection to Customers frame with ads block
        pattern_html = 'polls/bframe.html' #no ads - usual redirection
    else:
        pattern_html = 'polls/frame.html'  # ads block redirection

    return render(request, pattern_html,{     # usual immediate redirection
          'id_block': urlentry.url_id,
          'frame_block':   urlentry.partner_ads,
          'body_block':  urlentry.url_text,
          })

    #HttpResponseRedirect(urlentry.url_text)

# list Webchecker records and log
@login_required(login_url=reverse_lazy('auth:login'))
def webchecker(request):
    webrecords = Webrecords.objects.all().filter(author=request.user)
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = '/cronlog.txt'
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as file:
        lines = file.readlines()
    pattern_html = 'polls/webcheck.html'
    return render(request, pattern_html, {  # usual immediate redirection
        'webrecords': webrecords,
        'lines': lines
    })

# add Webchecker record
@login_required(login_url=reverse_lazy('auth:login'))
def webchecker_add(request):
    pattern_html = 'polls/webcheck_add.html'
    if request.method == "POST":
        form = WebrecordsForm(request.POST)
        if form.is_valid():
            webrecord = Webrecords()
            cd = form.cleaned_data
            webrecord.author = request.user
            webrecord.websites = 'U9'
            webrecord.url = cd['url']
            webrecord.polling_frequency = cd['polling_frequency'][0:2]
            webrecord.notifycb = cd['notifycb']
            webrecord.code100cb = cd['code100cb']
            webrecord.code200cb = cd['code200cb']
            webrecord.code300cb = cd['code300cb']
            webrecord.code400cb = cd['code400cb']
            webrecord.code500cb = cd['code500cb']
            if not request.user.is_staff:  # only customers have unlimited webrecords, users have only 5
                counter = Webrecords.objects.all().filter(author=request.user).count()
                if counter > 4:
                    messages.error(request,
                                   'WARNING! New record was not created. Your user status allows only 5 webrecords. Contact the administrator to acquire Customer privileges with unlimited number of websites to check')
                else:
                    webrecord.save()
            else:
                webrecord.save()
            return redirect('polls:webchecker')
        else:
            messages.error(request, form.errors)
            return redirect('polls:webcheckeradd')
        #else:
         #   messages.error(request, urlentry_form.error)
    else:
        form = WebrecordsForm()
        return render(request, pattern_html, {  # usual immediate redirection
        'form': form,
    })

# edit or delete Webchecker record
@login_required(login_url=reverse_lazy('auth:login'))
def webchecker_editdelete(request, pk):
    pattern_html = 'polls/webcheck_editdelete.html'
    if request.method == "POST":
        form = WebrecordsForm(request.POST)
        if form.is_valid():
            webrecord = Webrecords.objects.all().filter(author=request.user,pk=pk).get()
            cd = form.cleaned_data
            if webrecord:
                webrecord.websites = 'U9'
                webrecord.url = cd['url']
                webrecord.polling_frequency = cd['polling_frequency'][0:2]
                webrecord.notifycb = cd['notifycb']
                webrecord.code100cb = cd['code100cb']
                webrecord.code200cb = cd['code200cb']
                webrecord.code300cb = cd['code300cb']
                webrecord.code400cb = cd['code400cb']
                webrecord.code500cb = cd['code500cb']
                webrecord.save()
                return redirect('polls:webchecker')
    else:
        webrecord = Webrecords.objects.all().filter(author=request.user,pk=pk).get()
        if webrecord:
            form = WebrecordsForm()
            form.fields['url'].initial = webrecord.url
            form.fields['polling_frequency'].initial = webrecord.polling_frequency
            form.fields['notifycb'].initial = webrecord.notifycb
            form.fields['code100cb'].initial = webrecord.code100cb
            form.fields['code200cb'].initial = webrecord.code200cb
            form.fields['code300cb'].initial = webrecord.code300cb
            form.fields['code400cb'].initial = webrecord.code400cb
            form.fields['code500cb'].initial = webrecord.code500cb
        else:
            form = WebrecordsForm()
            return redirect('polls:webcheckeradd')
        return render(request, pattern_html, {  # usual immediate redirection
        'form': form,
        'webrecord' : webrecord,
        })

# edit or delete Webchecker record
@login_required(login_url=reverse_lazy('auth:login'))
def webchecker_delete(request, pk):
    webrecord = Webrecords.objects.all().filter(author=request.user,pk=pk).get()
    if webrecord:
        webrecord.delete()
        messages.error(request, 'webrecord deleted successfully')
        return redirect('polls:webchecker')
    else:
        messages.error(request, 'WARNING! Failure when deleting the webrecord. It may be not existing under your account.')
        return redirect('polls:webchecker')
    return redirect('polls:webchecker')