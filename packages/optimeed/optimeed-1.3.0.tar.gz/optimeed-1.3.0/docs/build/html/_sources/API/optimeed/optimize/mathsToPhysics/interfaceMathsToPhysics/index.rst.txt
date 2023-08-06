``interfaceMathsToPhysics``
===============================================================

.. py:module:: optimeed.optimize.mathsToPhysics.interfaceMathsToPhysics


Module Contents
---------------

.. py:class:: InterfaceMathsToPhysics

   Interface to transform output from the optimizer to meaningful variables of the device

   .. method:: fromMathsToPhys(self, xVector, theDevice, opti_variables)
      :abstractmethod:


      Transforms an input vector coming from the optimization (e.g. [0.23, 4, False]) to "meaningful" variable (ex: length, number of poles, flag).

      :param xVector: List of optimization variables from the optimizer
      :param theDevice: :class:`~optimeed.InterfaceDevice.InterfaceDevice`
      :param opti_variables: list of :class:`~optimeed.optimize.OptimizationVariable.OptimizationVariable`


   .. method:: fromPhysToMaths(self, theDevice, opti_variables)
      :abstractmethod:


      Extracts a mathematical vector from meaningful variable of the Device

      :param theDevice: :class:`~optimeed.InterfaceDevice.InterfaceDevice`
      :param opti_variables: list of :class:`~optimeed.optimize.OptimizationVariable.OptimizationVariable`
      :return: List of optimization variables



