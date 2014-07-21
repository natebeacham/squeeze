import os
import hashlib

from django.conf import settings
from django.core.cache import cache

from squeeze.compilers import COMPILERS

_out_dir = settings.SQUEEZE.get('out_dir', 's')
_compile = settings.SQUEEZE.get('compile', True)
_debug = settings.SQUEEZE.get('debug', False)

VERSION = 1 # Cache version

def path(name):
	return os.path.join(settings.MEDIA_ROOT, _out_dir, name)

def uri(name, ext):
	return '%s%s/%s.%s' % (settings.MEDIA_URL, _out_dir, name, ext)

if not os.path.exists(os.path.join(settings.MEDIA_ROOT, _out_dir)):
	os.mkdir(os.path.join(settings.MEDIA_ROOT, _out_dir))

class UnknownPackage(Exception):
	pass

class Package(object):
	def __init__(self, name):
		self.__name = name

		try:
			self.buffers = settings.SQUEEZE['packages'][name]
		except KeyError, e:
			raise UnknownPackage, e

	@property
	def packagename(self):
		#return hashlib.md5(self.__name).hexdigest()
		return self.__name

	def path_with_ext(self, ext):
		return '%s.%s' % (path(self.__name), ext)

	def needs_update(self, ext):
		if _debug:
			return True

		if not os.path.exists('%s.%s' % (path(self.__name), ext)):
			return True

		compiletime = os.stat('%s.%s' % (path(self.__name), ext)).st_mtime

		for buffer, compiler in self.get_compilers():
			if not ext == compiler.type:
				continue

			modtime = os.stat(os.path.join(settings.MEDIA_ROOT, buffer)).st_mtime

			if modtime > compiletime:
				return True

		return False

	def get_cache_key(self, ext):
		return 'squeezed__%s__%s:%s' % (self.__name, ext, VERSION)

	def from_cache(self, ext, nocache=False):
		cache_key = self.get_cache_key(ext)

		cached = cache.get(cache_key)

		if not _debug and cached is not None and not nocache:
			return cached

		buf = open('%s.%s' % (path(self.__name), ext), 'r').read()

		cache.set(cache_key, buf)

		return buf

	def write(self, ext, compress=_compile):
		cache_key = self.get_cache_key(ext)

		rendered = []

		for buffer, compiler in self.get_compilers():
			if not compiler.type == ext:
				continue

			fullpath = os.path.join(settings.MEDIA_ROOT, buffer)
			compiled = compiler.compile(fullpath)

			if compress:
				rendered.append(compiler.compress(compiled))
			else:
				rendered.append(compiled)

		joiner = ';\n' if ext == 'js' else '\n'

		content = joiner.join(rendered)

		out = open('%s.%s' % (path(self.__name), ext), 'w')
		out.write(content)
		out.close()

		cache.set(cache_key, content)

		return content

	def get_compilers(self):
		for buffer in self.buffers:
			ext = buffer.split('.')[-1].lower()
			if ext in COMPILERS:
				yield buffer, COMPILERS[ext]

	@property
	def types(self):
		for buffer, compiler in self.get_compilers():
			yield compiler.type

	def render(self):
		types = list(self.types)
		result = ''

		if 'js' in types:
			result += '<script language="javascript" type="text/javascript" src="%s"></script>\n' % uri(self.packagename, 'js')

		if 'css' in types:
			result += '<link type="text/css" rel="stylesheet" href="%s">\n' % uri(self.packagename, 'css')

		return result
