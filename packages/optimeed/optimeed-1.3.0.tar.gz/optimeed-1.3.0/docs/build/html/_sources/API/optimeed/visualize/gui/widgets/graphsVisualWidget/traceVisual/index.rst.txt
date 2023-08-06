``traceVisual``
====================================================================

.. py:module:: optimeed.visualize.gui.widgets.graphsVisualWidget.traceVisual


Module Contents
---------------

.. py:class:: TraceVisual(theData, theWGPlot, highlight_last)

   Bases: :class:`PyQt5.QtCore.QObject`

   Defines a trace in a graph.

   .. py:class:: _ModifiedPaintElem

      Hidden class to manage brushes or pens

      .. method:: add_modified_paintElem(self, index, newPaintElem)



      .. method:: modify_paintElems(self, paintElemsIn_List)


         Apply transformation to paintElemsIn_List


         :param paintElemsIn_List: list of brushes or pens to modify
         :return: False if nothing has been modified, True is something has been modified


      .. method:: reset_paintElem(self, index)


         Remove transformation of point index


      .. method:: reset(self)




   .. attribute:: signal_must_update
      

      

   .. method:: hide_points(self)


      Hide all the points


   .. method:: get_color(self)


      Get colour of the trace, return tuple (r,g,b)


   .. method:: set_color(self, color)


      Set colour of the trace, argument as tuple (r,g,b)


   .. method:: get_base_symbol_brush(self)


      Get symbol brush configured for this trace, return :class:`pg.QBrush`


   .. method:: get_base_pen(self)


      Get pen configured for this trace, return :class:`pg.QPen`


   .. method:: get_base_symbol_pen(self)


      Get symbol pen configured for this trace, return :class:`pg.QPen`


   .. method:: get_base_symbol(self)


      Get base symbol configured for this trace, return str of the symbol (e.g. 'o')


   .. method:: get_symbol(self, size)


      Get actual symbols for the trace. If the symbols have been modified: return a list which maps each points to a symbol.
      Otherwise: return :meth:TraceVisual.get_base_symbol()


   .. method:: updateTrace(self)


      Forces the trace to refresh.


   .. method:: get_length(self)


      Return number of data to plot


   .. method:: hide(self)


      Hides the trace


   .. method:: show(self)


      Shows the trace


   .. method:: toggle(self, boolean)


      Toggle the trace (hide/show)


   .. method:: get_data(self)


      Get data to plot :class:`~optimeed.visualize.graphs.Graphs.Data`


   .. method:: get_brushes(self, size)


      Get actual brushes for the trace (=symbol filling). return a list which maps each points to a symbol brush


   .. method:: set_brush(self, indexPoint, newbrush, update=True)


      Set the symbol brush for a specific point:

      :param indexPoint: Index of the point (in the graph) to modify
      :param newbrush: either QBrush or tuple (r, g, b) of the new brush
      :param update: if True, update the trace afterwards. This is slow operation.


   .. method:: set_symbol(self, indexPoint, newSymbol, update=True)


      Set the symbol shape for a specific point:

      :param indexPoint: Index of the point (in the graph) to modify
      :param newSymbol: string of the new symbol (e.g.: 'o')
      :param update: if True, update the trace afterwards. This is slow operation.


   .. method:: set_brushes(self, list_indexPoint, list_newbrush)


      Same as :meth:`~TraceVisual.set_brush` but by taking a list as input


   .. method:: reset_brush(self, indexPoint, update=True)


      Reset the brush of the point indexpoint


   .. method:: reset_all_brushes(self)


      Reset all the brushes


   .. method:: reset_symbol(self, indexPoint, update=True)


      Reset the symbol shape of the point indexpoint


   .. method:: get_symbolPens(self, size)


      Get actual symbol pens for the trace (=symbol outline). return a list which maps each points to a symbol pen


   .. method:: set_symbolPen(self, indexPoint, newPen, update=True)


      Set the symbol shape for a specific point:

      :param indexPoint: Index of the point (in the graph) to modify
      :param newPen: QPen item or tuple of the color (r,g,b)
      :param update: if True, update the trace afterwards. This is slow operation.


   .. method:: set_symbolPens(self, list_indexPoint, list_newpens)


      Same as :meth:`~TraceVisual.set_symbolPen` but by taking a list as input


   .. method:: reset_symbolPen(self, indexPoint)


      Reset the symbol pen of the point indexpoint


   .. method:: reset_all_symbolPens(self)


      Reset all the symbol pens


   .. method:: set_pen_linestyle(thePen, linestyle)
      :staticmethod:


      Transform a pen for dashed lines:

      :param thePen: QPen item
      :param linestyle: str (e.g.: '.', '.-', '--', ...)


   .. method:: get_point(self, indexPoint)


      Return object pyqtgraph.SpotItem



