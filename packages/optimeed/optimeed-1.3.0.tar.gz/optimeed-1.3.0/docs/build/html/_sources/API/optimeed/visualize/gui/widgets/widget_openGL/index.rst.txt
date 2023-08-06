``widget_openGL``
===================================================

.. py:module:: optimeed.visualize.gui.widgets.widget_openGL


Module Contents
---------------

.. py:class:: widget_openGL(parent=None)

   Bases: :class:`PyQt5.QtWidgets.QOpenGLWidget`

   Interface that provides opengl capabilities.
   Ensures zoom, light, rotation, etc.

   .. method:: sizeHint(self)



   .. method:: minimumSizeHint(self)



   .. method:: set_deviceDrawer(self, theDeviceDrawer)


      Set a drawer :class:`optimeed.visualize.gui.widgets.openGLWidget.DeviceDrawerInterface.DeviceDrawerInterface`


   .. method:: set_deviceToDraw(self, theDeviceToDraw)


      Set the device to draw :class:`optimeed.InterfaceDevice.InterfaceDevice`


   .. method:: _get_specialButtonsMapping()
      :staticmethod:



   .. method:: initializeGL(self)



   .. method:: paintGL(self)



   .. method:: resizeGL(self, w, h)



   .. method:: mousePressEvent(self, event)



   .. method:: mouseMoveEvent(self, event)



   .. method:: keyPressEvent(self, event)



   .. method:: wheelEvent(self, QWheelEvent)




