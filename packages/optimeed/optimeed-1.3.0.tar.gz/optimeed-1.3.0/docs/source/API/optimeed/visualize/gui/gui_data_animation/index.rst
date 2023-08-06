``gui_data_animation``
================================================

.. py:module:: optimeed.visualize.gui.gui_data_animation


Module Contents
---------------

.. py:class:: DataAnimationTrace(elements_list, theTrace)

   Contains all the element to animate for a trace

   .. py:class:: element_animation(elements)

      .. method:: get(self)




   .. method:: get_element_animations(self, itemNumber, index_in_show)


      Get the element to show
      :param itemNumber: item number (0 if only one think to draw)
      :param index_in_show: index in the list
      :return: The element to draw


   .. method:: show_all(self)



   .. method:: delete_all(self)



   .. method:: get_indices_to_show(self)



   .. method:: add_element(self, indexPoint)



   .. method:: add_index_to_show(self, index)



   .. method:: _remove_index_from_show(self, index)



   .. method:: set_curr_brush(self, index_in_show)



   .. method:: set_idle_brush(self, index_in_show)



   .. method:: get_number_of_elements(self)



   .. method:: map_index(self, index_in_show)



   .. method:: get_base_pen(self)




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



