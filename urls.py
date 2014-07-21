from django.conf import settings

from django.conf.urls import patterns, include, url

out_dir = settings.SQUEEZE.get('out_dir', 's')

urlpatterns = patterns('',
    url(r'^%s/(?P<packagename>[a-zA-Z0-9\-_]+)\.(?P<ext>[a-zA-Z]+)' % out_dir,
        'squeeze.views.staticpackage', name='squeezer'),
)
