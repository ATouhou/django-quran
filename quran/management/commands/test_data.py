from django.core.management import BaseCommand
from quran.tests import *


def test_data(verbosity):
    verbosity = int(verbosity)
    print(verbosity)

    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestQuran)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)

    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMorphology)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)

    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestWordMeanings)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):
        test_data(2)