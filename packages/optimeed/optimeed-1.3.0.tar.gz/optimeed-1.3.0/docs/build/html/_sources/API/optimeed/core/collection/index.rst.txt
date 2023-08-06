``collection``
===============================

.. py:module:: optimeed.core.collection


Module Contents
---------------

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



