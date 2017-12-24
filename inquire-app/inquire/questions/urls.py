from django.conf.urls import url

from inquire.questions import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^ask/$', views.goto_add_page, name='ask'),
    url(r'^add_question/$', views.add_question, name='ask_question'),
    url(r'^(?P<question_id>\d+)/answer/$', views.goto_answer_page, name='answer'),
    url(r'^(?P<question_id>\d+)/add_answer/$', views.add_answer, name='answer_question'),
    url(r'^(?P<question_id>\d+)/edit_question_page/$', views.edit_question_page, name='edit_question_page'),
    url(r'^(?P<question_id>\d+)/edit_question/$', views.edit_question, name='edit_question'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/edit_answer_page/$', views.edit_answer_page, name='edit_answer_page'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/edit_answer/$', views.edit_answer, name='edit_answer'),
    url(r'^(?P<tag_id>\d+)/question_group_by_tag/$', views.tag_handler, name='tag_handler'),
    url(r'^(?P<question_id>\d+)/rss/$', views.rss, name='rss'),
]
