[TBlock Logo]

[Pipeline status] [Translation status]

TBlock

TBlock is a free and open-source system-wide ad-blocker that is
compatible with most filter list formats.

Features

-   Free and open-source software
-   Does not cost any money
-   Does not track your personal data
-   Does not make you fingerprintable, unlike some ad-blocking browser
    extensions
-   Blocks ads for your whole operating system
-   Compatible with most filter list formats
-   Has an online filter repository to help you find and subscribe to
    filter lists in an easier way
-   Has a built-in filter converter
-   Has a built-in daemon that regularly updates the filter lists and
    prevents your hosts file from being edited by another program

Installation

TBlock provides various installation methods. These installation methods
can be found on the website and in the documentation.

Though the developers encourage you to install the package that is
compatible with your operating system, you can still TBlock install
safely and easily with pipx (that will only install it for the current
user):

    pipx install tblock

Building TBlock manually can also be an option, although you’ll have to
check manually for new updates. To learn more about how to build the
software manually, see BUILDING.md or consult the documentation.

After installation

If you don’t do anything after installing TBlock, it won’t be able to
block ads. You need to initialize it and to sync the online sources of
your choice, in order to have an efficient blocking. The developers
consider subscribing to the tblock-base list a good start. Right after
the installation, you need to run (with administration privileges):

    tblock -Sy tblock-base

Issues

If you encounter an issue while you are using TBlock, or if you want to
suggest a new feature, you have multiple options (because we don’t want
to force our users to join Codeberg to contribute to the project):

-   Open an issue on Codeberg
-   Contact us via Email
-   Contact us on Matrix
-   Contact us on XMPP
-   Contact us on Mastodon

If however you found a vulnerability in TBlock’s code, it is important
that you don’t share it publicly, because other people could exploit it.
In that case, see SECURITY.md.

Libraries used

TBlock uses the external libraries:

  ----------------------------------------------------------------------------------------------------
  Name              Author            License           Homepage
  ----------------- ----------------- ----------------- ----------------------------------------------
  colorama          Jonathan Hartley  BSD               https://github.com/tartley/colorama

  requests          Kenneth Reitz     Apache 2.0        https://requests.readthedocs.io/

  urllib3           Andrey Petrov     MIT               https://urllib3.readthedocs.io/

  defusedxml        Christian Hiemes  PSFL              https://github.com/tiran/defusedxml

  argumentor        Twann             LGPLv3            https://codeberg.org/twann/python-argumentor
  ----------------------------------------------------------------------------------------------------

License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see https://www.gnu.org/licenses/.
