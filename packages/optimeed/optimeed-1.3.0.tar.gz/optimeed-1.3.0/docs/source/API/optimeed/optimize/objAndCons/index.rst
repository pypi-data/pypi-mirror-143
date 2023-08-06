**objAndCons**
===================================

.. py:module:: optimeed.optimize.objAndCons


.. toctree::
   :titlesonly:
   :maxdepth: 1

   fastObjCons/index.rst
   interfaceObjCons/index.rst


Package Contents
----------------

.. py:class:: FastObjCons(constraintEquation, name=None)

   Bases: :class:`optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`

   Convenience class to create an objective or a constraint very fast.

   .. method:: compute(self, theDevice)



   .. method:: get_name(self)




.. py:class:: InterfaceObjCons

   Interface class for objectives and constraints. The objective is to MINIMIZE and the constraint has to respect VALUE <= 0

   .. method:: compute(self, theDevice)
      :abstractmethod:


      Get the value of the objective or the constraint. The objective is to MINIMIZE and the constraint has to respect VALUE <= 0

      :param theDevice: Input device that has already been evaluated
      :return: float.


   .. method:: get_name(self)



   .. method:: __str__(self)




