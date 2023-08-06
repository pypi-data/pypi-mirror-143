``ContextHandler``
=================================================================

.. py:module:: optimeed.visualize.gui.widgets.openGLWidget.ContextHandler


Module Contents
---------------

.. data:: MODE_ZOOM
   :annotation: = 0

   

.. data:: MODE_ROTATION
   :annotation: = 1

   

.. data:: MODE_LIGHT
   :annotation: = 2

   

.. data:: NUMBER_OF_MODES
   :annotation: = 3

   

.. data:: CLIC_LEFT
   :annotation: = 0

   

.. data:: CLIC_RIGHT
   :annotation: = 1

   

.. py:class:: SpecialButtonsMapping


.. py:class:: MyText(color, fontSize, theStr, windowPosition)


.. py:class:: ContextHandler

   .. method:: set_specialButtonsMapping(self, theSpecialButtonsMapping)



   .. method:: set_deviceDrawer(self, theDeviceDrawer)



   .. method:: set_deviceToDraw(self, theDeviceToDraw)



   .. method:: resizeWindowAction(self, new_width, new_height)



   .. method:: mouseWheelAction(self, deltaAngle)



   .. method:: mouseClicAction(self, button, my_x, y)



   .. method:: mouseMotionAction(self, my_x, y)



   .. method:: keyboardPushAction(self, key)



   .. method:: keyboardReleaseAction(self, key, my_x, y)



   .. method:: __draw_axis__(self)



   .. method:: redraw(self)



   .. method:: get_text_to_write(self)



   .. method:: __lightingInit__(self)



   .. method:: initialize(self)



   .. method:: __reset__(self)




