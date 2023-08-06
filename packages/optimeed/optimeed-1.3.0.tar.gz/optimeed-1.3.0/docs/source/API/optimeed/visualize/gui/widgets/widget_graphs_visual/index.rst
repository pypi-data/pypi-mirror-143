``widget_graphs_visual``
==========================================================

.. py:module:: optimeed.visualize.gui.widgets.widget_graphs_visual


Module Contents
---------------

.. py:class:: on_graph_click_interface

   Interface class for the action to perform when a point is clicked

   .. method:: graph_clicked(self, theGraphsVisual, index_graph, index_trace, indices_points)
      :abstractmethod:


      Action to perform when a graph is clicked

      :param theGraphsVisual: class widget_graphs_visual that has called the method
      :param index_graph: Index of the graph that has been clicked
      :param index_trace: Index of the trace that has been clicked
      :param indices_points: graph Indices of the points that have been clicked
      :return:


   .. method:: get_name(self)
      :abstractmethod:




.. py:class:: widget_graphs_visual(theGraphs, **kwargs)

   Bases: :class:`PyQt5.QtWidgets.QWidget`

   Widget element to draw a graph. The traces and graphs to draw are defined in :class:`~optimeed.visualize.graphs.Graphs.Graphs` taken as argument.
   This widget is linked to the excellent third-party library pyqtgraph, under MIT license

   .. attribute:: signal_must_update
      

      

   .. attribute:: signal_graph_changed
      

      

   .. method:: set_graph_disposition(self, indexGraph, row=1, col=1, rowspan=1, colspan=1)


      Change the graphs disposition.

      :param indexGraph: index of the graph to change
      :param row: row where to place the graph
      :param col: column where to place the graph
      :param rowspan: number of rows across which the graph spans
      :param colspan: number of columns across which the graph spans
      :return:


   .. method:: __create_graph(self, idGraph)



   .. method:: __check_graphs(self)



   .. method:: on_click(self, plotDataItem, clicked_points)



   .. method:: update_graphs(self, singleUpdate=True)


      This method is used to update the graph. This is fast but NOT safe (especially when working with threads).
      To limit the risks, please use self.signal_must_update.emit() instead.

      :param singleUpdate: if set to False, the graph will periodically refres each self.refreshtime


   .. method:: fast_update(self)


      Use this method to update the graph in a fast way. NOT THREAD SAFE.


   .. method:: exportGraphs(self)


      Export the graphs


   .. method:: export_txt(self, filename_txt)



   .. method:: export_svg(self, filename)



   .. method:: export_pdf(filename_svg, filename_pdf)
      :staticmethod:



   .. method:: export_png(filename_svg, filename_png)
      :staticmethod:



   .. method:: export_tikz(self, foldername_tikz)



   .. method:: link_axes(self)



   .. method:: get_graph(self, idGraph)


      Get corresponding :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.GraphVisual.GraphVisual` of the graph idGraph


   .. method:: keyPressEvent(self, event)


      What happens if a key is pressed.
      R: reset the axes to their default value


   .. method:: delete_graph(self, idGraph)


      Delete the graph idGraph


   .. method:: delete(self)



   .. method:: get_all_graphsVisual(self)


      Return a dictionary {idGraph: :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.GraphVisual.GraphVisual`}.


   .. method:: get_layout_buttons(self)


      Get the QGraphicsLayout where it's possible to add buttons, etc.


   .. method:: set_actionOnClick(self, theActionOnClick)


      Action to perform when the graph is clicked

      :param theActionOnClick: :class:`on_graph_click_interface`
      :return:


   .. method:: set_title(self, idGraph, titleName, **kwargs)


      Set title of the graph

      :param idGraph: id of the graph
      :param titleName: title to set


   .. method:: set_article_template(self, graph_size_x=8.8, graph_size_y=4.4, legendPosition='NW')


      Method to set the graphs to article quality graph.

      :param graph_size_x: width of the graph in cm
      :param graph_size_y: height of the graph in cm
      :param legendPosition: position of the legend (NE, SE, SW, NW)
      :return:



