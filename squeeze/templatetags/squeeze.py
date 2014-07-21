from __future__ import absolute_import

from squeeze.package import Package

def render_package(packagename):
        return Package(packagename).render()

