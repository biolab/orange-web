===========================
Orange Data Mining Homepage
===========================
Î

Install for development
-----------------------

1. Clone from the repository::

    hg clone https://github.com/biolab/orange-web.git

   You can also use SSH-based URLs or URLs of your forks.

2. Create and activate new `Python virtual environment`_::

    virtualenv ~/.virtualenv/orangeweb
    source ~/.virtualenv/orangeweb/bin/activate

3. Move to location where you cloned the repository and run::

    pip install -r requirements

4. Run::

    python manage.py runserver

   and start developing!

.. _Python virtual environment: http://www.virtualenv.org
