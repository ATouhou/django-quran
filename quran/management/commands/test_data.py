import unittest

from django.core.management import BaseCommand

from quran.models import Word, AyaTranslation, Segment

from quran.buckwalter import get_unicode


def test_data(verbosity):
    verbosity = int(verbosity)
    print(verbosity)
    test_suite = unittest.TestLoader().loadTestsFromTestCase(DataIntegrityTestCase)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


class DataIntegrityTestCase(unittest.TestCase):

    @staticmethod
    def get_word(sura_number, aya_number, word_number):
        return Word.objects \
            .filter(number=word_number) \
            .filter(sura__number=sura_number) \
            .filter(aya__number=aya_number)

    def check_word(self, sura_number, aya_number, word_number, expected_word):
        word = self.get_word(sura_number, aya_number, word_number)
        self.assertEquals(word.__len__(), 1)
        self.assertEquals(word[0].text, get_unicode(expected_word))

    def check_lemma(self, sura_number, aya_number, word_number, expected_lemma):
        word = self.get_word(sura_number, aya_number, word_number)
        if expected_lemma == '':
            self.assertIsNone(word[0].lemma)
        else:
            self.assertEquals(word[0].lemma.text, get_unicode(expected_lemma))

    def check_root(self, sura_number, aya_number, word_number, expected_root):
        word = self.get_word(sura_number, aya_number, word_number)
        if expected_root == '':
            if word[0].lemma:
                self.assertIsNone(word[0].lemma.root)
        else:
            self.assertEquals(word[0].lemma.root.text, get_unicode(expected_root))

    @staticmethod
    def get_segment(sura_number, aya_number, word_number, segment_ttext):
        return Segment.objects.filter(
            words__sura__number=sura_number,
            words__aya__number=aya_number,
            words__number=word_number,
            ttext=segment_ttext)

    def check_pos(self, sura_number, aya_number, word_number, segment_ttext, expected_pos):
        segment = self.get_segment(sura_number, aya_number, word_number, segment_ttext)
        self.assertEquals(segment.__len__(), 1)
        if expected_pos == '':
            self.assertIsNone(segment[0].pos)
        else:
            self.assertEquals(segment[0].pos.text, expected_pos)

    def check_gender(self, sura_number, aya_number, word_number, segment_ttext, expected_gender):
        segment = self.get_segment(sura_number, aya_number, word_number, segment_ttext)
        self.assertEquals(segment.__len__(), 1)
        if expected_gender == '':
            self.assertIsNone(segment[0].gender)
        else:
            self.assertEquals(segment[0].gender.text, expected_gender)

    def check_case(self, sura_number, aya_number, word_number, segment_ttext, expected_case):
        segment = self.get_segment(sura_number, aya_number, word_number, segment_ttext)
        self.assertEquals(segment.__len__(), 1)
        if expected_case == '':
            self.assertIsNone(segment[0].case)
        else:
            self.assertEquals(segment[0].case.text, expected_case)

    def test_words(self):
        # Test the first ayas of some suras
        self.check_word(1, 1, 3, '{lr~aHoma`ni')
        self.check_word(2, 1, 1, 'Al^m^')
        self.check_word(114, 1, 1, 'qulo')

        # Test the last ayas of some suras
        self.check_word(1, 7, 2, '{l~a*iyna')
        self.check_word(2, 286, 49, '{loka`firiyna')
        self.check_word(114, 6, 3, 'wa{ln~aAsi')

    def test_lemmas(self):
        # Test the first ayas of some suras
        self.check_lemma(1, 1, 3, 'r~aHoma`n')
        self.check_lemma(2, 1, 1, '')
        self.check_lemma(114, 1, 1, 'qaAla')

        # Test the last ayas of some suras
        self.check_lemma(1, 7, 2, '{l~a*iY')
        self.check_lemma(2, 286, 49, 'ka`firuwn')
        self.check_lemma(114, 6, 3, 'n~aAs')

    def test_roots(self):
        # Test the first ayas of some suras
        self.check_root(1, 1, 3, 'rHm')
        self.check_root(2, 1, 1, '')
        self.check_root(114, 1, 1, 'qwl')

        # Test the last ayas of some suras
        self.check_root(1, 7, 2, '')
        self.check_root(2, 286, 49, 'kfr')
        self.check_root(114, 6, 3, 'nws')

    def test_pos(self):
        # Test the first ayas of some suras
        self.check_pos(1, 1, 3, '{l', 'DET')
        self.check_pos(1, 1, 3, 'r~aHoma`ni', 'ADJ')
        self.check_pos(2, 1, 1, 'Al^m^', 'INL')
        self.check_pos(114, 1, 1, 'qulo', 'V')

        # Test the last ayas of some suras
        self.check_pos(1, 7, 2, '{l~a*iyna', 'REL')
        self.check_pos(2, 286, 49, '{lo', 'DET')
        self.check_pos(2, 286, 49, 'ka`firiyna', 'ADJ')
        self.check_pos(114, 6, 3, 'wa', 'CONJ')
        self.check_pos(114, 6, 3, '{l', 'DET')
        self.check_pos(114, 6, 3, 'n~aAsi', 'N')

    def test_gender(self):
        # Test the first ayas of some suras
        self.check_gender(1, 1, 3, '{l', '')
        self.check_gender(1, 1, 3, 'r~aHoma`ni', 'MS')
        self.check_gender(2, 1, 1, 'Al^m^', '')
        self.check_gender(114, 1, 1, 'qulo', '2MS')

        # Test the last ayas of some suras
        self.check_gender(1, 7, 2, '{l~a*iyna', 'MP')
        self.check_gender(2, 286, 49, '{lo', '')
        self.check_gender(2, 286, 49, 'ka`firiyna', 'MP')
        self.check_gender(114, 6, 3, 'wa', '')
        self.check_gender(114, 6, 3, '{l', '')
        self.check_gender(114, 6, 3, 'n~aAsi', 'MP')

    def test_case(self):
        # Test the first ayas of some suras
        self.check_case(1, 1, 3, '{l', '')
        self.check_case(1, 1, 3, 'r~aHoma`ni', 'GEN')
        self.check_case(2, 1, 1, 'Al^m^', '')
        self.check_case(114, 1, 1, 'qulo', '')

        # Test the last ayas of some suras
        self.check_case(1, 7, 2, '{l~a*iyna', '')
        self.check_case(2, 286, 49, '{lo', '')
        self.check_case(2, 286, 49, 'ka`firiyna', 'GEN')
        self.check_case(114, 6, 3, 'wa', '')
        self.check_case(114, 6, 3, '{l', '')
        self.check_case(114, 6, 3, 'n~aAsi', 'GEN')

    def test_yusuf_ali(self):
        """
        Test some ayas against Yusuf Ali
        """
        sura_number = 112
        aya_number = 4
        aya_translation = AyaTranslation.objects\
            .filter(translation__ttext='Yusuf Ali')\
            .filter(sura__number=sura_number)\
            .filter(aya__number=aya_number)
        self.assertEquals(aya_translation.__len__(), 1)
        self.assertEquals(aya_translation[0].text, 'And there is none like unto Him.')


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):
        test_data(2)