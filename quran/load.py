import unittest

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
        bismillah = ayas[0].getAttribute('bismillah')
        for aya in ayas:
            index = int(aya.getAttribute('index'))
            utext = aya.getAttribute('text')
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
    translator_data = open(path_to('data/zekr/translator_data.txt'))
    for line in translator_data.readlines():
        name, translator, source_name, source_url, filename = line.strip().split(';')
        translation = Translation(ttext=name, translator=translator, source_name=source_name, source_url=source_url)
        translation.save()
        import_translation_txt(path_to('data/zekr/%s' % filename), translation)


def import_morphology(test):
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

        if test and sura_number > 1:  # just do sura Fatiha if testing
            break

        # print("%d.%d.%d.%d" % (sura_number, aya_number, word_number, segment_number))

        ttext = parts[1]
        pos, created = Pos.objects.get_or_create(pk=parts[2])
        morphology = parts[3].split('|')

        if word_number is not word.number:
            if aya_number is not aya.number:
                if sura_number is not sura.number:
                    sura = Sura.objects.get(number=sura_number)
                    print("Sura: %d started,    Time passed: %s" % (sura_number, str(timedelta(seconds=time.time() - time_begin))))
                aya = Aya.objects.get(sura=sura, number=aya_number)
            word, created = Word.objects.get_or_create(sura=sura, aya=aya, number=word_number)
            # print ("[morphology] %d:%d" % (sura.number, aya.number))

        if not word.ttext:
            word.ttext = ttext
        else:
            word.ttext += ttext

        lemma_ttext = None
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
                    morphology = morphology[0].split(':')[0] # take the part before ":", part after : repeats POS
                prefix, created = Other.objects.get_or_create(pk=morphology[0], category='prefix')
                segment_props['other'] = prefix
        else:
            for prop in morphology:
                if "LEM" in prop:
                    lemma_ttext = prop[4:]  # stash because it has to be done with the root (if any)
                elif "ROOT" in prop:
                    root_ttext = prop[5:]  # stash
                else:
                    decorate_segment(segment_props, prop, segment_type)

            if lemma_ttext:
                root = None
                if root_ttext:
                    root, created = Root.objects.get_or_create(ttext=root_ttext)
                segment_props['lemma'], created = Lemma.objects.get_or_create(ttext=lemma_ttext, root=root)
            elif root_ttext:
                print("root without lemma: %s" % root_ttext)

        segment, created = Segment.objects.get_or_create(**segment_props)
        word_segment = WordSegment(word=word, number=segment_number, segment=segment, type=segment_type)
        word_segment.save()
        word.utext = get_unicode(word.ttext)
        word.save()  # to save word text
        line = f.readline()

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


def test_data(verbosity):
    verbosity = int(verbosity)
    print(verbosity)
    test_suite = unittest.TestLoader().loadTestsFromTestCase(DataIntegrityTestCase)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


class DataIntegrityTestCase(unittest.TestCase):
    def check_word(self, sura_number, aya_number, word_number, expected_word):
        sura = Sura.objects.get(number=sura_number)
        aya = sura.ayas.get(number=aya_number)
        word = aya.words.get(number=word_number)
        self.assertEquals(word.text, get_unicode(expected_word))

    def test_first_ayas(self):
        """
        Test the first ayas of some suras
        """
        self.check_word(1, 1, 3, u'{lr~aHoma`ni')
        self.check_word(2, 1, 1, u'Al^m^')
        self.check_word(114, 1, 1, u'qulo')

    def test_last_ayas(self):
        """
        Test the last ayas of some suras
        """
        self.check_word(1, 7, 2, u'{l~a*iyna')
        self.check_word(2, 286, 49, u'{loka`firiyna')
        self.check_word(114, 6, 3, u'wa{ln~aAsi')

    def test_yusuf_ali(self):
        """
        Test some ayas against Yusuf Ali
        """
        sura_number = 112
        aya_number = 4
        sura = Sura.objects.get(number=sura_number)
        aya = sura.ayas.get(number=aya_number)
        translation = Translation.objects.get(name='Yusuf Ali')
        t = aya.translations.get(translation=translation)
        self.assertEquals(t.text, 'And there is none like unto Him.')
