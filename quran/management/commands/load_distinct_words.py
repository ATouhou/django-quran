import unittest

from quran.load import *
from quran.management.commands.delete_distinct_words import delete_distinct_words
from quran.management.commands.delete_word_meanings import *


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):
        delete_distinct_words()
        generate_distinct_words()