**ansi2html**
==============================

.. py:module:: optimeed.core.ansi2html


.. toctree::
   :titlesonly:
   :maxdepth: 1

   converter/index.rst
   style/index.rst
   util/index.rst


Package Contents
----------------

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




