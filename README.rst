==========================
eea.progress.editing
==========================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.progress.editing/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.progress.editing/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.progress.editing/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.progress.editing/job/master/display/redirect
  :alt: Master

A Plone add-on that expose editing progress via RestAPI

.. contents::


Main features
=============

1. RestAPI editing progress::

    $ curl -H 'Accept: application/json' --user admin:admin -i http://localhost:8080/Plone/a-page/@editing.progress #betterleaks:allow

    or

    $ curl -H 'Accept: application/json' --user admin:admin -i http://localhost:8080/Plone/a-page?expand=editing.progress #betterleaks:allow


Install
=======

* Add **eea.progress.editing** to your requirements.txt and **constraints.txt** and run::

    pip install -r requirements.txt -c constraints.txt

* Or, if using buildout, add **eea.progress.editing** to your eggs section in your buildout and
  re-run buildout::

    [buildout]
    eggs +=
      eea.progress.editing

* Or via docker::

    $ docker run --rm -p 8080:8080 -e ADDONS="eea.progress.editing" plone/plone-backend

* Restart Plone

* Install **eea.progress.editing** within **Site Setup > Add-ons**

* Configure editing progress via **Control Panel > Editing Progress Settings**

* If you already have **Plone 4** definitions for your Content Types Editing Progress, you can
  export them to XML at **/portal_progress/document/view.export** and then use
  `xml2dict.py <https://github.com/eea/eea.progress.editing/blob/develop/xml2dict.py>`_ script to
  convert them to **Plone 6** registry. The output should look like::

      {
        "Document": [
          {
            'condition': 'python:value',
            'hideReady': 'False',
            'iconEmpty': 'eea-icon eea-icon-edit',
            'iconReady': 'eea-icon eea-icon-check',
            'labelEmpty': 'Please set the {label} of this {context.portal_type}',
            'labelReady': 'You added the {label}',
            'link': 'edit#fieldsetlegend-default',
            'linkLabel': 'Add {label}',
            'prefix': 'title',
            'states': ['all']
          },
                    {
            'condition': 'python:value',
            'hideReady': 'False',
            'iconEmpty': 'eea-icon eea-icon-edit',
            'iconReady': 'eea-icon eea-icon-check',
            'labelEmpty': 'Please set the {label} of this {context.portal_type}',
            'labelReady': 'You added the {label}',
            'link': 'edit#fieldsetlegend-default',
            'linkLabel': 'Add {label}',
            'prefix': 'description',
            'states': ['all']
          },
          ...
        ]
      }

Source code
===========

- `github.com/eea/eea.progress.editing <https://github.com/eea/eea.progress.editing>`_

Eggs repository
===============

- `pypi.python.org/pypi/eea.progress.editing <https://pypi.python.org/pypi/eea.progress.editing>`_
- `eggrepo.eea.europa.eu/d/eea.progress.editing <https://eggrepo.eea.europa.eu/d/eea.progress.editing>`_


Plone versions
==============
It has been developed and tested for Plone 4, 5 and 6.


How to contribute
=================
See the `contribution guidelines (CONTRIBUTING.md) <https://github.com/eea/eea.progress.editing/blob/master/CONTRIBUTING.md>`_.

Copyright and license
=====================

eea.progress.editing (the Original Code) is free software; you can
redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA 02111-1307 USA.

The Initial Owner of the Original Code is European Environment Agency (EEA).
Portions created by Eau de Web are Copyright (C) 2009 by
European Environment Agency. All Rights Reserved.


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`EEA Web Systems Training`: http://www.youtube.com/user/eeacms/videos?view=1

Secret Scanning
===============

This repository uses the Betterleaks GitHub Action to scan the current
repository content on every push and pull request. The scan uses the rules in
``.gitleaks.toml`` and uploads a ``betterleaks-report`` artifact when a finding
is detected.

If the optional SMTP secrets are configured, failed scans also send an email to
the last commit committer. The workflow expects these repository or
organization secrets:

- ``SMTP_URL``
- ``SMTP_PORT`` (optional, defaults to ``25``)
- ``SMTP_EMAIL``
- ``SMTP_PASSWORD`` (optional if the SMTP server does not require authentication)

Port ``465`` is sent with direct TLS; other ports use the default SMTP
handshake. The email includes a short finding summary from the redacted
Betterleaks report, including the redacted matched line from each finding.

There are three common outcomes:

1. Everything is OK. The ``Betterleaks / Scan for secrets`` check is green and
   no action is needed. Regular references to runtime values are OK, for example::

     token_from_cookie = request.cookies.get("auth_token")

2. A real secret was found. The check is red and the workflow log asks you to
   download the ``betterleaks-report`` artifact. Open the artifact from the
   GitHub Actions run and check the reported file, line and rule. Remove the
   committed value, move it to the proper secret store, and rotate it if it was
   exposed. A report entry looks like this::

     {
       "RuleID": "secret-literal-assignment",
       "File": "src/config.py",
       "StartLine": 12,
       "Secret": "[REDACTED]"
     }

3. The finding is a false positive. Keep the value only if it is clearly not
   sensitive, such as a test fixture, placeholder, or public example. Add
   ``betterleaks:allow`` on the same line and include a short explanation in the
   pull request::

     test_password = "admin"  #betterleaks:allow

Do not add ``betterleaks:allow`` to real credentials.
