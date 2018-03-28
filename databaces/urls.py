"""databaces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import app.views

# Examples:
# url(r'^$', 'databaces.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
url(r'^$', app.views.index, name='index'),
url(r'^index.html$', app.views.index, name='index'),
url(r'^register.html$', app.views.register, name='register'),
url(r'^dashboard.html$', app.views.dashboard, name='dashboard'),
url(r'^profile.html$', app.views.profile, name='profile'),
url(r'^submitrecipe.html', app.views.submitrecipe, name='submitrecipe'),
url(r'^search/', app.views.search, name='search'),
url(r'^edit/', app.views.edit, name='edit'),
url(r'^submitedit', app.views.submitedit, name='submitedit'),
url(r'^deleterecipe', app.views.deleterecipe, name='deleterecipe'),
url(r'^addrecipe', app.views.addrecipe, name='addrecipe'),
path('admin/', admin.site.urls)

]
