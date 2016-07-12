import unittest

from django.core.management.base import BaseCommand
from quran.load import *

from quran.management.commands.delete_translations import delete_translations
from quran.tests import TestQuran


class Command(BaseCommand):
    help = "Load Translations"

    def handle(self, **options):

        delete_translations()

        import_translations()

        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestQuran)
        unittest.TextTestRunner(verbosity=2).run(test_suite)
