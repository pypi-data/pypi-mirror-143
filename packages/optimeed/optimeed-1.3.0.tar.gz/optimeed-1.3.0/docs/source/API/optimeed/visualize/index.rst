**visualize**
=========================

.. py:module:: optimeed.visualize


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 8

   gui/index.rst


.. toctree::
   :titlesonly:
   :maxdepth: 1

   displayOptimization/index.rst
   fastPlot/index.rst


Package Contents
----------------

.. py:class:: gui_mainWindow(QtWidgetList, isLight=True, actionOnWindowClosed=None, neverCloseWindow=False, title_window='Awesome Visualisation Tool', size=None)

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   Main class that spawns a Qt window. Use :meth:`~gui_mainWindow.run` to display it.

   .. method:: set_actionOnClose(self, actionOnWindowClosed)



   .. method:: closeEvent(self, event)



   .. method:: run(self, hold=False)


      Display the window


   .. method:: hold()
      :staticmethod:



   .. method:: keyPressEvent(self, event)




.. data:: app
   

   

.. function:: start_qt_mainloop()

   Starts qt mainloop, which is necessary for qt to handle events


.. function:: stop_qt_mainloop()

   Stops qt mainloop and resumes to program


.. py:class:: gui_collection_exporter

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   Simple gui that allows to export data

   .. attribute:: signal_has_exported
      

      

   .. attribute:: signal_has_reset
      

      

   .. method:: exportCollection(self)


      Export the collection


   .. method:: reset(self)



   .. method:: add_data_to_collection(self, data)


      Add data to the collection to export

      :param data: Whichever type you like


   .. method:: set_info(self, info)



   .. method:: set_collection(self, theCollection)




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



.. py:class:: GuiDataSelector(list_ListDataStruct_in, actionOnUpdate: Action_on_selector_update)

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   .. attribute:: theActionOnUpdate
      

      Generate GUI


   .. method:: apply_filters(self, _)



   .. method:: run(self)




.. py:class:: Action_on_selector_update

   .. method:: selector_updated(self, selection_name, the_collection, indices_data)
      :abstractmethod:


      Action to perform once the data have been selected
      :param selection_name: name of the selection (deprecated ?)
      :param the_collection: the collection
      :param indices_data: indices of the data
      :return:



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




.. py:class:: widget_menuButton(theParentButton)

   Bases: :class:`PyQt5.QtWidgets.QMenu`

   Same as QMenu, but integrates it behind a button more easily.

   .. method:: showEvent(self, QShowEvent)




.. py:class:: widget_openGL(parent=None)

   Bases: :class:`PyQt5.QtWidgets.QOpenGLWidget`

   Interface that provides opengl capabilities.
   Ensures zoom, light, rotation, etc.

   .. method:: sizeHint(self)



   .. method:: minimumSizeHint(self)



   .. method:: set_deviceDrawer(self, theDeviceDrawer)


      Set a drawer :class:`optimeed.visualize.gui.widgets.openGLWidget.DeviceDrawerInterface.DeviceDrawerInterface`


   .. method:: set_deviceToDraw(self, theDeviceToDraw)


      Set the device to draw :class:`optimeed.InterfaceDevice.InterfaceDevice`


   .. method:: _get_specialButtonsMapping()
      :staticmethod:



   .. method:: initializeGL(self)



   .. method:: paintGL(self)



   .. method:: resizeGL(self, w, h)



   .. method:: mousePressEvent(self, event)



   .. method:: mouseMoveEvent(self, event)



   .. method:: keyPressEvent(self, event)



   .. method:: wheelEvent(self, QWheelEvent)




.. py:class:: widget_text(theText, is_light=False, convertToHtml=False)

   Bases: :class:`PyQt5.QtWidgets.QLabel`

   Widget able to display a text

   .. method:: set_text(self, theText, convertToHtml=False)


      Set the text to display



.. py:class:: Widget_image(image_b64)

   Bases: :class:`PyQt5.QtWidgets.QLabel`

   .. method:: eventFilter(self, source, event)



   .. method:: set_image(self, image_b64)


      Set new image to widget 



