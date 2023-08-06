``tools``
==========================

.. py:module:: optimeed.core.tools


Module Contents
---------------

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


