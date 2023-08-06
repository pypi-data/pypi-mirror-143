``widget_line_drawer``
========================================================

.. py:module:: optimeed.visualize.gui.widgets.widget_line_drawer


Module Contents
---------------

.. py:class:: widget_line_drawer(minWinHeight=300, minWinWidth=300, is_light=True)

   Bases: :class:`PyQt5.QtWidgets.QWidget`

   Widget allowing to display several lines easily

   .. attribute:: signal_must_update
      

      

   .. method:: on_update_signal(self, listOfLines)



   .. method:: delete_lines(self, key_id)


      Dele the lines
      :param key_id: id to delete
      :return:


   .. method:: set_lines(self, listOfLines, key_id=0, pen=None)


      Set the lines to display
      :param listOfLines: list of [x1, y1, x2, y2] corresponding to lines
      :param key_id: id of the trace
      :param pen: pen used to draw the lines
      :return:


   .. method:: paintEvent(self, event, painter=None)



   .. method:: get_extrema_lines(self)




