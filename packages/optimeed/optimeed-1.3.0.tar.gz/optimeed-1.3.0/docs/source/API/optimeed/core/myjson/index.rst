``myjson``
===========================

.. py:module:: optimeed.core.myjson


Module Contents
---------------

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


