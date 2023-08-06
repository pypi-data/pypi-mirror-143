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
          --color      View translated text with colour.
          --progress   Show progress bar.
     -l,  --languages  Show all supported languages.
     -v,  --version    Print the version and exit.
     -h,  --help       Show this message and exit.


Example
-------

.. code-block:: bash

   $ subtrs subtitles.srt el --progress
   [1/1] Translate into greek |########                        | 27% - 24s


An example which create multiple subtitles files:

.. code-block:: bash

   $ subtrs subtitles.srt zh-cn,de,ru --color
   [1/3] Translate into chinese

   [en] << - Did you hear that?

   [zh-cn] >> - 你听到了吗？

   [en] << - Hear what?

   [zh-cn] >> - 听到什么？

   [en] << Are you sure this line is clean?

   [zh-cn] >> 你确定这条线是干净的吗？

   [en] << Yeah, of course I'm sure.

   [zh-cn] >> 是的，我当然确定。

   [en] << I better go.

   [zh-cn] >> 我最好去。

   [en] << - Freeze! Police!

   [zh-cn] >> - 冻结！警察！

   [en] << - Hands on your head!

   [zh-cn] >> - 把手放在你的头上！

   [en] << Do it! Do it now!

   [zh-cn] >> 去做吧！现在做
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
       ├── __metadata__.py
       └── main.py


Donate
------

If you feel satisfied with this project and want to thanks me make a donation.

.. image:: https://gitlab.com/dslackw/images/raw/master/donate/paypaldonate.png
   :target: https://www.paypal.me/dslackw

          
Copyright
---------

- Copyright 2022 © dslackw


License
-------
`MIT <https://gitlab.com/dslackw/subtrs/-/blob/main/LICENSE.txt>`_
