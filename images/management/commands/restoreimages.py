import pathlib

from django.core.management.base import BaseCommand

from images.models import Image

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):

        # Go through all images in the DB and make sure they are there, if not, restore from filedata field.
        for i in Image.objects.all():
            f = pathlib.Path(i.file.path)
            if not f.is_file():
                print(f"Restoring file{f}")
                with open(i.file.path, "wb") as fix:
                    fix.write(i.filedata)