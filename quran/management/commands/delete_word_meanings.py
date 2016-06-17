from django.core.management.base import BaseCommand
from django.db import connection


def delete_word_meanings():
    cursor = connection.cursor()
    print("----- deleting words' meanings ----------- ")
    cursor.execute('update quran_word set meaning_id=null')
    cursor.execute('delete from quran_wordmeaning')
    cursor.execute("alter sequence quran_wordmeaning_id_seq minvalue 1 start with 1 restart")


class Command(BaseCommand):
    help = "Delete word meanings."

    def handle(self, *args, **options):
        delete_word_meanings()
