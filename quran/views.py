from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from quran.models import *

def index(request, template_name='quran/index.html'):
    suras = get_list_or_404(Sura)
    return render_to_response(template_name, {'suras': suras})

def get_sura(request, sura_number, translation=1, template_name='quran/sura.html'):
    sura = get_object_or_404(Sura, number=sura_number)
    ayas = sura.ayas.all()
    if translation:
        translations = sura.translations.filter(translation=translation)
        ayas = zip(ayas, translations)
    return render_to_response(template_name, {'sura': sura, 'ayas': ayas})

def get_aya(request, sura_number, aya_number, translation=1, template_name='quran/aya.html'):
    sura = get_object_or_404(Sura, number=sura_number)
    aya = get_object_or_404(Aya, sura=sura, number=aya_number)
    translated_aya = get_object_or_404(AyaTranslation, aya=aya, translation=translation)
    words = aya.words.all()
    return render_to_response(template_name, {'sura': sura, 'aya': aya, 'translation': translated_aya, 'words': words})

def get_word(request, sura_number, aya_number, word_number, template_name='quran/word.html'):
    aya = get_object_or_404(Aya, sura=sura_number, number=aya_number)
    word = get_object_or_404(Word, aya=aya, number=word_number)
    root = word.root
    return render_to_response(template_name, {'word': word, 'aya': aya, 'root': root})

def get_lemma(request, lemma_id, template_name='quran/lemma.html'):
    lemma = get_object_or_404(Lemma, pk=lemma_id)
    root = lemma.root
    words = lemma.word_set.all()
    ayas = lemma.ayas.distinct()
    return render_to_response(template_name, {'lemma': lemma, 'root': root, 'words': words, 'ayas': ayas})

def get_root(request, root_id, template_name='quran/root.html'):
    root = get_object_or_404(Root, pk=root_id)
    lemmas = root.lemmas.all()
    ayas = root.ayas.distinct()
    return render_to_response(template_name, {'root': root, 'lemmas': lemmas, 'ayas': ayas})

def root_index(request, template_name='quran/root_index.html'):
    roots = Root.objects.all().order_by('letters')
    return render_to_response(template_name, {'roots': roots})