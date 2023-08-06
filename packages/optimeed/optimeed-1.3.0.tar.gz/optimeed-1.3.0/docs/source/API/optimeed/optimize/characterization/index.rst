**characterization**
=========================================

.. py:module:: optimeed.optimize.characterization


.. toctree::
   :titlesonly:
   :maxdepth: 1

   characterization/index.rst
   interfaceCharacterization/index.rst


Package Contents
----------------

.. py:class:: InterfaceCharacterization

   Interface for the evaluation of a device

   .. method:: compute(self, theDevice)
      :abstractmethod:


      Action to perform to characterize (= compute the objective function) of the device.

      :param theDevice: the device to characterize


   .. method:: __str__(self)




.. py:class:: Characterization

   Bases: :class:`optimeed.optimize.characterization.interfaceCharacterization.InterfaceCharacterization`

   .. method:: compute(self, theDevice)




