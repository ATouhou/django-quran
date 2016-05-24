from django.db.models import Prefetch
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response

from quran.load import import_morphology
from quran.models import *


def index(request, template_name='quran/index.html'):
    suras = get_list_or_404(Sura)
    return render_to_response(template_name, {'suras': suras})

def get_sura(request, sura_number, translation=2, template_name='quran/sura.html'):
    sura = get_object_or_404(Sura, number=sura_number)
    ayas = sura.ayas.all()
    if translation:
        translations = sura.translations.filter(translation=translation)
        ayas = zip(ayas, translations)
    return render_to_response(template_name, {'sura': sura, 'ayas': ayas})

def get_aya(request, sura_number, aya_number, translation=2, template_name='quran/aya.html'):
    sura = get_object_or_404(Sura, number=sura_number)
    aya = get_object_or_404(Aya, sura=sura, number=aya_number)
    translated_aya = get_object_or_404(AyaTranslation, aya=aya, translation=translation)
    words = aya.words.all()
    return render_to_response(template_name, {'sura': sura, 'aya': aya, 'translation': translated_aya, 'words': words})

def get_word(request, sura_number, aya_number, word_number, translation=2, template_name='quran/word.html'):
    aya = get_object_or_404(Aya, sura=sura_number, number=aya_number)
    translated_aya = get_object_or_404(AyaTranslation, aya=aya, translation=translation)
    word = Word.objects.filter(aya=aya, number=word_number).prefetch_related() # todo cant see extent of data brought
    return render_to_response(template_name, {'word': word[0], 'aya': aya, 'translation': translated_aya})

def get_lemma(request, lemma_id, translation=2, template_name='quran/lemma.html'):
    lemma = get_object_or_404(Lemma, pk=lemma_id)
    words = lemma.words.all()
    ayas = Aya.objects.filter(words__lemma__id = lemma_id).distinct()
    # todo: add translation
    return render_to_response(template_name, {'lemma': lemma, 'words': words, 'ayas': ayas})

def get_root(request, root_id, template_name='quran/root.html'):
    lemmas = Lemma.objects.filter(root__id=root_id).prefetch_related('words__aya')
    return render_to_response(template_name, {'lemmas': lemmas})  # , 'ayas': ayas

def root_index(request, template_name='quran/root_index.html'):
    roots = Root.objects.all().order_by('utext')
    return render_to_response(template_name, {'roots': roots})