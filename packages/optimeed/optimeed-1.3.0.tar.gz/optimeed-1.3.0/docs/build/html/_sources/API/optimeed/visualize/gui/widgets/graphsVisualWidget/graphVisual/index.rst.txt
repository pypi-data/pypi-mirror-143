``graphVisual``
====================================================================

.. py:module:: optimeed.visualize.gui.widgets.graphsVisualWidget.graphVisual


Module Contents
---------------

.. py:class:: GraphVisual(theWidgetGraphVisual)

   Provide an interface to a graph. A graph contains traces.

   .. method:: set_fontTicks(self, fontSize, fontname=None)


      Set font of the ticks

      :param fontSize: Size of the font
      :param fontname: Name of the font


   .. method:: set_numberTicks(self, number, axis)


      Set the number of ticks to be displayed

      :param number: Number of ticks for the axis
      :param axis: Axis (string, "bottom", "left", "right", "top")
      :return:


   .. method:: set_fontLabel(self, fontSize, color='#000', fontname=None)


      Set font of the axis labels

      :param fontSize: font size
      :param color: color in hexadecimal (str)
      :param fontname: name of the font


   .. method:: get_legend(self)


      Get the legend


   .. method:: get_axis(self, axis)


      Get the axis

      :param axis: Axis (string, "bottom", "left", "right", "top")
      :return: axis object


   .. method:: set_fontLegend(self, font_size, font_color, fontname=None)



   .. method:: set_label_pos(self, orientation, x_offset=0, y_offset=0)



   .. method:: set_color_palette(self, palette)



   .. method:: apply_palette(self)



   .. method:: hide_axes(self)



   .. method:: add_feature(self, theFeature)


      To add any pyqtgraph item to the graph


   .. method:: remove_feature(self, theFeature)


      To remove any pyqtgraph item from the graph


   .. method:: add_data(self, idGraph, theData)



   .. method:: set_graph_properties(self, theTrace)


      This function is automatically called on creation of the graph


   .. method:: set_lims(self, xlim, ylim)


      Set limits of the graphs, xlim or ylim = [val_low, val_high]. Or None.


   .. method:: add_trace(self, idTrace, theTrace)


      Add a :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.TraceVisual.TraceVisual` to the graph, with index idTrace


   .. method:: set_legend(self)


      Set default legend options (color and font)


   .. method:: set_title(self, titleName, **kwargs)


      Set title of the graph

      :param titleName: title to set


   .. method:: get_trace(self, idTrace)


      Return the :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.TraceVisual.TraceVisual` correspondong to the index idTrace


   .. method:: get_all_traces(self)


      Return a dictionary {idtrace: :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.TraceVisual.TraceVisual`}.


   .. method:: delete_trace(self, idTrace)


      Delete the trace of index idTrace


   .. method:: delete(self)


      Delete the graph


   .. method:: linkXToGraph(self, graph)


      Link the axis of the current graph to an other :class:`GraphVisual`


   .. method:: update(self)


      Update the traces contained in the graph


   .. method:: fast_update(self)


      Same as :meth:`~GraphVisual.update` but faster. This is NOT thread safe (cannot be called a second time before finishing operation)


   .. method:: axis_equal(self)



   .. method:: log_mode(self, x=False, y=False)



   .. method:: grid_off(self)


      Turn off grid



