from django.urls import path
from . import views
#limit class views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

app_name = 'polls'
urlpatterns = [
    path('', view=views.IndexView.as_view(), name='index'),
    path('a/new/', view=login_required(views.create_urls, login_url=reverse_lazy('auth:login')), name='new'),#views.create_urls
    path('a/update/<int:pk>/', view=views.update_urlentry, name="update"),
    path('a/delete/<int:pk>/', view=login_required(views.DeleteUrlentry.as_view(), login_url=reverse_lazy('auth:login')), name='delete'),
    path('details/<int:pk>/', view=login_required(views.DetailView.as_view(), login_url=reverse_lazy('auth:login')), name='detail'),
    path('a/<int:pk>/results/', view=login_required(views.results_urlentry, login_url=reverse_lazy('auth:login')), name='results'),
    path('a/<int:pk>/results/get', view=views.ClicksView.as_view(), name='get'),
    path('a/<int:pk>/results/get/<str:datefrom>/<str:dateto>/', views.get_urlentry_count, name='get_urlentry_count'),
    #old links redirects
    path('polls/<int:pk>/results/', view=login_required(views.results_urlentry, login_url=reverse_lazy('auth:login')),
         name='results'),
    path('polls/<int:pk>/results/get', view=views.ClicksView.as_view(), name='get'),
    path('a/apps', view=views.AppsView.as_view(), name='apps'),
    path('a/webchecker', view=login_required(views.webchecker, login_url=reverse_lazy('auth:login')), name='webchecker'),
    path('a/webchecker/add', view=login_required(views.webchecker_add, login_url=reverse_lazy('auth:login')),
         name='webcheckeradd'),
    path('a/webchecker/editdelete/<int:pk>', view=login_required(views.webchecker_editdelete, login_url=reverse_lazy('auth:login')),
         name='webcheckereditdelete'),
    path('a/webchecker/delete/<int:pk>',
         view=login_required(views.webchecker_delete, login_url=reverse_lazy('auth:login')),
         name='webcheckerdelete'),
    #path('m/<str:hash>/<str:hash>/', view=views.add_lead_and_redirect, name='msgnosubj'),
    #path('m/<str:hash>/<str:hash>/<str:hash>/', view=views.add_lead_and_redirect, name='msgsubj'),
    #path('notify/donotify', view=views.NotifyView.as_view(), name='donotify'),
    path('<str:hash>/', view=views.add_lead_and_redirect, name='short'),
]