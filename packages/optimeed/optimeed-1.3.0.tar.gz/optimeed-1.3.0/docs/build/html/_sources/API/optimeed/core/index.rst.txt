**core**
====================

.. py:module:: optimeed.core


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 8

   ansi2html/index.rst


.. toctree::
   :titlesonly:
   :maxdepth: 1

   additional_tools/index.rst
   collection/index.rst
   color_palette/index.rst
   commonImport/index.rst
   graphs/index.rst
   interfaceDevice/index.rst
   linkDataGraph/index.rst
   myjson/index.rst
   options/index.rst
   tikzTranslator/index.rst
   tools/index.rst


Package Contents
----------------

.. function:: getPath_workspace()


.. function:: obj_to_json(theObj)

   Extract the json dictionary from the object. The data saved are automatically detected, using typehints.
   ex: x: int=5 will be saved, x=5 won't.
   Inheritance of annotation is managed by this function


.. function:: json_to_obj(json_dict)

   Convenience class to create object from dictionary. Only works if CLASS_TAG is valid

   :param json_dict: dictionary loaded from a json file.
   :raise TypeError: if class can not be found
   :raise KeyError: if CLASS_TAG not present in dictionary


.. function:: json_to_obj_safe(json_dict, cls)

   Safe class to create object from dictionary.

   :param json_dict: dictionary loaded from a json file
   :param cls: class object to instantiate with dictionary


.. function:: encode_str_json(theStr)


.. function:: decode_str_json(theStr)


.. function:: get_json_module_tree(theObj)

   Return dict containing {CLASS_TAG: "class_name", MODULE_TAG: "module_name", "attribute1":{"class_name": "module_name", ...}}


.. data:: MODULE_TAG
   :annotation: = __module__

   

.. data:: CLASS_TAG
   :annotation: = __class__

   

.. function:: indentParagraph(text_in, indent_level=1)


.. function:: rgetattr(obj, attr)

   Recursively get an attribute from object. Extends getattr method

   :param obj: object
   :param attr: attribute to get
   :return:


.. function:: applyEquation(objectIn, s)

   Apply literal expression based on an object

   :param objectIn: Object
   :param s: literal expression. Float variables taken from the object are written between {}, int between []. Example: s="{x}+{y}*2" if x and y are attributes of objectIn.
   :return: value (float)


.. function:: printIfShown(theStr, show_type=SHOW_DEBUG, isToPrint=True, appendTypeName=True)


.. data:: SHOW_WARNING
   :annotation: = 0

   

.. data:: SHOW_DEBUG
   :annotation: = 3

   

.. py:class:: DataStruct_Interface

   .. method:: save(self, filename)
      :abstractmethod:


      Save the datastructure to filename


   .. method:: load(filename, **kwargs)
      :staticmethod:
      :abstractmethod:


      Load the datastructure from filename


   .. method:: get_info(self)


      Get simple string describing the datastructure


   .. method:: set_info(self, info)


      Set simple string describing the datastructure


   .. method:: get_extension()
      :staticmethod:


      File extension used for datastructure


   .. method:: __str__(self)




.. py:class:: AutosaveStruct(dataStruct, filename='', change_filename_if_exists=True)

   Structure that provides automated save of DataStructures

   .. method:: __str__(self)



   .. method:: get_filename(self)


      Get set filename


   .. method:: set_filename(self, filename, change_filename_if_exists)


      :param filename: Filename to set
      :param change_filename_if_exists: If already exists, create a new filename


   .. method:: stop_autosave(self)


      Stop autosave


   .. method:: start_autosave(self, timer_autosave)


      Start autosave


   .. method:: save(self, safe_save=True)


      Save


   .. method:: get_datastruct(self)


      Return :class:'~DataStruct_Interface'


   .. method:: __getstate__(self)



   .. method:: __setstate__(self, state)




