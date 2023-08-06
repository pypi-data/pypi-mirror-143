**mathsToPhysics**
=======================================

.. py:module:: optimeed.optimize.mathsToPhysics


.. toctree::
   :titlesonly:
   :maxdepth: 1

   interfaceMathsToPhysics/index.rst
   mathsToPhysics/index.rst


Package Contents
----------------

.. py:class:: MathsToPhysics

   Bases: :class:`optimeed.optimize.mathsToPhysics.interfaceMathsToPhysics.InterfaceMathsToPhysics`

   Dummy yet powerful example of maths to physics.
   The optimization variables are directly injected to the device

   .. method:: fromMathsToPhys(self, xVector, theDevice, theOptimizationVariables)



   .. method:: fromPhysToMaths(self, theDevice, theOptimizationVariables)



   .. method:: __str__(self)




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



