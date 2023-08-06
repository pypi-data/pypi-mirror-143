``on_click_anim``
============================================================================================

.. py:module:: optimeed.visualize.gui.widgets.graphsVisualWidget.examplesActionOnClick.on_click_anim


Module Contents
---------------

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




