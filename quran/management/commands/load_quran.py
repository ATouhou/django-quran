from django.core.management.base import BaseCommand
from quran.load import *
from django.db import connection


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):

        cursor = connection.cursor()

        print("------ deleting words, segments, lemmas, roots, pos', moods, genders, forms, specials, cases, definites, tenses, participles, etc.")
        cursor.execute('delete from postgres.quran.quran_wordsegment')
        cursor.execute('delete from postgres.quran.quran_segment')
        cursor.execute('delete from postgres.quran.quran_word')
        cursor.execute('delete from postgres.quran.quran_lemma')
        cursor.execute('delete from postgres.quran.quran_root')
        cursor.execute('delete from postgres.quran.quran_pos')
        cursor.execute('delete from postgres.quran.quran_mood')
        cursor.execute('delete from postgres.quran.quran_gender')
        cursor.execute('delete from postgres.quran.quran_form')
        cursor.execute('delete from postgres.quran.quran_special')
        cursor.execute('delete from postgres.quran.quran_case')
        cursor.execute('delete from postgres.quran.quran_definite')
        cursor.execute('delete from postgres.quran.quran_tense')
        cursor.execute('delete from postgres.quran.quran_participle')
        cursor.execute('delete from postgres.quran.quran_other')
        cursor.execute("select setval('quran.quran_word_id_seq', 1)")

        print("------ deleting suras, translations, ayas, ayatranslations")
        cursor.execute('delete from postgres.quran.quran_ayatranslation')
        cursor.execute('delete from postgres.quran.quran_translation')
        cursor.execute('delete from postgres.quran.quran_aya')
        cursor.execute('delete from postgres.quran.quran_sura')
        cursor.execute("select setval('quran.quran_aya_id_seq', 1)")

        print ("----- importing quran data (Tanzil) -----")
        import_quran()

        print ("----- done importing quran data (Tanzil). starting translations -----")
        import_translations()
