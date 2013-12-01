# coding=utf-8
from system.plugin_manager import YamlPluginManagerSingleton

__author__ = 'Gareth Coles'

import logging
import urllib
import urllib2

from system.plugin import PluginObject
from utils.config import Config
from utils.misc import output_exception


class URLToolsPlugin(PluginObject):

    config = None
    api_details = {}

    sites = {}
    shorteners = {}

    plugman = None

    def setup(self):
        try:
            self.config = Config("plugins/money.yml")
        except Exception:
            self.logger.error("Unable to load the configuration!")
            output_exception(self.logger, logging.ERROR)
            self._disable_self()
            return

        self.sites["osu.ppy.sh"] = self.site_osu
        self.sites["youtube.com"] = self.site_youtube

        self.shorteners["bit.ly"] = self.shortener_bitly
        self.shorteners["is.gd"] = self.shortener_isgd
        self.shorteners["j.mp"] = self.shortener_jmp
        self.shorteners["nazr.in"] = self.shortener_nazrin
        self.shorteners["v.gd"] = self.shortener_vgd
        self.shorteners["waa.ai"] = self.shortener_waaai

        self.plugman = YamlPluginManagerSingleton.instance()

        shorteners = self.config["shorteners"]
        sites = self.config["sites"]

        sites_enabled = []
        shorteners_enabled = []

        for site in sites["enabled"]:
            if site.lower() == "osu.ppy.sh":
                if not sites["apikeys"]["osu"]:
                    self.logger.warn("Osu! support enabled, but no API key was"
                                     " configured. You'll need to add one if "
                                     "you want Osu! support.")
                    continue
            sites_enabled.append(sites)
        self.logger.info("Enabled support for %s sites."
                         % len(sites_enabled))

        for shortener in shorteners["enabled"]:
            if shortener.lower() == "bit.ly":
                if not shorteners["bitly"]["apikey"]:
                    self.logger.info("Enabling bit.ly support without an API "
                                     "key.")
                elif not shorteners["bitly"]["login"]:
                    self.logger.info("Enabling bit.ly support without an API "
                                     "login.")
                else:
                    self.logger.info("Bit.ly API key and login found!")
                    self.api_details["bit.ly"] = shorteners["bitly"]
            elif shortener.lower() == "j.mp":
                if not shorteners["apikeys"]["bitly"]:
                    self.logger.info("Enabling j.mp support without an API "
                                     "key.")
                else:
                    self.logger.info("J.mp API key found!")
            shorteners_enabled.append(shortener)

        self.logger.debug("Setting up shorteners with the URLs plugin..")

        urls = self.plugman.getPluginByName("URLs")

        for site in sites_enabled:
            urls.add_handler(site, self.sites[site])

        for shortener in shorteners_enabled:
            urls.add_shortener(shortener, self.shorteners[shortener])

        self.logger.info("Enabled support for %s shorteners."
                         % len(shorteners_enabled))

    def do_get(self, url, params):
        query_string = urllib.urlencode(params)
        constructed = url + "?" + query_string
        self.logger.debug("Constructed GET: %s" % constructed)
        r = urllib2.urlopen(constructed)
        data = r.read()
        self.logger.debug("Response: %s" % data)
        return data

    def do_post(self, url, params, header=None):
        if not header:
            header = {}
        request = urllib2.Request(url, params, header)
        self.logger.debug("Constructed POST: %s | %s" % (url, params))
        r = urllib2.urlopen(request)
        data = r.read()
        self.logger.debug("Response: %s" % data)
        return data

    def shortener_bitly(self, url):
        # Params: login, apiKey, longUrl, domain=bit.ly, format=txt
        # URL: /v3/shorten
        # Domain: api[-ssl].bitly.com
        # Response: Text, shortened URL
        params = {"longUrl": url, "format": "txt", "domain": "bit.ly"}

        if "bit.ly" in self.api_details:
            params["login"] = self.api_details["bit.ly"]["login"]
            params["apiKey"] = self.api_details["bit.ly"]["apikey"]

        data = self.do_get("http://api.bitly.com/v3/shorten", params)

        return data

    def shortener_isgd(self, url):
        # Domain: is.gd
        # URL: /create.php
        # Params: url, format=simple
        # Response: Text, shortened URL

        params = {"url": url, "format": "simple"}

        data = self.do_get("http://is.gd/create.php", params)

        return data

    def shortener_jmp(self, url):
        # Params: login, apiKey, longUrl, domain=j.mp, format=txt
        # URL: /v3/shorten
        # Domain: api[-ssl].bitly.com
        # Response: Text, shortened URL
        params = {"longUrl": url, "format": "txt", "domain": "j.mp"}

        if "bit.ly" in self.api_details:
            params["login"] = self.api_details["bit.ly"]["login"]
            params["apiKey"] = self.api_details["bit.ly"]["apikey"]

        data = self.do_get("http://api.bitly.com/v3/shorten", params)

        return data

    def shortener_nazrin(self, url):
        # Domain: nazr.in
        # URL: /api/shorten
        # Params: url
        # Response: Text, shortened URL

        params = {"url": url}

        data = self.do_get("http://nazr.in/api/shorten", params)

        return data

    def shortener_vgd(self, url):
        # Domain: v.gd
        # URL: /create.php
        # Params: url, format=simple
        # Response: Text, shortened URL

        params = {"url": url, "format": "simple"}

        data = self.do_get("http://v.gd/create.php", params)

        return data

    def shortener_waaai(self, url):
        # Domain: api.waa.ai
        # URL: /
        # Params: url
        # Response: Text, shortened URL

        params = {"url": url}

        data = self.do_get("http://api.waa.ai/", params)

        return data

    def site_osu(self, url):
        return url

    def site_youtube(self, url):
        return url

    def _disable_self(self):
        self.factory_manager.plugman.deactivatePluginByName(self.info.name)
