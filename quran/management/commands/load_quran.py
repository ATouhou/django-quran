import unittest

from django.core.management.base import BaseCommand
from quran.load import *

from quran.management.commands.delete_quran import delete_quran
from quran.management.commands.delete_word_meanings import delete_word_meanings
from quran.management.commands.load_morphology import delete_morphology
from quran.tests import TestQuran


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):

        delete_word_meanings()
        delete_morphology()
        delete_quran()

        import_quran()

        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestQuran)
        unittest.TextTestRunner(verbosity=2).run(test_suite)
