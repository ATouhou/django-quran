from django.core.management.base import BaseCommand
from django.db import connection

from quran.management.commands.delete_word_meanings import delete_word_meanings


def delete_morphology():
    cursor = connection.cursor()
    print("----- deleting words, segments, lemmas, roots, pos', moods, genders, forms, specials, cases, definites, tenses, participles")
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
    cursor.execute("alter sequence quran_word_id_seq minvalue 1 start with 1 restart")
    cursor.execute("alter sequence quran_wordsegment_id_seq minvalue 1 start with 1 restart")
    cursor.execute("alter sequence quran_segment_id_seq minvalue 1 start with 1 restart")
    cursor.execute("alter sequence quran_lemma_id_seq minvalue 1 start with 1 restart")
    cursor.execute("alter sequence quran_root_id_seq minvalue 1 start with 1 restart")


class Command(BaseCommand):
    help = "Delete morphology data."

    def handle(self, *args, **options):
        delete_word_meanings()
        delete_morphology()
