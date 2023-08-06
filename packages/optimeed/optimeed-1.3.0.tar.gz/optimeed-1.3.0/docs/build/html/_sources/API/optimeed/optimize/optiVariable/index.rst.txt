``optiVariable``
=====================================

.. py:module:: optimeed.optimize.optiVariable


Module Contents
---------------

.. py:class:: OptimizationVariable(attributeName)

   Contains information about the optimization of a variable

   .. method:: get_attribute_name(self)


      Return the attribute to set


   .. method:: add_prefix_attribute_name(self, thePrefix)


      Used for nested object, lower the name by prefix. Example: R_ext becomes (thePrefix).R_ext


   .. method:: get_PhysToMaths(self, deviceIn)


      Convert the initial value of the variable contained in the device to optimization variable value

      :param deviceIn: :class:`~optimeed.InterfaceDevice.InterfaceDevice`
      :return: value of the corresponding optimization variable


   .. method:: do_MathsToPhys(self, variableValue, deviceIn)


      Apply the value to the device


   .. method:: __str__(self)




.. py:class:: Real_OptimizationVariable(attributeName, val_min, val_max)

   Bases: :class:`optimeed.optimize.optiVariable.OptimizationVariable`

   Real (continuous) optimization variable. Most used type

   .. method:: get_min_value(self)



   .. method:: get_max_value(self)



   .. method:: get_PhysToMaths(self, deviceIn)



   .. method:: do_MathsToPhys(self, value, deviceIn)



   .. method:: __str__(self)




.. py:class:: Binary_OptimizationVariable

   Bases: :class:`optimeed.optimize.optiVariable.OptimizationVariable`

   Boolean (True/False) optimization variable.

   .. method:: get_PhysToMaths(self, deviceIn)



   .. method:: do_MathsToPhys(self, value, deviceIn)



   .. method:: __str__(self)




.. py:class:: Integer_OptimizationVariable(attributeName, val_min, val_max)

   Bases: :class:`optimeed.optimize.optiVariable.OptimizationVariable`

   Integer variable, in [min_value, max_value]

   .. method:: get_min_value(self)



   .. method:: get_max_value(self)



   .. method:: get_PhysToMaths(self, deviceIn)



   .. method:: do_MathsToPhys(self, value, deviceIn)



   .. method:: __str__(self)




