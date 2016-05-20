import re
import unittest
from os import path
from xml.dom.minidom import parse, parseString
from django.db import transaction

from quran.models import *
from quran.buckwalter import *


def path_to(fn):
    return path.join(path.dirname(__file__), fn)

@transaction.atomic
def import_quran():
    quran_data = parse(path_to('tanzil/quran-data.xml'))
    quran = parse(path_to('tanzil/quran-uthmani.xml'))
    sura_datas = quran_data.getElementsByTagName('sura')

    for sura_data in sura_datas:
        index = int(sura_data.getAttribute('index'))
        ayas = sura_data.getAttribute('ayas')
        name = sura_data.getAttribute('name')
        tname = sura_data.getAttribute('tname')
        ename = sura_data.getAttribute('ename')
        type_ = sura_data.getAttribute('type')
        order = int(sura_data.getAttribute('order'))
        rukus = int(sura_data.getAttribute('rukus'))

        sura_model = Sura(number=index, name=name, tname=tname, ename=ename, type=type_, order=order, rukus=rukus, aya_number=ayas)

        sura = quran.getElementsByTagName('sura')[index - 1]
        assert int(sura.getAttribute('index')) == sura_model.number
        sura_model.save()

        ayas = sura.getElementsByTagName('aya')
        bismillah = ayas[0].getAttribute('bismillah')
        for aya in ayas:
            index = int(aya.getAttribute('index'))
            text = aya.getAttribute('text')
            aya_model = Aya(sura=sura_model, number=index, text=text, bismillah=bismillah)
            aya_model.save()
            print ("%d:%d" % (sura_model.number, index))


@transaction.atomic
def import_translation_txt(path_, translation):
    print ("Importing %s translation" % translation.name)
    f = open(path_)
    ayas = Aya.objects.all()
    for aya in ayas:
        line = f.readline()
        if len(line) <= 1:
            raise Exception('Translation file [%s] ended preemtively on aya %d:%d' % (path_, aya.sura_id, aya.number))
        line = line.strip()
        t = AyaTranslation(sura=aya.sura, aya=aya, translation=translation, text=line)
        t.save()
        print ("[%s] %d:%d" % (translation.name, aya.sura_id, aya.number))


def import_translations():
    translator_data = open(path_to('zekr/translator_data.txt'))
    for line in translator_data.readlines():
        name,translator,source_name,source_url,filename = line.strip().split(';')
        translation = Translation(name=name, translator=translator, source_name=source_name, source_url=source_url)
        translation.save()
        import_translation_txt(path_to('zekr/%s' % filename), translation)


def import_morphology():
    sura = Sura.objects.get(number=2)
    aya = Aya.objects.get(sura=sura, number=2) # any aya except the first.
    word = Word(number=-1) # non existent word to begin with
    f = open(path_to('corpus/quranic-corpus-morphology-0.4.txt'))

    line = f.readline()
    while len(line) > 0:
        parts = line.strip().split('\t')
        numbers = parts[0].split('(:)')

        try:
            sura_number = int(numbers[0])
            aya_number = int(numbers[1])
            word_number = int(numbers[2])
            segment_number = int(numbers[3])
        except ValueError:
            line = f.readline()
            continue

        text = parts[1]
        pos = parts[2]
        morphology = parts[3].split('|')

        if word_number is not word.number:
            if aya_number is not aya.number:
                if sura_number is not sura.number:
                    sura = Sura.objects.get(number=sura_number)
                aya = Aya.objects.get(sura=sura, number=aya_number)
            word = Word.objects.get_or_create(number=word_number)
            # print ("[morphology] %d:%d" % (sura.number, aya.number))

        lemma_text = None
        root_text = None
        segment_props = {'pos': pos, 'text': text}
        for prop in morphology:
            if "LEM" in prop:
                lemma_text = prop[4:] # stash because it has to be done with the root (if any)
            if "ROOT" in prop:
                root_text = prop[5:] # stash
            else:
                decorate_segment(segment_props, prop)

        if lemma_text:
            root = None
            if root_text:
                root=Root.objects.get_or_create(text=root_text)
            segment_props.lemma = Lemma.objects.get_or_create(text=lemma_text, root=root)

        segment=Segment.objects.get_or_create(**segment_props)
        word_segment = WordSegment(word=word, number=segment_number, segment=segment)
        word_segment.save()

        line = f.readline()


def decorate_segment(props, prop):
    skip = ["wa+", "Al+", "POS", "l", "PCPL", "f", "w"]
    for item in skip:
        if item in prop:
            return

    if "LEM" in prop:
        props.lemma = Lemma.objects.get_or_create(text=prop[4:], root=props.root)
        return
    if "ROOT" in prop:
        if not props.lemma:
            print("root without lemma!")
        props.lemma.root = Root.objects.get_or_create(text=prop[5:])
        return

    if "MOOD" in prop:
        props.mood = prop[5:]
        return
    if "PRON" in prop:
        props.gender = prop[5:]
        return
    if "(" in prop:
        props.form = prop[1:-1]
        return
    if "SP" in prop:
        props.special = prop[3:]
        return

    if ":" not in prop:
        lists = {  # non-titled fields
            'gender': ["3MP", "3MD", "3MS", "3FP", "3FS", "3FD", "2MP", "2MD", "2MS", "2FP", "2FD", "2FS", "1S", "1P", "MP", "MS", "FP", "FS", "F"],
            'case': ["GEN", "ACC", "NOM"],
            'definite': ["DEF", "INDEF"],
            'tense': ["PERF", "IMPF", "IMPV"],
            'participle': ["ACT", "PASS", "VN"],
        }
        for name, list_ in lists:
            if prop in list_:
                props.name=prop
                return

    print("unknown header in: %", prop) # worst case - something left unresolved


def test_data(verbosity):
    verbosity = int(verbosity)
    print (verbosity)
    test_suite = unittest.TestLoader().loadTestsFromTestCase(DataIntegrityTestCase)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


class DataIntegrityTestCase(unittest.TestCase):
    def check_word(self, sura_number, aya_number, word_number, expected_word):
        sura = Sura.objects.get(number=sura_number)
        aya = sura.ayas.get(number=aya_number)
        word = aya.words.get(number=word_number)
        self.assertEquals(word.token, buckwalter_to_unicode(expected_word))

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