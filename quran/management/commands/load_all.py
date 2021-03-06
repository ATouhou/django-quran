from django.core.management.base import BaseCommand

from quran.management.commands.delete_quran import delete_quran
from quran.management.commands.delete_word_meanings import delete_word_meanings
from quran.management.commands.load_morphology import delete_morphology
from quran.management.commands.delete_distinct_words import delete_distinct_words
from quran.management.commands.test_data import test_data

from quran.load import *



class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):

        # order below is important due to dependencies
        delete_distinct_words()
        delete_word_meanings()
        delete_morphology()
        delete_quran()

        import_quran()
        import_morphology()
        import_word_meanings()
        generate_distinct_words()

        test_data(verbosity=2)
