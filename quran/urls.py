from django.conf.urls import *
from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='quran_index'),
    url(r'^(?P<sura_number>\d+)/$', SuraView.as_view(), name='quran_sura'),
    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', AyaView.as_view(), name='quran_aya'),
    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/(?P<word_number>\d+)/$', WordView.as_view(), name='quran_word'),

    url(r'^page/(?P<page_number>\d+)/$', PageView.as_view(), name='quran_page'),
    # can override the template as PageView.as_view(template_name='your_custom_template')

    url(r'^lemma/(?P<lemma_id>\d+)/$', LemmaView.as_view(), name='quran_lemma'),
    url(r'^root/(?P<root_id>\d+)/$', RootView.as_view(), name='quran_root'),
    url(r'^root/$', RootIndexView.as_view(), name='quran_root_index'),

    url(r'^settings/$', settings, name='quran_settings')
]