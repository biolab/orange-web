import os
import json
import fnmatch
import time
from error_report.sentry import send_to_sentry

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<FOLDER>'
    help = 'Reads error reports from a given folder and sends them to Sentry'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("Required argument <FOLDER> missing.\n"
                               "Run --help for more info.")
        folder = args[0]
        if not os.path.exists(folder):
            raise CommandError("Path '{}' does not exists!".format(folder))

        for root, dirnames, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, '*.txt'):
                path = os.path.join(root, filename)
                print('Sending errors from file {} ...'.format(path))
                report = ' '.join(open(path, 'r').readlines())
                report = json.loads(report)

                # check for schema
                schema = path.replace('.txt', '.ows')
                if os.path.exists(schema):
                    rel_path = schema.partition(folder+'/')[2]
                    report['Widget Scheme'] = rel_path

                send_to_sentry(report)
                time.sleep(1)   # to prevent being rate limited
