from django.core.management import BaseCommand
from backend.utils import get_text_list

class Command(BaseCommand):
    help = "run notifications"

    def handle(self, *args, **options):
        get_text_list()
        print("done")