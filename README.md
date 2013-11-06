Ultros-contrib
==============

This repo contains packages for Ultros that have been contributed by people other than the core development team.
Packages may contain plugins, protocols, utils, and otherwise pretty much any files the developer requires.
If you'd like to add to this repository, please take note of the following guidelines..

* Packages must have a file structure that matches Ultros' file structure - making installation a simple copy and paste of a set of files.
* Every package must contain a README.md file, written using GitHub-flavored Markdown.
* Every package must include a LICENSE file. The license doesn't have to match the Ultros core license.
  * Be sure to reference the file or license in your plugin's .plug files, if you have any.
  * Licenses must be open-source licenses; a good place to find these licenses is [the Open Source Initiative](http://opensource.org/licenses)
* If your plugin needs configuration, include an example configuration file.
* Do not commit libraries if you didn't develop them. List them in the README instead.
* Test your code. Make sure it works. You don't have to supply a test suite, but we will be manually testing all submitted code.
* Obviously, don't submit anything malicious. Don't bother trying to wreck our computers with malicious code either; we do our testing in VMs.

Other than that, your package has no restrictions. It can contain plugins, protocols, a mixture of both, or even a set of dev tools for your other packages.

The best way to submit a package is to fork this repo, modify your copy of it, and then submit a pull request with your changes.
A member of the core dev team will look over your code and test it, and will either approve or deny it within a couple days.

