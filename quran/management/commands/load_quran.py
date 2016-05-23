from django.core.management.base import BaseCommand
from quran.load import *

from quran.management.commands.delete_quran import delete_quran
from quran.management.commands.load_morphology import delete_morphology


class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):

        delete_morphology()
        delete_quran()

        import_quran()

        import_translations()
