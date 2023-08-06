``gui_mainWindow``
============================================

.. py:module:: optimeed.visualize.gui.gui_mainWindow


Module Contents
---------------

.. data:: app
   

   

.. function:: start_qt_mainloop()

   Starts qt mainloop, which is necessary for qt to handle events


.. function:: stop_qt_mainloop()

   Stops qt mainloop and resumes to program


.. py:class:: gui_mainWindow(QtWidgetList, isLight=True, actionOnWindowClosed=None, neverCloseWindow=False, title_window='Awesome Visualisation Tool', size=None)

   Bases: :class:`PyQt5.QtWidgets.QMainWindow`

   Main class that spawns a Qt window. Use :meth:`~gui_mainWindow.run` to display it.

   .. method:: set_actionOnClose(self, actionOnWindowClosed)



   .. method:: closeEvent(self, event)



   .. method:: run(self, hold=False)


      Display the window


   .. method:: hold()
      :staticmethod:



   .. method:: keyPressEvent(self, event)




