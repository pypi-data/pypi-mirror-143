**examplesActionOnClick**
==============================================================================

.. py:module:: optimeed.visualize.gui.widgets.graphsVisualWidget.examplesActionOnClick


.. toctree::
   :titlesonly:
   :maxdepth: 1

   on_click_anim/index.rst
   on_click_change_symbol/index.rst
   on_click_copy_something/index.rst
   on_click_delete/index.rst
   on_click_draw_device/index.rst
   on_click_export_collection/index.rst
   on_click_extract_pareto/index.rst
   on_click_measure/index.rst
   on_click_remove_trace/index.rst
   on_click_showinfo/index.rst


Package Contents
----------------

.. py:class:: on_graph_click_delete(theDataLink)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On Click: Delete the points from the graph, and save the modified collection

   .. method:: apply(self)



   .. method:: reset(self)



   .. method:: graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points)



   .. method:: get_name(self)




.. py:class:: on_graph_click_export(theDataLink)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On click: export the selected points

   .. method:: graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points)



   .. method:: reset_graph(self)



   .. method:: get_name(self)




.. py:class:: on_click_extract_pareto(theDataLink, max_x=False, max_y=False)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On click: extract the pareto from the cloud of points

   .. method:: graph_clicked(self, the_graph_visual, index_graph, index_trace, _)



   .. method:: get_name(self)




.. py:class:: on_graph_click_showInfo(theLinkDataGraph, visuals=None)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On click: show informations about the points (loop through attributes)

   .. py:class:: DataInformationVisuals

      .. method:: delete_visual(self, theVisual)



      .. method:: add_visual(self, theVisual, theTrace, indexPoint)



      .. method:: get_new_index(self)



      .. method:: curr_index(self)




   .. method:: graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points)


      Action to perform when a point in the graph has been clicked:
      Creates new window displaying the device and its informations


   .. method:: get_name(self)




.. py:class:: Repr_opengl(DeviceDrawer)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: Repr_lines(attribute_lines)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: Repr_brut_attributes(is_light=True, convertToHtml=True, recursion_level=5)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: Repr_image(get_base_64_from_device)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: on_graph_click_remove_trace(theDataLink)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   .. method:: graph_clicked(self, theGraphVisual, index_graph, index_trace, _)



   .. method:: get_name(self)




.. py:class:: on_click_copy_something(theDataLink, functionStrFromDevice)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On Click: copy something

   .. method:: graph_clicked(self, the_graph_visual, index_graph, index_trace, indices_points)



   .. method:: get_name(self)




.. py:class:: on_click_change_symbol(theLinkDataGraph)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On Click: Change the symbol of the point that is clicked

   .. method:: graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points)



   .. method:: get_name(self)




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




