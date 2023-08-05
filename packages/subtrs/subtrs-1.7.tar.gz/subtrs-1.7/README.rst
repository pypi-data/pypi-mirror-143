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
          --progress   Show progress bar.
     -l,  --languages  Show all supported languages.
     -v,  --version    Print the version and exit.
     -h,  --help       Show this message and exit.


Example
-------

.. code-block:: bash

   $ subtrs captions.srt el --progress
   Processing |########                        | 47/180


An example which create multiple subtitles files:

.. code-block:: bash

   $ subtrs matrix_en.srt zh-cn,de,ru --color

   [en] << Is everything in place?

   [zh-cn] >> 一切都到位了吗？

   [en] << You're not to relieve me.

   [zh-cn] >> 你不是来解救我的。

   [en] << I know, but I felt like taking a shift.

   [zh-cn] >> 我知道，但我想换个班。

   [en] << You like him, don't you?

   [zh-cn] >> 你喜欢他，不是吗？

   [en] << You like watching him.

   [zh-cn] >> 你喜欢看他。

   [en] << Don't be ridiculous.

   [zh-cn] >> 别开玩笑了。

   [en] << We're going to kill him.

   [zh-cn] >> 我们要杀了他。
   .
   .
   .
   
This command should translate and create three different files, one with Chinese subtitles, one with German and one with Russia subtitles.



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