.. py:class:: guiPyqtgraph(graphsVisual, **kwargs)

   Create a gui for pyqtgraph with trace selection options, export and action on clic choices

   .. method:: refreshTraceList(self)


      Refresh all the traces



.. py:class:: DeviceDrawerInterface

   .. method:: draw(self, theDevice)
      :abstractmethod:



   .. method:: get_init_camera(self, theDevice)
      :abstractmethod:



   .. method:: keyboard_push_action(self, theKey)



   .. method:: get_colour_scalebar(self)



   .. method:: get_colour_background(self)



   .. method:: get_opengl_options(self)




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




.. py:class:: on_click_measure

   Bases: :class:`optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`

   On Click: Measure distance. Click on two points to perform that action

   .. method:: graph_clicked(self, the_graph_visual, index_graph, index_trace, indices_points)



   .. method:: reset_distance(self)



   .. method:: display_distance(self)



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




.. py:class:: On_select_new_trace(theLinkDataGraphs)

   Bases: :class:`optimeed.visualize.gui.gui_data_selector.Action_on_selector_update`

   .. method:: selector_updated(self, selection_name, the_collection, indices_data)


      Action to perform once the data have been selected
      :param selection_name: name of the selection (deprecated ?)
      :param the_collection: the collection
      :param indices_data: indices of the data
      :return:



.. py:class:: LinkDataGraph

   .. py:class:: _collection_linker

      .. method:: add_link(self, idSlave, idMaster)



      .. method:: get_collection_master(self, idToGet)



      .. method:: is_slave(self, idToCheck)



      .. method:: set_same_master(self, idExistingSlave, idOtherSlave)


         :param idExistingSlave: id collection of the existing slave
         :param idOtherSlave: id collection of the new slave that has to be linked to an existing master



   .. method:: add_collection(self, theCollection, kwargs=None)



   .. method:: add_graph(self, howToPlotGraph)



   .. method:: createGraphs(self)



   .. method:: get_x_y_to_plot(theCollection, howToPlotGraph)
      :staticmethod:



   .. method:: get_howToPlotGraph(self, idGraph)



   .. method:: get_collectionInfo(self, idCollectionInfo)



   .. method:: create_trace(self, collectionInfo, howToPlotGraph, idGraph)



   .. method:: get_all_id_graphs(self)



   .. method:: get_all_traces_id_graph(self, idGraph)



   .. method:: update_graphs(self)



   .. method:: is_slave(self, idGraph, idTrace)



   .. method:: get_idCollection_from_graph(self, idGraph, idTrace, getMaster=True)


      From indices in the graph, get index of corresponding collection


   .. method:: get_collection_from_graph(self, idGraph, idTrace, getMaster=True)


      From indices in the graph, get corresponding collection


   .. method:: get_dataObject_from_graph(self, idGraph, idTrace, idPoint)



   .. method:: get_dataObjects_from_graph(self, idGraph, idTrace, idPoint_list)



   .. method:: remove_element_from_graph(self, idGraph, idTrace, idPoint, deleteFromMaster=False)


      Remove element from the graph, or the master collection


   .. method:: remove_elements_from_trace(self, idGraph, idTrace, idPoints, deleteFromMaster=False)


      Performances optimisation when compared to :meth:`LinkDataGraph.remove_element_from_graph`


   .. method:: link_collection_to_graph_collection(self, id_collection_graph, id_collection_master)


      Link data
      :param id_collection_graph:
      :param id_collection_master:
      :return:


   .. method:: remove_trace(self, idGraph, idTrace)



   .. method:: get_graph_and_trace_from_collection(self, idCollection)


      Reverse search: from a collection, get the associated graph


   .. method:: get_mappingData_graph(self, idGraph)



   .. method:: get_mappingData_trace(self, idGraph, idTrace)



   .. method:: get_idcollection_from_collection(self, theCollection)



   .. method:: get_idPoints_from_indices_in_collection(self, idGraph, idTrace, indices_in_collection)




