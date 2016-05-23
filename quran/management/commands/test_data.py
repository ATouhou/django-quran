import unittest

from django.core.management import BaseCommand

from quran.models import Sura, Translation
from quran.buckwalter import get_unicode


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
        translation = Translation.objects.get(ttext='Yusuf Ali')
        t = aya.translations.get(translation=translation)
        self.assertEquals(t.text, 'And there is none like unto Him.')


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):
        test_data(2)