**optimize**
========================

.. py:module:: optimeed.optimize


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 8

   characterization/index.rst
   mathsToPhysics/index.rst
   objAndCons/index.rst
   optiAlgorithms/index.rst


.. toctree::
   :titlesonly:
   :maxdepth: 1

   optiVariable/index.rst
   optimizer/index.rst


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




.. py:class:: MultiObjective_GA

   Bases: :class:`optimeed.optimize.optiAlgorithms.algorithmInterface.AlgorithmInterface`, :class:`optimeed.core.Option_class`

   Based on `Platypus Library <https://platypus.readthedocs.io/en/docs/index.html>`_.
   Workflow:
   Define what to optimize and which function to call with a :class:`Problem`
   Define the initial population with a :class:`Generator`
   Define the algorithm. As options, define how to evaluate the elements with a :class:`Evaluator`, i.e., for multiprocessing.
   Define what is the termination condition of the algorithm with :class:`TerminationCondition`. Here, termination condition is a maximum time.

   .. attribute:: DIVISION_OUTER
      :annotation: = 0

      

   .. attribute:: OPTI_ALGORITHM
      :annotation: = 1

      

   .. attribute:: NUMBER_OF_CORES
      :annotation: = 2

      

   .. method:: compute(self, initialVectorGuess, listOfOptimizationVariables)



   .. method:: set_evaluationFunction(self, evaluationFunction, callback_on_evaluation, numberOfObjectives, numberOfConstraints)



   .. method:: set_maxtime(self, maxTime)



   .. method:: __str__(self)



   .. method:: get_convergence(self)




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




.. py:class:: Optimizer

   Bases: :class:`optimeed.core.options.Option_class`

   Main optimizing class

   .. attribute:: DISPLAY_INFO
      :annotation: = 1

      

   .. attribute:: KWARGS_OPTIHISTO
      :annotation: = 2

      

   .. method:: set_optimizer(self, theDevice, theObjectiveList, theConstraintList, theOptimizationVariables, theOptimizationAlgorithm=default['Algo'], theCharacterization=default['Charac'], theMathsToPhysics=default['M2P'])


      Prepare the optimizer for the optimization.

      :param theDevice: object of type  :class:`~optimeed.core.interfaceDevice.InterfaceDevice`
      :param theCharacterization: object of type :class:`~optimeed.optimize.characterization.interfaceCharacterization.InterfaceCharacterization`
      :param theMathsToPhysics: object of type :class:`~optimeed.optimize.mathsToPhysics.interfaceMathsToPhysics.InterfaceMathsToPhysics`
      :param theObjectiveList: list of objects of type :class:`~optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`
      :param theConstraintList: list of objects of type :class:`~optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`
      :param theOptimizationAlgorithm: list of objects of type :class:`~optimeed.optimize.optiAlgorithms.algorithmInterface.AlgorithmInterface`
      :param theOptimizationVariables: list of objects of type :class:`~optimeed.optimize.optiVariable.OptimizationVariable`
      :return: :class:`~PipeOptimization`


   .. method:: run_optimization(self)


      Perform the optimization.

      :return: :class:`Collection <optimeed.core.collection.Collection>` of the best optimized devices


   .. method:: set_max_opti_time(self, max_time_sec)



   .. method:: evaluateObjectiveAndConstraints(self, x)


      Evaluates the performances of device associated to entrance vector x. Outputs the objective function and the constraints,
      and other data used in optiHistoric.

      This function is NOT process safe: "self." is actually a FORK in multiprocessing algorithms.
      It means that the motor originally contained in self. is modified only in the fork, and only gathered by reaching the end of the fork.
      It is not (yet?) possible to access this motor on the main process before the end of the fork. This behaviour could be changed by using pipes or Managers.

      :param x: Input mathematical vector from optimization algorithm
      :return: dictionary, containing objective values (list of scalar), constraint values (list of scalar), and other info (motor, time)


   .. method:: callback_on_evaluation(self, returnedValues)


      Save the output of evaluateObjectiveAndConstraints to optiHistoric.
      This function should be called by the optimizer IN a process safe context.


   .. method:: formatInfo(self)




