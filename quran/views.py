from django.db.models import Prefetch
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response

from quran.models import *


def index(request, template_name='quran/index.html'):
    suras = get_list_or_404(Sura)
    return render_to_response(template_name, {'suras': suras})


def get_sura(request, sura_number, translation_id=2, template_name='quran/sura.html'):
    translation = None
    if translation_id:
        translation = Translation.objects.get(id=translation_id)
    ayas = Aya.objects.filter(sura__number=sura_number).prefetch_related(Prefetch('translations', queryset=AyaTranslation.objects.filter(translation=translation)))
    return render_to_response(template_name, {'ayas': ayas})


def get_aya(request, sura_number, aya_number, translation_id=2, template_name='quran/aya.html'):
    aya = Aya.objects.filter(sura__number=sura_number, number=aya_number).prefetch_related(
        Prefetch('translations', queryset=AyaTranslation.objects.filter(translation=translation_id)))
    return render_to_response(template_name, {'aya': aya[0]})


def get_word(request, sura_number, aya_number, word_number, translation_id=2, template_name='quran/word.html'):
    aya = Aya.objects.filter(sura__number=sura_number, number=aya_number)\
        .prefetch_related(Prefetch('translations', queryset=AyaTranslation.objects.filter(translation=translation_id)))
    word = Word.objects.filter(aya=aya, number=word_number).prefetch_related()  # todo cant see extent of data brought
    ayas = Aya.objects.filter(words__utext=word[0].utext)\
        .order_by('sura_id', 'number')\
        .prefetch_related(Prefetch('translations', queryset=AyaTranslation.objects.filter(translation=translation_id))) #  # other ayas with same word
    return render_to_response(template_name, {'word': word[0], 'aya': aya[0], 'ayas': ayas })


def get_lemma(request, lemma_id, translation=2, template_name='quran/lemma.html'):
    lemma = get_object_or_404(Lemma, pk=lemma_id)
    words = lemma.words.all().select_related('aya')
    return render_to_response(template_name, {'lemma': lemma, 'words': words})


def get_root(request, root_id, template_name='quran/root.html'):
    lemmas = Lemma.objects.filter(root__id=root_id).prefetch_related('words__aya')
    return render_to_response(template_name, {'lemmas': lemmas})  # , 'ayas': ayas


def root_index(request, template_name='quran/root_index.html'):
    roots = Root.objects.all().order_by('utext')
    return render_to_response(template_name, {'roots': roots})
