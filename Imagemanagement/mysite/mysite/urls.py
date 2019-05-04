"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
# from django.urls import path
from ImageManagement import views
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls.static import static
from django.conf import settings


# all the urls defined here
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls')),
    url(r'^index/strains/(?P<strain>[\w\-]+)/$', views.getStrains),
    url(r'^index/strains/(?P<strain>[\w\-]+)/(?P<stage>[\w\-]+)/$', views.getStrain_stage),
    url(r'^index/strains/(?P<strain>[\w\-]+)/(?P<stage>[\w\-]+)/(?P<imageid>[\w\-]+)/$', views.getImageDetails),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)