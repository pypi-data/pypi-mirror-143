``on_click_showinfo``
================================================================================================

.. py:module:: optimeed.visualize.gui.widgets.graphsVisualWidget.examplesActionOnClick.on_click_showinfo


Module Contents
---------------

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




.. py:class:: Repr_brut_attributes(is_light=True, convertToHtml=True, recursion_level=5)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: Repr_lines(attribute_lines)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: Repr_opengl(DeviceDrawer)

   .. method:: get_widget(self, theNewDevice)




.. py:class:: Repr_image(get_base_64_from_device)

   .. method:: get_widget(self, theNewDevice)




