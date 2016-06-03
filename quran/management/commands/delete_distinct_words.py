from django.core.management.base import BaseCommand
from django.db import connection


def delete_distinct_words():
    cursor = connection.cursor()
    print("----- deleting distinct words ----------- ")
    cursor.execute('update postgres.quran.quran_word set distinct_word_id=null')
    cursor.execute('delete from postgres.quran.quran_distinctword')
    cursor.execute("alter sequence quran.quran_distinctword_id_seq minvalue 1 start with 1 restart")


class Command(BaseCommand):
    help = "Delete distinct words."

    def handle(self, *args, **options):
        delete_distinct_words()
