import unittest

from quran.load import *
from quran.management.commands.delete_word_meanings import *
from quran.tests import TestWordMeanings


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):
        delete_word_meanings()
        import_word_meanings()

        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestWordMeanings)
        unittest.TextTestRunner(verbosity=2).run(test_suite)
