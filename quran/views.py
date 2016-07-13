from django.db.models import Prefetch
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.views.generic import TemplateView

from quran.models import *


class IndexView(TemplateView):
    template_name = 'quran/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        suras = get_list_or_404(Sura)
        context['suras'] = suras
        return context


class SuraView(TemplateView):
    template_name = 'quran/sura.html'
    def get_context_data(self, sura_number, **kwargs):
        context = super(SuraView, self).get_context_data(**kwargs)
        ayas = Aya.objects.filter(sura__number=sura_number)\
            .prefetch_related(prefetch_aya_translations(self.request))
        context['ayas'] = ayas
        return context


class PageView(TemplateView):
    template_name='quran/page.html'
    def get_context_data(self, page_number, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        page = Page.objects.get(number=page_number)

        ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id)\
            .prefetch_related(prefetch_aya_translations(self.request))
        context['ayas'] = ayas
        context['show_word_meanings'] = get_setting(self.request, 'show_word_meanings')
        context['page_number'] = int(page_number)
        return context


class AyaView(TemplateView):
    template_name='quran/aya.html'
    def get_context_data(self, sura_number, aya_number, **kwargs):
        context = super(AyaView, self).get_context_data(**kwargs)
        aya = Aya.objects.filter(sura__number=sura_number, number=aya_number)\
            .prefetch_related(prefetch_aya_translations(self.request))
        context['aya'] = aya[0]
        return context


class WordView(TemplateView):
    template_name='quran/word.html'
    def get_context_data(self, sura_number, aya_number, word_number, **kwargs):
        context = super(WordView, self).get_context_data(**kwargs)
        aya = Aya.objects.filter(sura__number=sura_number, number=aya_number) \
            .prefetch_related(prefetch_aya_translations(self.request))
        word = Word.objects.filter(aya=aya, number=word_number).prefetch_related()  # todo cant see extent of data brought
        ayas = Aya.objects.filter(words__distinct_word=word[0].distinct_word) \
            .order_by('sura_id', 'number') \
            .prefetch_related(prefetch_aya_translations(self.request))  # other ayas with same word
        context['word'] = word[0]
        context['aya'] = aya[0]
        context['ayas'] = ayas
        return context


class LemmaView(TemplateView):
    template_name='quran/lemma.html'
    def get_context_data(self, lemma_id, **kwargs):
        context = super(LemmaView, self).get_context_data(**kwargs)
        lemma = get_object_or_404(Lemma, pk=lemma_id)
        aya_translation_queryset = AyaTranslation.objects.filter(translation_id=get_setting(self.request, 'translation_type'))
        words = lemma.words.all() \
            .order_by('sura_id', 'aya_id') \
            .prefetch_related('aya') \
            .prefetch_related(Prefetch('aya__translations', queryset=aya_translation_queryset))
        context['lemma'] = lemma
        context['words'] = words
        return context


class RootView(TemplateView):
    template_name='quran/root.html'
    def get_context_data(self, root_id, **kwargs):
        context = super(RootView, self).get_context_data(**kwargs)
        lemmas = Lemma.objects.filter(root__id=root_id)\
            .prefetch_related('words__aya')\
            .prefetch_related(Prefetch('words__aya__translations', queryset=AyaTranslation.objects.filter(translation_id=get_setting(self.request, 'translation_type'))))
        context['lemmas'] = lemmas  # , 'ayas': ayas
        return context


class RootIndexView(TemplateView):
    template_name = 'quran/root_index.html'
    def get_context_data(self, **kwargs):
        context = super(RootIndexView, self).get_context_data(**kwargs)
        roots = Root.objects.all().order_by('utext')
        context['roots'] = roots
        return context


settings_list = {
    'translation_type': 1, #Translation.objects.first().id, # problem for migrating to another server
    'show_translation': False,
    'show_word_meanings': False,
}

# function to set settings from url
def settings(request):
    for setting, default in settings_list.items():
        if request.GET.get(setting, None):
            request.session[setting] = request.GET.get(setting, None)
            if request.session[setting].lower() == 'false':
                request.session[setting] = False
    return redirect('quran_index')

# to be overridden
def get_setting(request, setting):
    if not setting in request.session:
        request.session[setting] = settings_list[setting]
    return request.session.get(setting)


def prefetch_aya_translations(request):
    translation_id = get_setting(request, 'translation_type')
    return Prefetch('translations', queryset=AyaTranslation.objects.filter(translation_id=translation_id))

