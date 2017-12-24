from django.conf.urls import url
from django.contrib.auth.views import login, logout

from inquire.profiles.views import *


urlpatterns = [
    url(r'^register/$', register_user, name='register_user'),
    url(r'^register_success/$', register_success, name='register_success'),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^logout_success/$', logout_success, name="logout_success"),
    url(r'^profile/$', profile, name="profile"),
]