.. py:class:: ListDataStruct(compress_save=False)

   Bases: :class:`optimeed.core.collection.DataStruct_Interface`

   .. attribute:: _INFO_STR
      :annotation: = info

      

   .. attribute:: _DATA_STR
      :annotation: = data

      

   .. attribute:: _COMPRESS_SAVE_STR
      :annotation: = module_tree

      

   .. method:: save(self, filename)


      Save data using json format. The data to be saved are automatically detected, see :meth:`~optimeed.core.myjson.obj_to_json` 


   .. method:: _format_str_save(self)


      Save data using json format. The data to be saved are automatically detected, see :meth:`~optimeed.core.myjson.obj_to_json` 


   .. method:: load(filename, theClass=None)
      :staticmethod:


      Load the file filename.

      :param filename: file to load
      :param theClass: optional. Can be used to fix unpickling errors.
      :return: self-like object


   .. method:: _jsondata_to_obj(item, theClass=None)
      :staticmethod:



   .. method:: add_data(self, data_in)


      Add a data to the list


   .. method:: get_data(self)


      Get full list of datas


   .. method:: set_data(self, theData)


      Set full list of datas


   .. method:: set_data_at_index(self, data_in, index)


      Replace data at specific index


   .. method:: set_attribute_data(self, the_attribute, the_value)


      Set attribute to all data


   .. method:: set_attribute_equation(self, attribute_name, equation_str)


      Advanced method to set the value of attribute_name from equation_str

      :param attribute_name: string (name of the attribute to set)
      :param equation_str: formatted equation, check :meth:`~optimeed.core.CommonFunctions_Library.applyEquation`
      :return:


   .. method:: get_list_attributes(self, attributeName)


      Get the value of attributeName of all the data in the Collection

      :param attributeName: string (name of the attribute to get)
      :return: list


   .. method:: delete_points_at_indices(self, indices)


      Delete several elements from the Collection

      :param indices: list of indices to delete


   .. method:: export_xls(self, excelFilename, excelsheet='Sheet1', mode='w')


      Export the collection to excel. It only exports the direct attributes.

      :param excelFilename: filename of the excel
      :param excelsheet: name of the sheet
      :param mode: 'w' to erase existing file, 'a' to append sheetname to existing file


   .. method:: merge(self, collection)


      Merge a collection with the current collection

      :param collection: :class:`~optimeed.core.Collection.Collection` to merge



.. function:: default_palette(N)


.. function:: blackOnly(N)


.. function:: dark2(N)


