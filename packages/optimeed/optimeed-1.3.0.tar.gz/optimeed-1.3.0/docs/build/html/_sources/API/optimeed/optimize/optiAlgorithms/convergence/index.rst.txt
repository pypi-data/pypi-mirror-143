**convergence**
===================================================

.. py:module:: optimeed.optimize.optiAlgorithms.convergence


.. toctree::
   :titlesonly:
   :maxdepth: 1

   evolutionaryConvergence/index.rst
   hypervolume/index.rst
   interfaceConvergence/index.rst


Package Contents
----------------

.. py:class:: EvolutionaryConvergence(is_monobj=False)

   Bases: :class:`optimeed.optimize.optiAlgorithms.convergence.interfaceConvergence.InterfaceConvergence`

   convergence class for population-based algorithm

   .. attribute:: objectives_per_step
      :annotation: :Dict[int, List[List[float]]]

      

   .. attribute:: constraints_per_step
      :annotation: :Dict[int, List[List[float]]]

      

   .. attribute:: is_monobj
      :annotation: :bool

      

   .. method:: set_points_at_step(self, theStep, theObjectives_list, theConstraints_list)



   .. method:: get_pareto_convergence(self)



   .. method:: get_last_pareto(self)



   .. method:: get_hypervolume_convergence(self, refPoint=None)


      Get the hypervolume indicator on each step

      :param refPoint: Reference point needed to compute the hypervolume. If None is specified, uses the nadir point Example: [10, 10] for two objectives.
      :return:


   .. method:: get_nb_objectives(self)



   .. method:: get_nadir_point(self)



   .. method:: get_nadir_point_all_steps(self)



   .. method:: get_nb_steps(self)



   .. method:: get_population_size(self)



   .. method:: get_graphs(self)




.. py:class:: InterfaceConvergence

   Simple interface to visually get the convergence of any optimization problem

   .. method:: get_graphs(self)
      :abstractmethod:


      Return :class:`~optimeed.core.graphs.Graphs`



