from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^questions/', include('inquire.questions.urls', namespace="questions")),
    url(r'^accounts/', include('inquire.profiles.urls', namespace='profiles')),
]
