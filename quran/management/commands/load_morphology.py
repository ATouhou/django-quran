import unittest

from django.core.management.base import BaseCommand
from quran.load import *

from quran.management.commands.delete_morphology import delete_morphology
from quran.tests import TestMorphology


class Command(BaseCommand):
    help = "Load initial Quran data."

    def add_arguments(self, parser):
        # Named (optional) argument -t for testing: just do sura fatiha for faster testing
        parser.add_argument('-t', action='store_true')

    def handle(self, *args, **options):
        delete_morphology()
        import_morphology(options['t'])

        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMorphology)
        unittest.TextTestRunner(verbosity=2).run(test_suite)
