# coding=utf-8

__author__ = 'Gareth Coles'

import threading
import tempfile
import os
import shutil

from weakref import ref

from cyclone.template import BaseLoader
from mako.lookup import TemplateLookup


class TemplateLoader(BaseLoader):

    lock = None  # To protect the template cache
    lookup = None  # Mako template lookup class
    _plugin = None  # Weakref of the plugin itself
    root = "web/templates"  # Relative path of templates
    tempdir = None  # Location of cached templates

    @property
    def plugin(self):
        return self._plugin()

    def __init__(self, plugin, namespace=None):
        plugin = ref(plugin)
        self.namespace = namespace or {}
        self.namespace["plugin"] = plugin

        self.lock = threading.RLock()
        self.lookup = TemplateLookup([self.root], self.tempdir)
        self._plugin = plugin
        self.tempdir = tempfile.gettempdir()

    def reset(self):
        with self.lock:
            shutil.rmtree(self.tempdir)
            os.mkdir(self.tempdir)

    def load(self, name, _=None):
        with self.lock:
            return self.lookup.get_template(name)
