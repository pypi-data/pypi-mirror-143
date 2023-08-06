``graphs``
===========================

.. py:module:: optimeed.core.graphs


Module Contents
---------------

.. py:class:: Data(x: list, y: list, x_label='', y_label='', legend='', is_scattered=False, transfo_x=lambda selfData, x: x, transfo_y=lambda selfData, y: y, xlim=None, ylim=None, permutations=None, sort_output=False, color=None, symbol='o', symbolsize=8, fillsymbol=True, outlinesymbol=1.8, linestyle='-', width=2)

   This class is used  to store informations necessary to plot a 2D graph. It has to be combined with a gui to be useful (ex. pyqtgraph)

   .. method:: set_data(self, x: list, y: list)


      Overwrites current datapoints with new set


   .. method:: get_x(self)


      Get x coordinates of datapoints


   .. method:: get_symbolsize(self)


      Get size of the symbols


   .. method:: symbol_isfilled(self)


      Check if symbols has to be filled or not


   .. method:: get_symbolOutline(self)


      Get color factor of outline of symbols


   .. method:: get_length_data(self)


      Get number of points


   .. method:: get_xlim(self)


      Get x limits of viewbox


   .. method:: get_ylim(self)


      Get y limits of viewbox


   .. method:: get_y(self)


      Get y coordinates of datapoints


   .. method:: get_color(self)


      Get color of the line


   .. method:: get_width(self)


      Get width of the line


   .. method:: get_number_of_points(self)


      Get number of points


   .. method:: get_plot_data(self)


      Call this method to get the x and y coordinates of the points that have to be displayed.
      => After transformation, and after permutations.

      :return: x (list), y (list)


   .. method:: get_permutations(self, x=None)


      Return the transformation 'permutation':
      xplot[i] = xdata[permutation[i]]


   .. method:: get_invert_permutations(self)


      Return the inverse of permutations:
      xdata[i] = xplot[revert[i]]


   .. method:: get_dataIndex_from_graphIndex(self, index_graph_point)


      From an index given in graph, recovers the index of the data.

      :param index_graph_point: Index in the graph
      :return: index of the data


   .. method:: get_dataIndices_from_graphIndices(self, index_graph_point_list)


      Same as get_dataIndex_from_graphIndex but with a list in entry.
      Can (?) improve performances for huge dataset.

      :param index_graph_point_list: List of Index in the graph
      :return: List of index of the data


   .. method:: get_graphIndex_from_dataIndex(self, index_data)


      From an index given in the data, recovers the index of the graph.

      :param index_data: Index in the data
      :return: index of the graph


   .. method:: get_graphIndices_from_dataIndices(self, index_data_list)


      Same as get_graphIndex_from_dataIndex but with a list in entry.
      Can (?) improve performances for huge dataset.

      :param index_data_list: List of Index in the data
      :return: List of index of the graph


   .. method:: set_permutations(self, permutations)


      Set permutations between datapoints of the trace

      :param permutations: list of indices to plot (example: [0, 2, 1] means that the first point will be plotted, then the third, then the second one)


   .. method:: get_x_label(self)


      Get x label of the trace 


   .. method:: get_y_label(self)


      Get y label of the trace 


   .. method:: get_legend(self)


      Get name of the trace 


   .. method:: get_symbol(self)


      Get symbol 


   .. method:: add_point(self, x, y)


      Add point(s) to trace (inputs can be list or numeral)


   .. method:: delete_point(self, index_point)


      Delete a point from the datapoints


   .. method:: is_scattered(self)


      Delete a point from the datapoints


   .. method:: set_indices_points_to_plot(self, indices)


      Set indices points to plot


   .. method:: get_indices_points_to_plot(self)


      Get indices points to plot


   .. method:: get_linestyle(self)


      Get linestyle


   .. method:: __str__(self)



   .. method:: export_str(self)


      Method to save the points constituting the trace


   .. method:: set_color(self, theColor)




.. py:class:: Graph

   Simple graph container that contains several traces

   .. method:: add_trace(self, data)


      Add a trace to the graph

      :param data: :class:`~Data`
      :return: id of the created trace


   .. method:: remove_trace(self, idTrace)


      Delete a trace from the graph

      :param idTrace: id of the trace to delete


   .. method:: get_trace(self, idTrace)


      Get data object of idTrace

      :param idTrace: id of the trace to get
      :return: :class:`~Data`


   .. method:: get_all_traces(self)


      Get all the traces id of the graph


   .. method:: export_str(self)




.. py:class:: Graphs

   Contains several :class:`Graph`

   .. method:: updateChildren(self)



   .. method:: add_trace_firstGraph(self, data, updateChildren=True)


      Same as add_trace, but only if graphs has only one id
      :param data:
      :param updateChildren:
      :return:


   .. method:: add_trace(self, idGraph, data, updateChildren=True)


      Add a trace to the graph

      :param idGraph: id of the graph
      :param data: :class:`~Data`
      :param updateChildren: Automatically calls callback functions
      :return: id of the created trace


   .. method:: remove_trace(self, idGraph, idTrace, updateChildren=True)


      Remove the trace from the graph

      :param idGraph: id of the graph
      :param idTrace: id of the trace to remove
      :param updateChildren: Automatically calls callback functions


   .. method:: get_first_graph(self)


      Get id of the first graph

      :return: id of the first graph


   .. method:: get_graph(self, idGraph)


      Get graph object at idgraph

      :param idGraph: id of the graph to get
      :return: :class:`~Graph`


   .. method:: get_all_graphs_ids(self)


      Get all ids of the graphs

      :return: list of id graphs


   .. method:: get_all_graphs(self)


      Get all graphs. Return dict {id: :class:`~Graph`}


   .. method:: add_graph(self, updateChildren=True)


      Add a new graph

      :return: id of the created graph


   .. method:: remove_graph(self, idGraph)


      Delete a graph

      :param idGraph: id of the graph to delete


   .. method:: add_update_method(self, childObject)


      Add a callback each time a graph is modified.

      :param childObject: method without arguments


   .. method:: export_str(self)


      Export all the graphs in text

      :return: str


   .. method:: merge(self, otherGraphs)



   .. method:: reset(self)



   .. method:: is_empty(self)




