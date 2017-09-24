codeorigins
===========
https://github.com/idlesign/codeorigins

|release| |stats|  |lic|

.. |release| image:: https://img.shields.io/pypi/v/codeorigins.svg
    :target: https://pypi.python.org/pypi/codeorigins

.. |stats| image:: https://img.shields.io/pypi/dm/codeorigins.svg
    :target: https://pypi.python.org/pypi/codeorigins

.. |lic| image:: https://img.shields.io/pypi/l/codeorigins.svg
    :target: https://pypi.python.org/pypi/codeorigins


**Work in progress. Stay tuned.**


Description
-----------

*Code origins contest based on GitHub data*

* Find interesting people and projects originating in various countries;
* See what countries produce most starred projects;
* Know your impact on community of your favourite language;
* and more.


Requirements
------------

* Python 3


CLI
---

**Dumper**

Using rate-limited GitHub search API:


.. code-block:: bash

    > codeorigins dump --into /home/idle/ghdump --country ru --language Python api

This will use `api` to fetch repositories data for users located in `Russia` whose primary language is `Python`
and dump it into `/home/idle/ghdump`.

Register OAuth Application (https://github.com/settings/applications/) and use its *Client ID* and
*Client Secret* to loosen the rate limits (append `--credentials <id>,<secret>` to dump command).


**Settings**

See supported countries and languages using the following command:

.. code-block:: bash

    > codeorigins show_settings

