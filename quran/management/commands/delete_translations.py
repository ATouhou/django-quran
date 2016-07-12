from django.core.management.base import BaseCommand
from django.db import connection


def delete_translations():
    print("----- deleting translations, ayatranslations")
    cursor = connection.cursor()
    cursor.execute('delete from quran_ayatranslation')
    cursor.execute('delete from quran_translation')
    cursor.execute("alter sequence quran_translation_id_seq minvalue 1 start with 1 restart")


class Command(BaseCommand):
    help = "Delete Translations."

    def handle(self, **options):
        delete_translations()
