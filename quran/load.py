
from datetime import timedelta
import time
from os import path
from xml.dom.minidom import parse
from django.db import transaction
from django.apps import apps

from quran.models import *
from quran.buckwalter import *


def path_to(fn):
    return path.join(path.dirname(__file__), fn)


@transaction.atomic
def import_quran():
    print("----- importing quran -----")
    quran_data = parse(path_to('data/tanzil/quran-data.xml'))
    quran = parse(path_to('data/tanzil/quran-uthmani.xml'))
    sura_datas = quran_data.getElementsByTagName('sura')

    for sura_data in sura_datas:
        index = int(sura_data.getAttribute('index'))
        ayas = sura_data.getAttribute('ayas')
        uname = sura_data.getAttribute('name')
        tname = sura_data.getAttribute('tname')
        ename = sura_data.getAttribute('ename')
        type_ = sura_data.getAttribute('type')
        order = int(sura_data.getAttribute('order'))
        rukus = int(sura_data.getAttribute('rukus'))

        sura_model = Sura(number=index, utext=uname, ttext=tname, etext=ename, type=type_, order=order, rukus=rukus, aya_count=ayas)

        sura = quran.getElementsByTagName('sura')[index - 1]
        assert int(sura.getAttribute('index')) == sura_model.number
        sura_model.save()

        ayas = sura.getElementsByTagName('aya')
        for aya in ayas:
            index = int(aya.getAttribute('index'))
            utext = aya.getAttribute('text')
            bismillah = aya.getAttribute('bismillah')
            aya_model = Aya(sura=sura_model, number=index, utext=utext, bismillah=bismillah)
            aya_model.save()
        print("Loaded sura: %d" % sura_model.number)


@transaction.atomic
def import_translation_txt(path_, translation):
    print("Importing %s translation" % translation.ttext)
    f = open(path_)
    ayas = Aya.objects.all()
    for aya in ayas:
        line = f.readline()
        if len(line) <= 1:
            raise Exception('Translation file [%s] ended preemtively on aya %d:%d' % (path_, aya.sura_id, aya.number))
        line = line.strip()
        t = AyaTranslation(sura=aya.sura, aya=aya, translation=translation, ttext=line)
        t.save()
        if aya.number == 1:
            print("Loaded translation: [%s]     sura: %d" % (translation.ttext, aya.sura_id))


def import_translations():
    print("----- importing translations -----")
    translator_data = open(path_to('data/zekr/translator_data.txt'))
    for line in translator_data.readlines():
        name, translator, source_name, source_url, filename = line.strip().split(';')
        translation = Translation(ttext=name, translator=translator, source_name=source_name, source_url=source_url)
        translation.save()
        import_translation_txt(path_to('data/zekr/%s' % filename), translation)


