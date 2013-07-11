Pops: Bootstrapping Django's Admin
=================================
Introducing Django's `admin`_ to Twitter's `Bootstrap`_.

This is built on top of the work of `django-admintools-bootstrap`_ and utilizes
`django-admin-tools`_.

.. warning:: This is development software and prone to constant change.  Tread carefully.


.. _admin: https://docs.djangoproject.com/en/1.4/ref/contrib/admin/
.. _Bootstrap: http://twitter.github.com/bootstrap/
.. _django-admintools-bootstrap: https://bitbucket.org/salvator/django-admintools-bootstrap
.. _django-admin-tools: http://django-admin-tools.readthedocs.org/en/latest/index.html


Installation & Configuration
----------------------------
You can install the development version of this package using `pip`_:

::

    $ git clone git://github.com/tswicegood/pops.git
    $ cd pops && pip install .

Next, you must add ``pops`` to the list of ``INSTALLED_APPS`` in your Django
settings before `django-admin-tools`_.  Note, you have to have a properly
`installed and configured`_ admin-tools package in order to use pops.

.. _pip: http://www.pip-installer.org/
.. _installed and configured: http://django-admin-tools.readthedocs.org/en/latest/quickstart.html#installing-django-admin-tools


License
-------
Copyright 2012-2013 Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Other Software
--------------
Pops is a fork of `django-admintools-bootstrap`_.  That code is available under
an MIT license.  All code listed below is copyrighted by their original owners
and distributed under their accompanying licenses.  See the various directories
in ``vendor/`` for full licensing information.

* http://addyosmani.github.com/jquery-ui-bootstrap/
* http://twitter.github.com/bootstrap/
* https://bitbucket.org/izi/django-admin-tools/
* http://www.crummy.com/software/BeautifulSoup/
* https://github.com/jezdez/django-appconf

What's in a name?
-----------------
"Pops" is one of Louis Armstrong's `nicknames`_.  This project is being done
for integration with the `Armstrong Project`_, which is named after Mr.
Armstrong.  Pops is completely independent of the project, however, so we
decided to give it a different, albeit still related, name.

.. _nicknames: http://en.wikipedia.org/wiki/Louis_Armstrong#Nicknames
.. _Armstrong Project: http://armstrongcms.org/
