.. Optiviz documentation master file, created by
   sphinx-quickstart on Wed Sep 11 10:27:32 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Optimeed's documentation!
====================================

Optimeed is a free open source package that allows to perform optimization and data visualization/management.

Requirements
------------

* PyQt5 for visualisation -> :code:`pip install PyQt5`
* `pyopengl` for visualisation -> :code:`pip install PyOpenGL`
* Numpy -> :code:`pip install numpy`
* Optional
    * pandas which is only used to export excel files -> :code:`pip install pandas`
    * :code:`nlopt` library for using other types of algorithm. -> :code:`pip install nlopt`
    * inkscape software for exporting graphs in .png and .pdf)

Installation
------------

To install the latest optimeed release, run the following command::

    pip install optimeed

To install the latest development version of optimeed, run the following commands::

   git clone https://git.immc.ucl.ac.be/chdegreef/optimeed.git
   cd optimeed
   python setup.py install


Quickstart
----------

Examples can be found `on the tutorial folder <https://git.immc.ucl.ac.be/chdegreef/optimeed>`_ .

.. toctree::
   :maxdepth: 2

   Quickstart/OptiModule_explanation
   Quickstart/VisuModule_explanation
   Quickstart/Load_save_explanation


Gallery
-------
.. toctree::
   :maxdepth: 2

   gallery


License and support
-------------------
.. toctree::
   :maxdepth: 2

   support


API
---
.. toctree::
   :maxdepth: 8
   :titlesonly:

   API/optimeed/index

Developer guide
---------------


.. toctree::
   :maxdepth: 2

   dev
