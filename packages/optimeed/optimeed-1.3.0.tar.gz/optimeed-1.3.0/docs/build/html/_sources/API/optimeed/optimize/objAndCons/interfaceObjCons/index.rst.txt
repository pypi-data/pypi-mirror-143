``interfaceObjCons``
====================================================

.. py:module:: optimeed.optimize.objAndCons.interfaceObjCons


Module Contents
---------------

.. py:class:: InterfaceObjCons

   Interface class for objectives and constraints. The objective is to MINIMIZE and the constraint has to respect VALUE <= 0

   .. method:: compute(self, theDevice)
      :abstractmethod:


      Get the value of the objective or the constraint. The objective is to MINIMIZE and the constraint has to respect VALUE <= 0

      :param theDevice: Input device that has already been evaluated
      :return: float.


   .. method:: get_name(self)



   .. method:: __str__(self)




