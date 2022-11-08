from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Urlentry, Leads
from django.utils import timezone
from .forms import UrlentryForm, LeadsForm, UrlentryFormShort
#limiting user view for users not logged in
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.utils.decorators import method_decorator
from authentication.decorators import allowed_users
from django.contrib.auth.models import Group, User
from django.contrib import messages

#supporting functions
def countme(iter):
    count=0
    for i in iter:
        count=count+1
    return count

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # context_object_name = 'questions_list'
    # def get_queryset(self):
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context_object_name = 'links_list'
    def get_queryset(self):
        return Urlentry.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')[:10]

@method_decorator(allowed_users(allowed_roles=['customer','admin']), name='dispatch')
class CreateUrlentry(generic.CreateView):
    model = Urlentry
    fields = ['url_text']
    template_name = 'polls/new_question.html'
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
            urlentry.datetime_available_to = timezone.now()
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
        return render(request, 'polls/question_choices.html',{
        'urlentry_form': urlentry_form,
        'formset': formset
        })

@login_required(login_url=reverse_lazy('auth:login'))
def update_urlentry(request, pk):
    urlentry = get_object_or_404(Urlentry, pk=pk)
    urlentry_formset=inlineformset_factory(Urlentry, Leads, fields=['follower_info'], extra=0)
    #urlentry_formset = formset_factory(Urlentry)
    formset=urlentry_formset(request.POST, instance=urlentry)
    #, fields=['url_text', 'partner_ads', 'qr_code', 'snapshot', 'datetime_available_from', 'datetime_available_to', 'follower_info'],
   # ['url_text', 'url_short', 'author', 'url_id', 'create_date', 'datetime_available_to',
   #  'partner_ads', 'qr_code', 'snapshot']

    if request.method == "POST":
        urlentry_form = UrlentryFormShort(request.POST, instance=urlentry)
        if urlentry_form.is_valid():
            urlentry = urlentry_form.save(commit=False)
            urlentry.save()
        redirect('polls:detail', pk=urlentry.pk)
        #else:
         #   messages.error(request, urlentry_form.error)
    else:
        urlentry_form = UrlentryForm(instance=urlentry)
        formset = urlentry_formset(instance=urlentry)
        redirect('polls:detail', pk=urlentry.pk)
    #         render(request, 'polls/question_choices.html',{
    #    'question_form': urlentry_form,
    #    'formset': formset
    # })
    return     redirect('polls:detail', pk=urlentry.pk)


# view to process short links like  localhost:8000/addb
def add_lead_and_redirect(request, hash):
    urlentry = get_object_or_404(Urlentry, url_short=hash)
    fol_info=''
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
          follower_fromwhere = request.META['REMOTE_ADDR']).save()
    if urlentry.partner_ads!="":
          return render(request, 'polls/frame.html',{
          'frame_block': urlentry.partner_ads,
          'body_block': urlentry.url_text,
          })
    return HttpResponseRedirect(urlentry.url_text)