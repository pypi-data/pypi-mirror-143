``linkDataGraph``
==================================

.. py:module:: optimeed.core.linkDataGraph


Module Contents
---------------

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




