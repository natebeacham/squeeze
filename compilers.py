import subprocess

from django.conf import settings

from . import compressors

COMPILERS = dict()

_compress = settings.SQUEEZE.get('compress', not settings.DEBUG)

class CompilerMetaClass(type):
	def __new__(*args):
		cls = type.__new__(*args)
		COMPILERS[cls.ext] = cls
		return cls

class Compiler(object):
	__metaclass__ = CompilerMetaClass

	ext = ''

	@classmethod
	def compile(cls, filename):
		return open(filename).read()

	@classmethod
	def compress(cls, buf):
		return buf

class CSS(Compiler):
	ext = 'css'
	type = 'css'

	@classmethod
	def compress(cls, buf):
		if _compress:
			return compressors.YUI.compress(buf)
		return buf

class SASS(CSS):
	ext = 'sass'

	@classmethod
	def compile(cls, filename):
		if _compress:
			args = ['sass', filename, '--style', 'compressed']
		else:
			args = ['sass', filename]

		process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()

		return out

class SCSS(SASS):
	ext = 'scss'

class JavaScript(Compiler):
	ext = 'js'
	type = 'js'

	@classmethod
	def compress(cls, buf):
		if _compress:
			return compressors.GoogleClosure.compress(buf)
		return buf
