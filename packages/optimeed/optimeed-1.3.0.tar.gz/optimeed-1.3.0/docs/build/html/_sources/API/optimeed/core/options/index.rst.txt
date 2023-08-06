``options``
============================

.. py:module:: optimeed.core.options


Module Contents
---------------

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




