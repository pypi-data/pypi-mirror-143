``NLOpt_Algorithm``
=======================================================

.. py:module:: optimeed.optimize.optiAlgorithms.NLOpt_Algorithm


Module Contents
---------------

.. py:class:: ConvergenceManager

   .. method:: add_point(self, newObj)



   .. method:: set_pop_size(self, popSize)




.. py:class:: NLOpt_Algorithm

   Bases: :class:`optimeed.optimize.optiAlgorithms.algorithmInterface.AlgorithmInterface`, :class:`optimeed.core.Option_class`

   .. attribute:: ALGORITHM
      :annotation: = 0

      

   .. attribute:: POPULATION_SIZE
      :annotation: = 1

      

   .. method:: compute(self, initialVectorGuess, listOfOptimizationVariables)



   .. method:: __set_optimizationVariables(listOfOptimizationVariables, theOptimizationAlgorithm)
      :staticmethod:



   .. method:: set_evaluationFunction(self, evaluationFunction, callback_on_evaluate, numberOfObjectives, _numberOfConstraints)



   .. method:: set_maxtime(self, maxTime)



   .. method:: __str__(self)



   .. method:: get_convergence(self)




