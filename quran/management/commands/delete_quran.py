from django.core.management.base import BaseCommand
from quran.load import *
from django.db import connection

from quran.management.commands.load_morphology import delete_morphology

def delete_quran():
    print("------ deleting suras, translations, ayas, ayatranslations")
    cursor = connection.cursor()
    cursor.execute('delete from postgres.quran.quran_ayatranslation')
    cursor.execute('delete from postgres.quran.quran_translation')
    cursor.execute('delete from postgres.quran.quran_page')
    cursor.execute('delete from postgres.quran.quran_aya')
    cursor.execute('delete from postgres.quran.quran_sura')
    cursor.execute("alter sequence quran.quran_page_id_seq minvalue 1 start with 1 restart")
    cursor.execute("alter sequence quran.quran_aya_id_seq minvalue 1 start with 1 restart")
    cursor.execute("alter sequence quran.quran_translation_id_seq minvalue 1 start with 1 restart")


class Command(BaseCommand):
    help = "Delete Quran data."

    def handle(self, **options):

        delete_morphology()
        delete_quran()
