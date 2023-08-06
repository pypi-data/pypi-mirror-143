``converter``
========================================

.. py:module:: optimeed.core.ansi2html.converter


Module Contents
---------------

.. data:: ANSI_FULL_RESET
   :annotation: = 0

   

.. data:: ANSI_INTENSITY_INCREASED
   :annotation: = 1

   

.. data:: ANSI_INTENSITY_REDUCED
   :annotation: = 2

   

.. data:: ANSI_INTENSITY_NORMAL
   :annotation: = 22

   

.. data:: ANSI_STYLE_ITALIC
   :annotation: = 3

   

.. data:: ANSI_STYLE_NORMAL
   :annotation: = 23

   

.. data:: ANSI_BLINK_SLOW
   :annotation: = 5

   

.. data:: ANSI_BLINK_FAST
   :annotation: = 6

   

.. data:: ANSI_BLINK_OFF
   :annotation: = 25

   

.. data:: ANSI_UNDERLINE_ON
   :annotation: = 4

   

.. data:: ANSI_UNDERLINE_OFF
   :annotation: = 24

   

.. data:: ANSI_CROSSED_OUT_ON
   :annotation: = 9

   

.. data:: ANSI_CROSSED_OUT_OFF
   :annotation: = 29

   

.. data:: ANSI_VISIBILITY_ON
   :annotation: = 28

   

.. data:: ANSI_VISIBILITY_OFF
   :annotation: = 8

   

.. data:: ANSI_FOREGROUND_CUSTOM_MIN
   :annotation: = 30

   

.. data:: ANSI_FOREGROUND_CUSTOM_MAX
   :annotation: = 37

   

.. data:: ANSI_FOREGROUND_256
   :annotation: = 38

   

.. data:: ANSI_FOREGROUND_DEFAULT
   :annotation: = 39

   

.. data:: ANSI_BACKGROUND_CUSTOM_MIN
   :annotation: = 40

   

.. data:: ANSI_BACKGROUND_CUSTOM_MAX
   :annotation: = 47

   

.. data:: ANSI_BACKGROUND_256
   :annotation: = 48

   

.. data:: ANSI_BACKGROUND_DEFAULT
   :annotation: = 49

   

.. data:: ANSI_NEGATIVE_ON
   :annotation: = 7

   

.. data:: ANSI_NEGATIVE_OFF
   :annotation: = 27

   

.. data:: ANSI_FOREGROUND_HIGH_INTENSITY_MIN
   :annotation: = 90

   

.. data:: ANSI_FOREGROUND_HIGH_INTENSITY_MAX
   :annotation: = 97

   

.. data:: ANSI_BACKGROUND_HIGH_INTENSITY_MIN
   :annotation: = 100

   

.. data:: ANSI_BACKGROUND_HIGH_INTENSITY_MAX
   :annotation: = 107

   

.. data:: VT100_BOX_CODES
   

   

.. data:: _latex_template
   :annotation: = \documentclass{scrartcl}
\usepackage[utf8]{inputenc}
\usepackage{fancyvrb}
\usepackage[usenames,dvipsnames]{xcolor}
%% \definecolor{red-sd}{HTML}{7ed2d2}

\title{%(title)s}

\fvset{commandchars=\\\{\}}

\begin{document}

\begin{Verbatim}
%(content)s
\end{Verbatim}
\end{document}


   

.. data:: _html_template
   

   

.. py:class:: _State

   Bases: :class:`object`

   .. method:: reset(self)



   .. method:: adjust(self, ansi_code, parameter=None)



   .. method:: to_css_classes(self)




.. function:: linkify(line, latex_mode)


.. function:: map_vt100_box_code(char)


.. function:: _needs_extra_newline(text)


.. py:class:: CursorMoveUp

   Bases: :class:`object`


.. py:class:: Ansi2HTMLConverter(latex=False, inline=False, dark_bg=True, line_wrap=True, font_size='normal', linkify=False, escaped=True, markup_lines=False, output_encoding='utf-8', scheme='ansi2html', title='')

   Bases: :class:`object`

   Convert Ansi color codes to CSS+HTML

   Example:
   >>> conv = Ansi2HTMLConverter()
   >>> ansi = " ".join(sys.stdin.readlines())
   >>> html = conv.convert(ansi)

   .. method:: apply_regex(self, ansi)



   .. method:: _apply_regex(self, ansi, styles_used)



   .. method:: _collapse_cursor(self, parts)


      Act on any CursorMoveUp commands by deleting preceding tokens 


   .. method:: prepare(self, ansi='', ensure_trailing_newline=False)


      Load the contents of 'ansi' into this object 


   .. method:: attrs(self)


      Prepare attributes for the template 


   .. method:: convert(self, ansi, full=True, ensure_trailing_newline=False)



   .. method:: produce_headers(self)




.. function:: main()

   $ ls --color=always | ansi2html > directories.html
   $ sudo tail /var/log/messages | ccze -A | ansi2html > logs.html
   $ task burndown | ansi2html > burndown.html


