``optimizer``
==================================

.. py:module:: optimeed.optimize.optimizer


Module Contents
---------------

.. data:: default
   

   

.. py:class:: PipeOptimization

   Provides a live interface of the current optimization

   .. method:: get_device(self)


      :return: :class:`~optimeed.core.interfaceDevice.InterfaceDevice` (not process safe, deprecated) 


   .. method:: get_historic(self)


      :return: :class:`~OptiHistoric` 


   .. method:: set_device(self, theDevice)



   .. method:: set_historic(self, theHistoric)




.. py:class:: OptiHistoric(**kwargs)

   Bases: :class:`object`

   Contains all the points that have been evaluated

   .. py:class:: _pointData(currTime, objectives, constraints)

      .. attribute:: time
         :annotation: :float

         

      .. attribute:: objectives
         :annotation: :List[float]

         

      .. attribute:: constraints
         :annotation: :List[float]

         


   .. attribute:: _DEVICE
      :annotation: = autosaved

      

   .. attribute:: _LOGOPTI
      :annotation: = logopti

      

   .. attribute:: _RESULTS
      :annotation: = results

      

   .. attribute:: _CONVERGENCE
      :annotation: = optiConvergence

      

   .. method:: add_point(self, device, currTime, objectives, constraints)



   .. method:: set_results(self, devicesList)



   .. method:: set_convergence(self, theConvergence)



   .. method:: set_info(self, theInfo)



   .. method:: save(self)



   .. method:: get_results(self)



   .. method:: get_convergence(self)


      :return: convergence :class:`~optimeed.optimize.optiAlgorithms.convergence.interfaceConvergence.InterfaceConvergence` 


   .. method:: get_devices(self)


      :return: List of devices (ordered by evaluation number) 


   .. method:: get_logopti(self)


      :return: Log optimization (to check the convergence) 



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




