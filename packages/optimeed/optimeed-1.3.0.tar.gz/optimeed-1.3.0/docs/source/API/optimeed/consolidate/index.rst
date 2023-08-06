**consolidate**
===========================

.. py:module:: optimeed.consolidate


.. toctree::
   :titlesonly:
   :maxdepth: 1

   parametric_analysis/index.rst


Package Contents
----------------

.. py:class:: Option_class

   Bases: :class:`optimeed.core.options.Option_class_interface`

   .. method:: __str__(self)



   .. method:: get_optionValue(self, optionId)



   .. method:: set_optionValue(self, optionId, value)



   .. method:: get_all_options(self)



   .. method:: set_all_options(self, options)



   .. method:: add_option(self, idOption, name, value)




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




.. function:: getPath_workspace()


.. function:: rsetattr(obj, attr, val)


.. function:: rgetattr(obj, attr)

   Recursively get an attribute from object. Extends getattr method

   :param obj: object
   :param attr: attribute to get
   :return:


.. py:class:: Parametric_Collection(**kwargs)

   Bases: :class:`optimeed.core.collection.ListDataStruct`

   .. method:: get_extension()
      :staticmethod:




.. py:class:: Parametric_parameter(analyzed_attribute, reference_device)

   Abstract class for a parametric parameter

   .. method:: get_values(self)
      :abstractmethod:



   .. method:: get_reference_device(self)



   .. method:: get_analyzed_attribute(self)




.. py:class:: Parametric_minmax(analyzed_attribute, reference_device, minValue, maxValue, is_relative=False, npoints=10)

   Bases: :class:`optimeed.consolidate.parametric_analysis.Parametric_parameter`

   .. method:: get_values(self)




.. py:class:: Parametric_analysis(theParametricParameter, theCharacterization, filename_collection=None, description_collection=None, autosave=False)

   Bases: :class:`optimeed.core.Option_class`

   .. attribute:: NUMBER_OF_CORES
      :annotation: = 1

      

   .. method:: run(self)


      Instantiates input arguments for analysis


   .. method:: evaluate(self, theDevice)



   .. method:: initialize_output_collection(self)