.. py:class:: HowToPlotGraph(attribute_x, attribute_y, kwargs_graph=None, excluded=None, exclusively=None, check_if_plot_elem=None)

   .. method:: exclude_col(self, id_col)


      Add id_col to exclude from the graph


   .. method:: exclusive_col(self, id_col)


      Set id_col to have exclusivity on the graph


   .. method:: __str__(self)




.. py:class:: Option_class

   Bases: :class:`optimeed.core.options.Option_class_interface`

   .. method:: __str__(self)



   .. method:: get_optionValue(self, optionId)



   .. method:: set_optionValue(self, optionId, value)



   .. method:: get_all_options(self)



   .. method:: set_all_options(self, options)



   .. method:: add_option(self, idOption, name, value)




.. py:class:: gui_mainWindow(QtWidgetList, isLight=True, actionOnWindowClosed=None, neverCloseWindow=False, title_window='Awesome Visualisation Tool', size=None)

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   Main class that spawns a Qt window. Use :meth:`~gui_mainWindow.run` to display it.

   .. method:: set_actionOnClose(self, actionOnWindowClosed)



   .. method:: closeEvent(self, event)



   .. method:: run(self, hold=False)


      Display the window


   .. method:: hold()
      :staticmethod:



   .. method:: keyPressEvent(self, event)




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




.. py:class:: guiPyqtgraph(graphsVisual, **kwargs)

   Create a gui for pyqtgraph with trace selection options, export and action on clic choices

   .. method:: refreshTraceList(self)


      Refresh all the traces



.. function:: check_if_must_plot(elem)


.. py:class:: OptimizationDisplayer(thePipeOpti, listOfObjectives, theOptimizer, additionalWidgets=None)

   Bases: :class:`optimeed.core.Option_class`

   Class used to display optimization process in real time

   .. attribute:: signal_optimization_over
      

      

   .. attribute:: SHOW_CONSTRAINTS
      :annotation: = 0

      

   .. method:: set_actionsOnClick(self, theList)


      Set actions to perform on click, list of :class:`~optimeed.visualize.gui.widgets.widget_graphs_visual.on_graph_click_interface`


   .. method:: generate_optimizationGraphs(self)


      Generates the optimization graphs.
      :return: :class:`~optimeed.core.graphs.Graphs`, :class:`~optimeed.core.linkDataGraph.LinkDataGraph`, :class:'~optimeed.visulaize.gui.widgets.widget_graphs_visual.widget_graphs_visual


   .. method:: __change_appearance_violate_constraints(self)



   .. method:: __refresh(self)



   .. method:: start_autorefresh(self, timer_autosave)



   .. method:: stop_autorefresh(self)



   .. method:: __set_graphs_disposition(self)


      Set nicely the graphs disposition


   .. method:: launch_optimization(self, refresh_time=0.1)


      Perform the optimization and spawn the convergence graphs afterwards.


   .. method:: __callback_optimization(self)



   .. method:: close_windows(self)



   .. method:: display_graphs(theGraphs)
      :staticmethod:



   .. method:: create_main_window(self)


      From the widgets and the actions on click, spawn a window and put a gui around widgetsGraphsVisual.



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



.. py:class:: gui_mainWindow(QtWidgetList, isLight=True, actionOnWindowClosed=None, neverCloseWindow=False, title_window='Awesome Visualisation Tool', size=None)

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   Main class that spawns a Qt window. Use :meth:`~gui_mainWindow.run` to display it.

   .. method:: set_actionOnClose(self, actionOnWindowClosed)



   .. method:: closeEvent(self, event)



   .. method:: run(self, hold=False)


      Display the window


   .. method:: hold()
      :staticmethod:



   .. method:: keyPressEvent(self, event)




.. function:: start_qt_mainloop()

   Starts qt mainloop, which is necessary for qt to handle events


.. function:: stop_qt_mainloop()

   Stops qt mainloop and resumes to program


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




.. py:class:: guiPyqtgraph(graphsVisual, **kwargs)

   Create a gui for pyqtgraph with trace selection options, export and action on clic choices

   .. method:: refreshTraceList(self)


      Refresh all the traces



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


