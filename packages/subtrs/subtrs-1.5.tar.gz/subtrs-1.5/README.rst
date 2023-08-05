.. contents:: Table of Contents:

About
-----

**Translate Video Subtitles**

**subtrs** is a simple tool that translates subtitles from files.

| The main idea came when using the YouTube auto-tool to translate my videos subtitles, I saw that the translation sucked.
| So I decided to create this simple tool and translate my subtitles more successfully.

|

| Enjoy!

|

.. image:: https://gitlab.com/dslackw/images/raw/master/subtrs/subtrs.gif
   :target: https://gitlab.com/dslackw/subtrs

	
Installing
----------

.. code-block:: bash

   $ pip3 install subtrs --upgrade

 
Command line usage
------------------

.. code-block:: bash

   Usage: subtrs [subtitles_file] [destination languages]

          Simple tool that trlanslates video subtitles

          Support subtitles files [*.sbv, *.vtt, *.srt]
          Destination languages [en,de,ru] etc.

   Optional arguments:
          --color      View translate text language with colour.
          --silent     Silent method, without viewing.
     -l,  --languages  Show all supported languages.
     -v,  --version    Show the version and exit.
     -h,  --help       Show this message and exit.


Example
-------

An example which create multiple subtitles files:

.. code-block:: bash

   $ subtrs captions.srt en,de,ru --color

This command should translate and create three different files, one with English subtitles, one with German and one with Russia subtitles.

Project layout
--------------

.. code-block:: bash

	├── CHANGES.md
	├── LICENSE.txt
	├── README.rst
	├── bin
	│   ├── __init.py__
	│   └── subtrs
	├── requirements.txt
	├── setup.py
	└── subtrs
		├── __init__.py
		└── main.py

Donate
------

If you feel satisfied with this project and want to thanks me make a donation.

.. image:: https://gitlab.com/dslackw/images/raw/master/donate/paypaldonate.png
   :target: https://www.paypal.me/dslackw

          
Copyright
---------

- Copyright 2022 © dslackw
