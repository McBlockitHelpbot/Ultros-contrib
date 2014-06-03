"""
w3validate.py:

Supply an URL and it returns the amount if the document passed the validation
test.

Makes use of the w3.org API

Licensed under MIT by Zarthus <zarthus@zarth.us>, 3 June, 2014.
"""

import requests

import system.plugin as plugin
from system.command_manager import CommandManager
from system.decorators import run_async_threadpool

from twisted.internet import reactor


class W3validatorPlugin(plugin.PluginObject):
    commands = None

    def setup(self):
        self.commands = CommandManager()

        self.commands.register_command("w3validate", self.w3validate,
                                       self, "w3.w3validate",
                                       aliases=["validate", "valid"])

    def w3validate(self, protocol, caller, source, command, raw_args,
                   parsed_args):
        """Syntax: w3validate [website to validate]"""

        if parsed_args is None:
            parsed_args = raw_args.split()

        if len(parsed_args) < 1:
            return caller.respond("{CHARS}w3validate [url] [...] - Validate a "
                                  "website using validator.w3.org")

        if len(parsed_args) > 3:
            caller.respond("You cannot request more than three websites "
                           "to be validated at a time, to prevent "
                           "flooding the validator.")

        # If we're sending too many requests, exit the loop.
        # Also used to calculate how long we should wait.
        itter = 0

        for website in parsed_args:
            reactor.callLater(itter, source.respond,
                              self.w3_validate_url(website))

            itter += 1
            if itter > 3:
                break

    @run_async_threadpool
    def w3_validate_url(self, website):
        """Retrieve and return the validity of a website"""
        val_link = "http://validator.w3.org/check?uri=" + website

        r = requests.get(val_link)
        valid = r.headers["x-w3c-validator-status"].lower()
        col_valid = self.w3_colour_validity(valid)

        if valid == "valid":
            return "[{}] The website {} is {}. ({})".format(col_valid, website,
                                                       col_valid, val_link)
        if valid == "abort":
            # Possibility that the URL is invalid
            return ("[{}] The validation for \"{}\" aborted unexpectedly."
                    " Is this a valid URL?".format(col_valid, website))

        errors = r.headers["x-w3c-validator-errors"]
        warnings = r.headers["x-w3c-validator-warnings"]
        recursion = r.headers["x-w3c-validator-recursion"]

        errstring = ""
        if errors:
            errstring += "Errors: {}, ".format(errors)
        if warnings:
            errstring += "Warnings: {}, ".format(warnings)
        if recursion:
            errstring += "Recursion: {}, ".format(recursion)
        if errstring:
            # Remove the ", " from the string.
            errstring = errstring[:-2]
            return ("[{}] The website {} is \x0304{}\x0F. {} ({})").format(
                     col_valid, website, col_valid, errstring, val_link
            )

        return "[{}] The website {} is {}. ({})".format(col_valid, website,
                                                        col_valid, val_link)

    def w3_colour_validity(validity):
        """
        Colourise the validity,
        green is valid, red is invalid, the rest is gray
        """
        col_valid = ""

        valid = validity.lower()
        if valid == "valid":
            col_valid = "\x0303Valid\x0F"
        elif valid == "invalid":
            col_valid = "\x0304Invalid\x0F"
        else:
            col_valid = "\x0314{}\x0F".format(validity)

        return col_valid