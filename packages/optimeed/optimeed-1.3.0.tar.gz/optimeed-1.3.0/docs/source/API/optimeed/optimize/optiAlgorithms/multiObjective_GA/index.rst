``multiObjective_GA``
=========================================================

.. py:module:: optimeed.optimize.optiAlgorithms.multiObjective_GA


Module Contents
---------------

.. py:class:: My_OMOPSO(problem, epsilons, **kwargs)

   Bases: :class:`optimeed.optimize.optiAlgorithms.platypus.algorithms.OMOPSO`


.. py:class:: MyConvergence(*args, **kwargs)

   Bases: :class:`optimeed.optimize.optiAlgorithms.convergence.InterfaceConvergence`, :class:`optimeed.optimize.optiAlgorithms.platypus.core.Archive`

   .. attribute:: conv
      :annotation: :EvolutionaryConvergence

      

   .. method:: extend(self, solutions)



   .. method:: get_graphs(self)




.. py:class:: MyProblem(theOptimizationVariables, nbr_objectives, nbr_constraints, evaluationFunction)

   Bases: :class:`optimeed.optimize.optiAlgorithms.platypus.core.Problem`

   Automatically sets the optimization problem

   .. method:: evaluate(self, solution)




.. py:class:: MyGenerator(initialVectorGuess)

   Bases: :class:`optimeed.optimize.optiAlgorithms.platypus.Generator`

   Population generator to insert initial individual

   .. method:: generate(self, problem)




.. py:class:: MyTerminationCondition(maxTime)

   Bases: :class:`optimeed.optimize.optiAlgorithms.platypus.core.TerminationCondition`

   .. method:: initialize(self, algorithm)



   .. method:: shouldTerminate(self, algorithm)




.. py:class:: MyMapEvaluator(callback_on_evaluation)

   Bases: :class:`optimeed.optimize.optiAlgorithms.platypus.evaluator.Evaluator`

   .. method:: evaluate_all(self, jobs, **kwargs)




.. py:class:: MyMultiprocessEvaluator(callback_on_evaluation, numberOfCores)

   Bases: :class:`optimeed.optimize.optiAlgorithms.platypus.evaluator.Evaluator`

   .. method:: evaluate_all(self, jobs, **kwargs)



   .. method:: close(self)




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




