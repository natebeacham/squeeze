import os
import tempfile
import subprocess

BIN_PATH = os.path.join(os.path.dirname(__file__), 'bin')

__all__ = ['GoogleClosure', 'YUI']

class GoogleClosure(object):
	binary = '%s/compiler.jar' % BIN_PATH

	@classmethod
	def compress(cls, buffer):
		tmp = tempfile.NamedTemporaryFile(suffix='.css', delete=False)
		tmp.write(buffer)
		tmp.close()

		process = subprocess.Popen(['java', '-jar', cls.binary, '--js', tmp.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		out, err = process.communicate()

		return out

class YUI(object):
	binary = '%s/yuicompressor.jar' % BIN_PATH

	@classmethod
	def compress(cls, buffer):
		tmp = tempfile.NamedTemporaryFile(suffix='.css', delete=False)
		tmp.write(buffer)
		tmp.close()

		process = subprocess.Popen(['java', '-jar', cls.binary, '--type', 'css', tmp.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		out, err = process.communicate()

		return out