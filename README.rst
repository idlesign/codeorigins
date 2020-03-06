codeorigins
===========
https://github.com/idlesign/codeorigins

|python| |release|

.. |python| image:: http://forthebadge.com/images/badges/made-with-python.svg
    :target: https://www.python.org

.. |release| image:: https://img.shields.io/pypi/v/codeorigins.svg
    :target: https://pypi.python.org/pypi/codeorigins


Description
-----------

*Code origins contest based on GitHub data*

CodeOrigins live: http://idlesign.github.io/codeorigins/

* Find interesting people and projects originating in various countries;
* See what countries produce most starred projects;
* Know your impact on community of your favourite language;
* and more.


FAQ
---

* *But wait, this data is not realtime!*

  Yes, these are static web-pages (see ``docs/``) compiled from dumped data (see ``codeorigins/dump/``).
  And it sure can be outdated.

* *And what if I want to see updated data?*

  You can dump data you're interested in and make a pull request.

  Quick and dirty start:

  1. Fork repository;
  2. Git pull forked repository into local directory;
  3. ``$ cd`` to the directory;
  4. ``$ pip install -e .`` (``sudo`` may be required) -
     this will made ``codeorigins`` CLI available;
  5. Use ``$ codeorigins dump`` (see below) without ``--into`` -
     this puts dumps into ``codeorigins/dump/``;
  6. Commit and push added/changed dumps;
  7. Create a pull request on your GitHub repository page.

* *My country or language is not listed, what am I to do?*

  Edit ``codeorigins/settings.py``, add all what you need and make a pull request.
  You can also make and submit new/updated dumps (see above).


CLI
---

**codeorigins** comes with CLI to streamline common actions.

Data Dump
~~~~~~~~~


Using rate-limited GitHub search API:


.. code-block:: bash

    $ codeorigins dump --into /home/idle/ghdump --country ru --language Python api

This will use ``api`` to fetch repositories data for users located in ``Russia`` whose primary language is ``Python``
and dump it into ``/home/idle/ghdump``.

Register OAuth Application (https://github.com/settings/developers) and use its *Client ID* and
*Client Secret* to loosen the rate limits (append ``--credentials <id>,<secret>`` to dump command).


HTML Export
~~~~~~~~~~~

Use ``make_html`` command to read data from dumps and compose HTML:

.. code-block:: bash

    $ codeorigins make_html --dump_dir /home/idle/ghdump

This will create HTML file in current working directory.


Settings
~~~~~~~~

See supported countries and languages using the following command:

.. code-block:: bash

    $ codeorigins show_settings


Requirements
------------

* Python 3.6+
* click
* Jinja2
* requests
