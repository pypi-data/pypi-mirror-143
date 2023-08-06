``algorithmInterface``
==========================================================

.. py:module:: optimeed.optimize.optiAlgorithms.algorithmInterface


Module Contents
---------------

.. py:class:: AlgorithmInterface

   Interface for the optimization algorithm

   .. method:: compute(self, initialVectorGuess, listOfOptimizationVariables)
      :abstractmethod:


      Launch the optimization

      :param initialVectorGuess: list of variables that describe the initial individual
      :param listOfOptimizationVariables: list of :class:`optimeed.optimize.optiVariable.OptimizationVariable`
      :return: vector of optimal variables


   .. method:: set_evaluationFunction(self, evaluationFunction, callback_on_evaluation, numberOfObjectives, numberOfConstraints)
      :abstractmethod:


      Set the evaluation function and all the necessary callbacks

      :param evaluationFunction: check :meth:`~optimeed.optimize.optimizer.evaluateObjectiveAndConstraints`
      :param callback_on_evaluation: check :meth:`~optimeed.optimize.optimizer.callback_on_evaluation`. Call this function after performing the evaluation of the individuals
      :param numberOfObjectives: int, number of objectives
      :param numberOfConstraints: int, number of constraints


   .. method:: set_maxtime(self, maxTime)
      :abstractmethod:


      Set maximum optimization time (in seconds)


   .. method:: get_convergence(self)
      :abstractmethod:


      Get the convergence of the optimization

      :return: :class:`~optimeed.optimize.optiAlgorithms.convergence.interfaceConvergence.InterfaceConvergence`


   .. method:: reset(self)




