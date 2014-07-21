import mimetypes

from django import http

from squeeze.package import Package, UnknownPackage

def staticpackage(request, packagename, ext):
	try:
		package = Package(packagename)
	except UnknownPackage:
		raise http.Http404, 'Unknown package: %s'  % packagename

	ext = ext.lower()

	nocache = request.META.get('HTTP_CACHE_CONTROL', '') == 'no-cache'

	if package.needs_update(ext) or nocache:
		content = package.write(ext)
	else:
		content = package.from_cache(ext)

	path = package.path_with_ext(ext)

	content_type = mimetypes.guess_type(path)[0]

	response = http.HttpResponse(content, content_type=content_type)
	response['Content-Length'] = len(content)

	return response