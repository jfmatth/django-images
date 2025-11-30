import pathlib

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from images.models import Image

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):

        mr = settings.MEDIA_ROOT
        
        # Go through all images in the DB and make sure they are there, if not, restore from filedata field.
        for i in Image.objects.all():
            f = pathlib.Path(i.file.path)
            if not f.is_file():
                print(f"MISSING FILE - {f}")
