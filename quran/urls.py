from django.conf.urls import *
from . import views


urlpatterns = [
    url(r'^$', views.index, name='quran_index'),
    url(r'^(?P<sura_number>\d+)/$', views.get_sura, name='quran_sura'),
    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', views.get_aya, name='quran_aya'),
    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/(?P<word_number>\d+)/$', views.get_word, name='quran_word'),

    url(r'^lemma/(?P<lemma_id>\d+)/$', views.get_lemma, name='quran_lemma'),
    url(r'^root/(?P<root_id>\d+)/$', views.get_root, name='quran_root'),
    url(r'^root/$', views.root_index, name='quran_root_list'),

    url(r'^settings/$', views.settings, name='quran_settings')
]