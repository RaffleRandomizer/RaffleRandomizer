from django.core.management import BaseCommand
from backend.utils import fill_db

class Command(BaseCommand):
    help = "run notifications"

    def handle(self, *args, **options):
        fill_db()
        print("done")