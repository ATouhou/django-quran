from django.core.management.base import BaseCommand
from quran.load import *
from django.db import connection

class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):

        print("------ deleting words, segments, lemmas, roots, pos', moods, genders, forms, specials, cases, definites, tenses, participles, etc.")
        cursor = connection.cursor()
        cursor.execute('delete from quran_wordsegment')
        cursor.execute('delete from quran_segment')
        cursor.execute('delete from quran_word')
        cursor.execute('delete from quran_lemma')
        cursor.execute('delete from quran_root')
        cursor.execute('delete from quran_pos')
        cursor.execute('delete from quran_mood')
        cursor.execute('delete from quran_gender')
        cursor.execute('delete from quran_form')
        cursor.execute('delete from quran_special')
        cursor.execute('delete from quran_case')
        cursor.execute('delete from quran_definite')
        cursor.execute('delete from quran_tense')
        cursor.execute('delete from quran_participle')
        cursor.execute('delete from quran_other')
        cursor.execute("select setval('quran.quran_word_id_seq', 1)")

        import_morphology()
        print ("----- done importing morphology -----")

        # test_data(verbosity=options['verbosity'])

