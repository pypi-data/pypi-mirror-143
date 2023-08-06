``tikzTranslator``
===================================

.. py:module:: optimeed.core.tikzTranslator


Module Contents
---------------

.. data:: templates_tikz
   

   

.. function:: format_escape_char(theStr)


.. function:: convert_linestyle(linestyle)


.. function:: convert_color(color)


.. function:: find_all_colors(theGraphs)


.. function:: convert_marker(marker)


.. function:: do_preamble()


.. function:: do_generate_figure()


.. function:: do_specific_axis_options(theGraph: Graph)

   Get graph-specific axis options


.. function:: do_specific_trace_options(theTrace: Data, theColor)

   Get latex trace options from Data


.. function:: export_to_tikz_groupGraphs(theGraphs: Graphs, foldername, additionalPreamble=lambda: '', additionalAxisOptions=lambda graphId: '', additionalTraceOptions=lambda graphId, traceId: '', debug=False)

   Export the graphs as group

   :param theGraphs: Graphs to save
   :param foldername: Foldername to save
   :param additionalPreamble: method that returns string for custom tikz options
   :param additionalAxisOptions: method that returns string for custom tikz options
   :param additionalTraceOptions: method that returns string for custom tikz options
   :return:


