``fastPlot``
==================================

.. py:module:: optimeed.visualize.fastPlot


Module Contents
---------------

.. py:class:: PlotHolders

   .. method:: add_plot(self, x, y, **kwargs)



   .. method:: get_wgGraphs(self)



   .. method:: new_plot(self)



   .. method:: set_title(self, theTitle, **kwargs)



   .. method:: reset(self)



   .. method:: axis_equal(self)




.. py:class:: WindowHolders

   .. method:: set_currFigure(self, currFigure)



   .. method:: add_plot(self, *args, **kwargs)



   .. method:: set_title(self, *args, **kwargs)



   .. method:: new_figure(self)



   .. method:: new_plot(self)



   .. method:: show(self)



   .. method:: get_curr_plotHolder(self)



   .. method:: get_wgGraphs(self, fig=None)



   .. method:: get_all_figures(self)



   .. method:: axis_equal(self)




.. data:: myWindows
   

   

.. function:: plot(x, y, hold=False, **kwargs)

   Plot new trace


.. function:: show()

   Show (start qt mainloop) graphs. Blocking


.. function:: figure(numb)

   Set current figure


.. function:: new_plot()

   Add new plot


.. function:: set_title(theTitle, **kwargs)

   Set title of the plot


.. function:: axis_equal()


.. function:: get_all_figures()

   Get all existing figures


.. function:: get_wgGraphs(fig=None)

   Advanced option.
   :return: :class:`~optimeed.visualize.gui.widgets.widget_graphs_visual.widget_graphs_visual`


