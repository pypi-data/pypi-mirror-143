``displayOptimization``
=============================================

.. py:module:: optimeed.visualize.displayOptimization


Module Contents
---------------

.. function:: check_if_must_plot(elem)


.. py:class:: OptimizationDisplayer(thePipeOpti, listOfObjectives, theOptimizer, additionalWidgets=None)

   Bases: :class:`optimeed.core.Option_class`

   Class used to display optimization process in real time

   .. attribute:: signal_optimization_over
      

      

   .. attribute:: SHOW_CONSTRAINTS
      :annotation: = 0

      

   .. method:: set_actionsOnClick(self, theList)


      Set actions to perform on click, list of :class:`~optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`


   .. method:: generate_optimizationGraphs(self)


      Generates the optimization graphs.
      :return: :class:`~optimeed.core.graphs.Graphs`, :class:`~optimeed.core.linkDataGraph.LinkDataGraph`, :class:'~optimeed.visulaize.gui.widgets.widget_graphs_visual.widget_graphs_visual


   .. method:: __change_appearance_violate_constraints(self)



   .. method:: __refresh(self)



   .. method:: start_autorefresh(self, timer_autosave)



   .. method:: stop_autorefresh(self)



   .. method:: __set_graphs_disposition(self)


      Set nicely the graphs disposition


   .. method:: launch_optimization(self, refresh_time=0.1)


      Perform the optimization and spawn the convergence graphs afterwards.


   .. method:: __callback_optimization(self)



   .. method:: close_windows(self)



   .. method:: display_graphs(theGraphs)
      :staticmethod:



   .. method:: create_main_window(self)


      From the widgets and the actions on click, spawn a window and put a gui around widgetsGraphsVisual.



