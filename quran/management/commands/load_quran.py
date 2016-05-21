from django.core.management.base import BaseCommand
from quran.load import *

class Command(BaseCommand):
    help = "Load initial Quran data."

    def handle(self, **options):
        if Aya.objects.count() > 0:
            print ('The quran database must be empty before running quran_loaddata. Running tests.')
            test_data(verbosity=options['verbosity'])
            return

        print ("----- importing quran data (Tanzil) -----")
        import_quran()

        print ("----- done importing quran data (Tanzil). starting translations -----")
        import_translations()
