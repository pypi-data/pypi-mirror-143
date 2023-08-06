**optiAlgorithms**
=======================================

.. py:module:: optimeed.optimize.optiAlgorithms


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 8

   convergence/index.rst


.. toctree::
   :titlesonly:
   :maxdepth: 1

   NLOpt_Algorithm/index.rst
   algorithmInterface/index.rst
   multiObjective_GA/index.rst


Package Contents
----------------

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




