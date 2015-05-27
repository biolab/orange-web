from PIL import Image
import glob, os

from django.core.management.base import BaseCommand

from homepage.views import discover_screenshots

class Command(BaseCommand):
    help = 'Generates thumbnails for screenshots'

    def handle(self, *args, **options):
        size = (180, 180)
        folder = os.path.dirname(os.path.realpath(__file__))
        static = os.path.join(folder, "../../static")
        pngs = os.path.join(static, "homepage/screenshots/*.png")

        screenshots = discover_screenshots()
        screen_ids = [screen['id'] for screen in screenshots]
        index = []

        for f in glob.glob(pngs):
            snp_dir = os.path.dirname(f)
            tbn_dir = os.path.join(snp_dir, "./thumbs")
            fname = os.path.basename(f)
            id, ext = os.path.splitext(fname)

            if id not in screen_ids:
                index.append('<screenshot id="%s" title="TODO" rank="999"></screenshot>' % id)

            im = Image.open(f)
            im = im.convert("RGBA")
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(os.path.join(tbn_dir, fname))

        for screenshot in screenshots:
            if not os.path.isfile(os.path.join(static, screenshot['img'])):
                print("Missing screenshot image %s" % screenshot['img'])

        if len(index)>0:
            print("Consider adding the following screenshots to the index:")
            print('\n'.join(index))
