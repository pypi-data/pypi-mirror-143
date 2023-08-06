``parametric_analysis``
===============================================

.. py:module:: optimeed.consolidate.parametric_analysis


Module Contents
---------------

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