.. py:class:: text_format

   .. attribute:: PURPLE
      :annotation: = [95m

      

   .. attribute:: CYAN
      :annotation: = [96m

      

   .. attribute:: DARKCYAN
      :annotation: = [36m

      

   .. attribute:: BLUE
      :annotation: = [94m

      

   .. attribute:: GREEN
      :annotation: = [92m

      

   .. attribute:: YELLOW
      :annotation: = [93m

      

   .. attribute:: WHITE
      :annotation: = [30m

      

   .. attribute:: RED
      :annotation: = [91m

      

   .. attribute:: BOLD
      :annotation: = [1m

      

   .. attribute:: UNDERLINE
      :annotation: = [4m

      

   .. attribute:: END
      :annotation: = [0m

      


.. function:: software_version()


.. function:: find_and_replace(begin_char, end_char, theStr, replace_function)


.. function:: create_unique_dirname(dirname)


.. function:: applyEquation(objectIn, s)

   Apply literal expression based on an object

   :param objectIn: Object
   :param s: literal expression. Float variables taken from the object are written between {}, int between []. Example: s="{x}+{y}*2" if x and y are attributes of objectIn.
   :return: value (float)


.. function:: arithmeticEval(s)


.. function:: isNonePrintMessage(theObject, theMessage, show_type=SHOW_INFO)


.. function:: getPath_workspace()


.. function:: getLineInfo(lvl=1)


.. function:: printIfShown(theStr, show_type=SHOW_DEBUG, isToPrint=True, appendTypeName=True)


.. function:: universalPath(thePath)


.. function:: add_suffix_to_path(thePath, suffix)


.. function:: get_object_attrs(obj)


.. function:: rsetattr(obj, attr, val)


.. function:: rgetattr(obj, attr)

   Recursively get an attribute from object. Extends getattr method

   :param obj: object
   :param attr: attribute to get
   :return:


.. function:: indentParagraph(text_in, indent_level=1)


.. function:: truncate(theStr, truncsize)


.. function:: str_all_attr(theObject, max_recursion_level)


.. function:: get_2D_pareto(xList, yList, max_X=True, max_Y=True)


.. function:: get_ND_pareto(objectives_list, are_maxobjectives_list=None)

   Return the N-D pareto front

   :param objectives_list: list of list of objectives: example [[0,1], [1,1], [2,2]]
   :param are_maxobjectives_list: for each objective, tells if they are to be maximized or not: example [True, False]. Default: False
   :return: extracted_pareto, indices: list of [x, y, ...] points forming the pareto front, and list of the indices of these points from the base list.


.. function:: delete_indices_from_list(indices, theList)

   Delete elements from list at indices
   :param indices: list
   :param theList: list


.. data:: SHOW_WARNING
   :annotation: = 0

   

.. data:: SHOW_INFO
   :annotation: = 1

   

.. data:: SHOW_ERROR
   :annotation: = 2

   

.. data:: SHOW_DEBUG
   :annotation: = 3

   

.. data:: SHOW_CURRENT
   

   

.. function:: printIfShown(theStr, show_type=SHOW_DEBUG, isToPrint=True, appendTypeName=True)


.. data:: SHOW_WARNING
   :annotation: = 0

   

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




.. data:: SHOW_WARNING
   :annotation: = 0

   

.. data:: SHOW_INFO
   :annotation: = 1

   

.. data:: SHOW_ERROR
   :annotation: = 2

   

.. data:: SHOW_DEBUG
   :annotation: = 3

   

.. data:: SHOW_CURRENT
   

   

.. py:class:: InterfaceDevice

   Interface class that represents a device.
   Hidden feature: variables that need to be saved must be type-hinted: e.g.: x: int. See :meth:`~optimeed.core.myjson.obj_to_json` for more info

   .. method:: assign(self, device_to_assign, resetAttribute=False)


      Copy the attribute values of device_to_assign to self. The references are not lost.

      :param device_to_assign: :class:`~optimeed.InterfaceDevice.InterfaceDevice`
      :param resetAttribute:



.. py:class:: HowToPlotGraph(attribute_x, attribute_y, kwargs_graph=None, excluded=None, exclusively=None, check_if_plot_elem=None)

   .. method:: exclude_col(self, id_col)


      Add id_col to exclude from the graph


   .. method:: exclusive_col(self, id_col)


      Set id_col to have exclusivity on the graph


   .. method:: __str__(self)




.. py:class:: CollectionInfo(theCollection, kwargs, theID)

   .. method:: get_collection(self)



   .. method:: get_kwargs(self)



   .. method:: get_id(self)




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




.. py:class:: Option_class_interface

   Bases: :class:`abc.ABC`

   Interface of the class 'Option_class'. It defines all the necessary methods to manage a set of options.

   .. method:: __str__(self)
      :abstractmethod:



   .. method:: get_optionValue(self, optionId: int)
      :abstractmethod:



   .. method:: set_optionValue(self, optionId: int, value)
      :abstractmethod:



   .. method:: get_all_options(self)
      :abstractmethod:


      Return a dictionnary containing tuples (name of the option, value of the option)
      :return: dict


   .. method:: set_all_options(self, options: Option_class_interface)
      :abstractmethod:


      The method allows to define all the options from another object of type 'Option_class_interface'
      :param options: Option_class_interface
      :return:


   .. method:: add_option(self, idOption: int, name: str, value)
      :abstractmethod:




.. py:class:: Options

   .. method:: get_name(self, idOption)



   .. method:: get_value(self, idOption)



   .. method:: add_option(self, idOption, name, value)



   .. method:: set_option(self, idOption, value)



   .. method:: copy(self)



   .. method:: set_self(self, the_options)



   .. method:: __str__(self)




.. py:class:: Option_class

   Bases: :class:`optimeed.core.options.Option_class_interface`

   .. method:: __str__(self)



   .. method:: get_optionValue(self, optionId)



   .. method:: set_optionValue(self, optionId, value)



   .. method:: get_all_options(self)



   .. method:: set_all_options(self, options)



   .. method:: add_option(self, idOption, name, value)




.. py:class:: Option_class_typed

   Bases: :class:`optimeed.core.options.Option_class_interface`

   .. attribute:: my_names
      :annotation: :Dict[int, str]

      

   .. attribute:: my_map
      :annotation: :Dict[int, str]

      

   .. attribute:: my_options_0
      :annotation: :Dict[int, int]

      

   .. attribute:: my_options_1
      :annotation: :Dict[int, float]

      

   .. attribute:: my_options_2
      :annotation: :Dict[int, bool]

      

   .. attribute:: my_options_3
      :annotation: :Dict[int, str]

      

   .. attribute:: my_options_4
      :annotation: :Dict[int, List[int]]

      

   .. attribute:: my_options_5
      :annotation: :Dict[int, List[float]]

      

   .. attribute:: my_options_6
      :annotation: :Dict[int, List[str]]

      

   .. attribute:: my_options_7
      :annotation: :Dict[int, List[bool]]

      

   .. method:: __get_types()
      :staticmethod:



   .. method:: get_optionValue(self, optionId: int)



   .. method:: set_optionValue(self, optionId: int, value)



   .. method:: get_all_options(self)



   .. method:: add_option(self, idOption: int, name: str, value)



   .. method:: __match(value, theType)
      :staticmethod:



   .. method:: set_all_options(self, options: Option_class_interface)



   .. method:: __str__(self)




.. py:class:: fast_LUT_interpolation(independent_variables, dependent_variables)

   Class designed for fast interpolation in look-up table when successive searchs are called often.
   Otherwise use griddata

   .. method:: interp_tri(xyz)
      :staticmethod:



   .. method:: interpolate(self, point, fill_value=np.nan)


      Perform the interpolation
      :param point: coordinates to interpolate (tuple or list of tuples for multipoints)
      :param fill_value: value to put if extrapolated.
      :return: coordinates



.. function:: interpolate_table(x0, x_values, y_values)

   From sorted table (x,y) find y0 corresponding to x0 (linear interpolation)


.. function:: derivate(t, y)


.. function:: linspace(start, stop, npoints)


.. function:: reconstitute_signal(amplitudes, phases, numberOfPeriods=1, x_points=None, n_points=50)

   Reconstitute the signal from fft. Number of periods of the signal must be specified if different of 1


.. function:: my_fft(y)

   Real FFT of signal Bx, with real amplitude of harmonics. Input signal must be within a period.


.. function:: cart2pol(x, y)


.. function:: pol2cart(rho, phi)


.. function:: partition(array, begin, end)


.. function:: quicksort(array)


.. function:: dist(p, q)

   Return the Euclidean distance between points p and q.
   :param p: [x, y]
   :param q: [x, y]
   :return: distance (float)


.. function:: sparse_subset(points, r)

   Returns a maximal list of elements of points such that no pairs of
   points in the result have distance less than r.
   :param points: list of tuples (x,y)
   :param r: distance
   :return: corresponding subset (list), indices of the subset (list)


.. function:: integrate(x, y)

   Performs Integral(x[0] to x[-1]) of y dx

   :param x: x axis coordinates (list)
   :param y: y axis coordinates (list)
   :return: integral value


.. function:: my_fourier(x, y, n, L)

   Fourier analys

   :param x: x axis coordinates
   :param y: y axis coordinates
   :param n: number of considered harmonic
   :param L: half-period length
   :return: a and b coefficients (y = a*cos(x) + b*sin(y))


.. function:: get_ellipse_axes(a, b, dphi)

   Trouve les longueurs des axes majeurs et mineurs de l'ellipse, ainsi que l'orientation de l'ellipse.
   ellipse: x(t) = A*cos(t), y(t) = B*cos(t+dphi)
   Etapes: longueur demi ellipse CENTRéE = sqrt(a^2 cos^2(x) + b^2 cos^2(t+phi)
   Minimisation de cette formule => obtention formule tg(2x) = alpha/beta


.. function:: rgetattr(obj, attr)

   Recursively get an attribute from object. Extends getattr method

   :param obj: object
   :param attr: attribute to get
   :return:


.. function:: rsetattr(obj, attr, val)


.. data:: MODULE_TAG
   :annotation: = __module__

   

.. data:: CLASS_TAG
   :annotation: = __class__

   

.. data:: EXCLUDED_TAGS
   

   

.. py:class:: SaveableObject

   Abstract class for dynamically type-hinted objects.
   This class is to solve the special case where the exact type of an attribute is not known before runtime, yet has to be saved.

   .. method:: get_additional_attributes_to_save(self)
      :abstractmethod:


      Return list of attributes corresponding to object, whose type cannot be determined statically (e.g. topology change)



.. function:: _get_object_class(theObj)


.. function:: _get_object_module(theObj)


.. function:: _object_to_FQCN(theobj)

   Gets module path of object


.. function:: _find_class(moduleName, className)


.. function:: json_to_obj(json_dict)

   Convenience class to create object from dictionary. Only works if CLASS_TAG is valid

   :param json_dict: dictionary loaded from a json file.
   :raise TypeError: if class can not be found
   :raise KeyError: if CLASS_TAG not present in dictionary


.. function:: json_to_obj_safe(json_dict, cls)

   Safe class to create object from dictionary.

   :param json_dict: dictionary loaded from a json file
   :param cls: class object to instantiate with dictionary


.. function:: _instantiates_annotated_object(_json_dict, _cls)


.. function:: _get_annotations(theObj)

   Return annotated attributes


.. function:: obj_to_json(theObj)

   Extract the json dictionary from the object. The data saved are automatically detected, using typehints.
   ex: x: int=5 will be saved, x=5 won't.
   Inheritance of annotation is managed by this function


.. function:: _get_attributes_to_save(theObj)

   Return list (attribute, is_first)


.. function:: get_json_module_tree(theObj)

   Return dict containing {CLASS_TAG: "class_name", MODULE_TAG: "module_name", "attribute1":{"class_name": "module_name", ...}}


.. function:: encode_str_json(theStr)


.. function:: decode_str_json(theStr)


.. function:: export_to_tikz_groupGraphs(theGraphs: Graphs, foldername, additionalPreamble=lambda: '', additionalAxisOptions=lambda graphId: '', additionalTraceOptions=lambda graphId, traceId: '', debug=False)

   Export the graphs as group

   :param theGraphs: Graphs to save
   :param foldername: Foldername to save
   :param additionalPreamble: method that returns string for custom tikz options
   :param additionalAxisOptions: method that returns string for custom tikz options
   :param additionalTraceOptions: method that returns string for custom tikz options
   :return:


