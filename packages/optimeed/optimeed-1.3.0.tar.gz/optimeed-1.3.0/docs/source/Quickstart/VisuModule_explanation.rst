Quickstart Visualization
========================

Visualization implies to have a GUI, which will help to display many things: graphs, text, 3D representations, ...
This software provides a clean interface to PyQt. PyQt works that way:

* A QMainWindow that includes layouts, (ex: horizontal, vertical, grid, ...)
* Layouts can include widgets.
* Widgets can be anything: buttons, menu, opengl 3D representation, graphs, ... Several high-level widgets are proposed, check :mod:`optimeed.visualize.gui.widgets` .

Simple gui using OpenGL:
------------------------

.. literalinclude:: ../../../tutorial/visualisation_openGL/example.py

Advanced visualization:
-----------------------

.. literalinclude:: ../../../tutorial/loadOptiData/example.py