def import_morphology(test=False):
    """
        some lemma's had trailing 2's which seemed to be bug, so in the below code they are removed
    """
    print("----- importing morphology -----")
    sura = Sura.objects.get(number=2)
    aya = Aya.objects.get(sura=sura, number=2)  # any aya except the first.
    word = Word(number=-1)  # non existent word to begin with
    f = open(path_to('data/corpus/quranic-corpus-morphology-0.4.txt'))

    time_begin = time.time()

    line = f.readline()
    while len(line) > 0:
        parts = line.strip().split('\t')
        numbers = parts[0]
        numbers = numbers[1:-1].split(':')  # throw first and last characters and split

        try:
            sura_number = int(numbers[0])
            aya_number = int(numbers[1])
            word_number = int(numbers[2])
            segment_number = int(numbers[3])
        except ValueError:
            line = f.readline()
            continue

        if test and 2 < sura_number < 114:  # just do sura Fatiha if testing
            line = f.readline()
            continue

        # print("%d.%d.%d.%d" % (sura_number, aya_number, word_number, segment_number))

        ttext = parts[1]
        pos, created = Pos.objects.get_or_create(pk=parts[2])
        morphology = parts[3].split('|')

        if word_number != word.number or aya_number != aya.number:
            if aya_number != aya.number:
                if sura_number != sura.number:
                    sura = Sura.objects.get(number=sura_number)
                    print("Sura: %d started,    Time passed: %s" % (sura_number, str(timedelta(seconds=time.time() - time_begin))))
                aya = Aya.objects.get(sura=sura, number=aya_number)
            if word.number != -1:  # non initial word
                word.utext = get_unicode(word.ttext)
                word.save()  # to save word text
            word, created = Word.objects.get_or_create(sura=sura, aya=aya, number=word_number)
            word.ttext = ttext
        else: # same word, keep adding
            word.ttext += ttext

        lemma_ttext = None
        lemma_meaning = None
        root_ttext = None
        segment_props = {
            'pos': pos,
            'ttext': ttext,
            'lemma': None,
            'mood': None,
            'gender': None,
            'form': None,
            'special': None,
            'case': None,
            'definite': None,
            'tense': None,
            'participle': None,
            'other': None,
        }

        segment_type = morphology[0].lower()  # prefix, stem, or suffix
        morphology = morphology[1:]

        if segment_type == 'prefix':
            if morphology.__len__() > 1:
                print("more than 1 tag in prefix: %s" % word)
            else:
                if ':' in morphology[0]:
                    morphology = morphology[0].split(':')[0]  # take the part before ":", part after : repeats POS
                prefix, created = Other.objects.get_or_create(pk=morphology[0], category='prefix')
                segment_props['other'] = prefix
        else:
            for prop in morphology:
                if "LEM" in prop:
                    lemma_ttext = prop[4:]  # stash because it has to be done with the root (if any)
                    """
                     homonyms: same spelling but different meanings, e.g., EaSaA عصا could mean both 'wand' and 'to rebel'.
                     it  seems like to work around some uniqueness constraint they just put a 2 to the end of second such item
                    """
                    if '2' in lemma_ttext:
                        lemma_ttext = lemma_ttext[0:-1]  # remove trailing 2 which seems to be bug
                        lemma_meaning = 2
                elif "ROOT" in prop:
                    root_ttext = prop[5:]  # stash
                else:
                    decorate_segment(segment_props, prop, segment_type)

            if lemma_ttext:
                root = None
                if root_ttext:
                    root, created = Root.objects.get_or_create(ttext=root_ttext)
                segment_props['lemma'], created = Lemma.objects.get_or_create(ttext=lemma_ttext, root=root, meaning=lemma_meaning)
                word.lemma = segment_props['lemma']
            elif root_ttext:
                print("root without lemma: %s" % root_ttext)

        segment, created = Segment.objects.get_or_create(**segment_props)
        word_segment = WordSegment(word=word, number=segment_number, segment=segment, type=segment_type)
        word_segment.save()
        line = f.readline()

    word.utext = get_unicode(word.ttext)  # to save the last word
    word.save()

    roots = Root.objects.all()
    for root in roots:
        root.utext = get_unicode(root.ttext)
        root.save()

    lemmas = Lemma.objects.all()
    for lemma in lemmas:
        lemma.utext = get_unicode(lemma.ttext)
        lemma.save()


def decorate_segment(segment_props, prop, segment_type):
    title = None
    skip = ["POS", "PCPL"]
    lists = {
        'Gender': ["3MP", "3MD", "3D", "3MS", "3FD", "3FP", "3FS",
                   "2MP", "2MD", "2D", "2MS", "2FD", "2FP", "2FS",
                   "1S", "1P", "MP", "MD", "MS", "FP", "FD", "FS", "F", "M", "P"],
        'Case': ["GEN", "ACC", "NOM"],
        'Definite': ["DEF", "INDEF"],
        'Tense': ["PERF", "IMPF", "IMPV"],
        'Participle': ["ACT", "PASS", "VN"],
    }

    if ':' in prop:  # titled
        prop = prop.split(':')
        title = prop[0]
        tag = prop[1]
        if title in skip:
            return
    else:  # non-titled
        tag = prop
        if prop in skip:
            return

    if segment_type == 'suffix' and tag not in lists['Gender']:
        segment_props['other'], created = Other.objects.get_or_create(pk=tag, category="suffix")
        return

    # titled fields
    if title == "MOOD":
        segment_props['mood'], created = Mood.objects.get_or_create(pk=tag)
        return
    if title == "PRON":
        segment_props['gender'], created = Gender.objects.get_or_create(pk=tag)
        return
    if "(" in tag:
        segment_props['form'], created = Form.objects.get_or_create(pk=tag[1:-1])
        return
    if title == "SP":
        segment_props['special'], created = Special.objects.get_or_create(pk=tag)
        return

    # non-titled fields
    if not title:
        for name, list_ in lists.items():
            if tag in list_:
                segment_props[name.lower()], created = apps.get_model(app_label='quran', model_name=name) \
                    .objects.get_or_create(pk=tag)
                return

    print("unknown header in: %s" % prop)  # worst case - something left unresolved

