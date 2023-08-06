``gui_data_selector``
===============================================

.. py:module:: optimeed.visualize.gui.gui_data_selector


Module Contents
---------------

.. data:: app
   

   

.. py:class:: Action_on_selector_update

   .. method:: selector_updated(self, selection_name, the_collection, indices_data)
      :abstractmethod:


      Action to perform once the data have been selected
      :param selection_name: name of the selection (deprecated ?)
      :param the_collection: the collection
      :param indices_data: indices of the data
      :return:



.. py:class:: Attribute_selector(attribute_name, value)

   .. method:: add_child(self, child)



   .. method:: get_children(self)



   .. method:: get_name(self)



   .. method:: get_min_max_attributes(self)



   .. method:: __str__(self)




.. py:class:: Container_attribute_selector(containerName)

   .. method:: add_child(self, child)



   .. method:: add_attribute_selector(self, attribute_selector)



   .. method:: set_attribute_selectors(self, attribute_selectors)



   .. method:: get_name(self)



   .. method:: get_children(self)



   .. method:: get_attribute_selectors(self)



   .. method:: __str__(self)




.. py:class:: GuiDataSelector(list_ListDataStruct_in, actionOnUpdate: Action_on_selector_update)

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   .. attribute:: theActionOnUpdate
      

      Generate GUI


   .. method:: apply_filters(self, _)



   .. method:: run(self)




.. function:: is_object_selected(container_in, object_in)


.. function:: check_and_add_if_float(the_container, attribute_value, attribute_name, parent=None)


.. function:: manage_list(the_container, in_object, _listOfValues, _listName)


.. function:: get_attr_object(the_container, in_object)


