"""urls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
# from .views import *
#from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# from polls import *
# from polls.views import *


from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('reset/<uidb64>/<token>/', view=auth_views.PasswordResetConfirmView.as_view(template_name='authentication/reset_password_done.html'), name='password_reset_confirm'),
    path('reset_password_sent/', view=auth_views.PasswordResetDoneView.as_view(template_name='authentication/reset_password_sent.html'), name='password_reset_done'),
    path('reset_password_complete/', view=auth_views.PasswordResetCompleteView.as_view(template_name='authentication/reset_password_complete.html'), name='password_reset_complete'),
    path('auth/', include('authentication.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)