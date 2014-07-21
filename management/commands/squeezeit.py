import sys
import time

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from squeeze.package import Package

PACKAGES = settings.SQUEEZE['packages']
OUT_DIR = settings.SQUEEZE.get('out_dir', 'squeezed')

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--ignoremod',
			action='store_true',
			dest='ignore_mod',
			default=False,
		),
	)

	def handle(self, *args, **opts):
		sys.stdout.write('\n\t=== Squeeze! ===\n\n')

		something_happened = False

		for packagename in PACKAGES:
			package = Package(packagename)

			for ext in set(package.types):
				if opts['ignore_mod'] or package.needs_update(ext):
					sys.stdout.write('\t* Writing %s.%s...\n' % (packagename, ext))

					start = time.time()
					package.write(ext, compress=True)
					end = time.time()

					sys.stdout.write('\t\t= %.2f seconds\n' % (end - start))

					something_happened = True

		if not something_happened:
			sys.stdout.write('\tNothing to do!\n')

