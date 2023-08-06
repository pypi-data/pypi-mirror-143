``hypervolume``
===============================================================

.. py:module:: optimeed.optimize.optiAlgorithms.convergence.hypervolume


Module Contents
---------------

.. data:: __author__
   :annotation: = Simon Wessing

   

.. py:class:: HyperVolume(referencePoint)

   Hypervolume computation based on variant 3 of the algorithm in the paper:
   C. M. Fonseca, L. Paquete, and M. Lopez-Ibanez. An improved dimension-sweep
   algorithm for the hypervolume indicator. In IEEE Congress on Evolutionary
   Computation, pages 1157-1163, Vancouver, Canada, July 2006.

   Minimization is implicitly assumed here!

   .. method:: compute(self, front)


      Returns the hypervolume that is dominated by a non-dominated front.

      Before the HV computation, front and reference point are translated, so
      that the reference point is [0, ..., 0].


   .. method:: hvRecursive(self, dimIndex, length, bounds)


      Recursive call to hypervolume calculation.

      In contrast to the paper, the code assumes that the reference point
      is [0, ..., 0]. This allows the avoidance of a few operations.


   .. method:: preProcess(self, front)


      Sets up the list data structure needed for calculation.


   .. method:: sortByDimension(self, nodes, i)


      Sorts the list of nodes by the i-th value of the contained points.



.. py:class:: MultiList(numberLists)

   A special data structure needed by FonsecaHyperVolume.

   It consists of several doubly linked lists that share common nodes. So,
   every node has multiple predecessors and successors, one in every list.

   .. py:class:: Node(numberLists, cargo=None)

      .. method:: __str__(self)




   .. method:: __str__(self)



   .. method:: __len__(self)


      Returns the number of lists that are included in this MultiList.


   .. method:: getLength(self, i)


      Returns the length of the i-th list.


   .. method:: append(self, node, index)


      Appends a node to the end of the list at the given index.


   .. method:: extend(self, nodes, index)


      Extends the list at the given index with the nodes.


   .. method:: remove(self, node, index, bounds)


      Removes and returns 'node' from all lists in [0, 'index'[.


   .. method:: reinsert(self, node, index, bounds)


      Inserts 'node' at the position it had in all lists in [0, 'index'[
      before it was removed. This method assumes that the next and previous
      nodes of the node that is reinserted are in the list.