.. py:class:: DataAnimationVisuals(id=0, window_title='Animation')

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   Spawns a gui that includes button to create animations nicely when paired with :class:`~optimeed.visualize.gui.widgets.widget_graphs_visual`

   .. attribute:: SlIDER_MAXIMUM_VALUE
      :annotation: = 500

      

   .. attribute:: SLIDER_MINIMUM_VALUE
      :annotation: = 1

      

   .. method:: add_trace(self, trace_id, element_list, theTrace)


      Add a trace to the animation.

      :param trace_id: id of the trace
      :param element_list: List of elements to save: [[OpenGL_item1, text_item1], [OpenGL_item2, text_item2], ... [OpenGL_itemN, text_itemN]]
      :param theTrace: :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.TraceVisual.TraceVisual`
      :return:


   .. method:: get_interesting_elements(element_list)
      :staticmethod:


      Function called upon new trace creation. From a list, takes the interesting elements for animation
      :param element_list:
      :return: new_element_list


   .. method:: add_elementToTrace(self, trace_id, indexPoint)



   .. method:: delete_point(self, trace_id, thePoint)



   .. method:: reset_all(self)



   .. method:: delete_all(self)



   .. method:: pause_play(self)



   .. method:: show_all(self)



   .. method:: next_frame(self)



   .. method:: slider_handler(self)



   .. method:: frame_selector(self)



   .. method:: set_refreshTime(self)



   .. method:: is_empty(self)



   .. method:: run(self)



   .. method:: closeEvent(self, _)



   .. method:: contains_trace(self, trace_id)



   .. method:: export_picture(self)



   .. method:: export_widget(self, painter)
      :abstractmethod:


      Render scene with a painter

      :param painter: PyQt painter


   .. method:: update_widget_w_animation(self, key, index, the_data_animation)
      :abstractmethod:


      What to do when a new element has to be animated. Example: self.theOpenGLWidget.set_deviceToDraw(the_data_animation.get_element_animations(0, index))

      :param key: key of the trace that has to be animated
      :param index: index that has to be animated
      :param the_data_animation: :class:`~DataAnimationTrace` that has to be animated


   .. method:: delete_key_widgets(self, key)
      :abstractmethod:


      What to do when a key has to be deleted

      :param key: key of the trace that has to be deleted



.. py:class:: widget_text(theText, is_light=False, convertToHtml=False)

   Bases: :class:`PyQt5.QtWidgets.QLabel`

   Widget able to display a text

   .. method:: set_text(self, theText, convertToHtml=False)


      Set the text to display



.. py:class:: widget_line_drawer(minWinHeight=300, minWinWidth=300, is_light=True)

   Bases: :class:`PyQt5.QtWidgets.QWidget`

   Widget allowing to display several lines easily

   .. attribute:: signal_must_update
      

      

   .. method:: on_update_signal(self, listOfLines)



   .. method:: delete_lines(self, key_id)


      Dele the lines
      :param key_id: id to delete
      :return:


   .. method:: set_lines(self, listOfLines, key_id=0, pen=None)


      Set the lines to display
      :param listOfLines: list of [x1, y1, x2, y2] corresponding to lines
      :param key_id: id of the trace
      :param pen: pen used to draw the lines
      :return:


   .. method:: paintEvent(self, event, painter=None)



   .. method:: get_extrema_lines(self)




.. py:class:: DataAnimationOpenGL(theOpenGLWidget, theId=0, window_title='Animation')

   Bases: :class:`optimeed.visualize.gui.gui_data_animation.DataAnimationVisuals`

   Implements :class:`~DataAnimationVisuals` to show opengl drawing

   .. method:: update_widget_w_animation(self, key, index, the_data_animation)



   .. method:: export_widget(self, painter)



   .. method:: delete_key_widgets(self, key)




.. py:class:: DataAnimationOpenGLwText(*args, is_light=True, **kwargs)

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.examplesActionOnClick.on_click_anim.DataAnimationOpenGL`

   Implements :class:`~DataAnimationVisuals` to show opengl drawing and text

   .. method:: update_widget_w_animation(self, key, index, the_data_animation)



   .. method:: get_interesting_elements(self, devices_list)




.. py:class:: DataAnimationLines(get_lines_method, is_light=True, theId=0, window_title='Animation')

   Bases: :class:`optimeed.visualize.gui.gui_data_animation.DataAnimationVisuals`

   Implements :class:`~DataAnimationVisuals` to show drawing made out of lines (:class:`~optimeed.visualize.gui.widgets.widget_line_drawer`)

   .. method:: export_widget(self, painter)



   .. method:: delete_key_widgets(self, key)



   .. method:: update_widget_w_animation(self, key, index, the_data_animation)



   .. method:: get_interesting_elements(self, devices_list)




.. py:class:: DataAnimationVisualswText(*args, **kwargs)

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.examplesActionOnClick.on_click_anim.DataAnimationLines`

   Same as :class:`~DataAnimationLines` but also with text

   .. method:: update_widget_w_animation(self, key, index, the_data_animation)




.. py:class:: on_graph_click_showAnim(theLinkDataGraph, theAnimation)

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On click: add or remove an element to animate

   .. method:: graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points)



   .. method:: get_name(self)




.. py:class:: on_click_measure

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On Click: Measure distance. Click on two points to perform that action

   .. method:: graph_clicked(self, the_graph_visual, index_graph, index_trace, indices_points)



   .. method:: reset_distance(self)



   .. method:: display_distance(self)



   .. method:: get_name(self)




