``interfaceDevice``
====================================

.. py:module:: optimeed.core.interfaceDevice


Module Contents
---------------

.. py:class:: InterfaceDevice

   Interface class that represents a device.
   Hidden feature: variables that need to be saved must be type-hinted: e.g.: x: int. See :meth:`~optimeed.core.myjson.obj_to_json` for more info

   .. method:: assign(self, device_to_assign, resetAttribute=False)


      Copy the attribute values of device_to_assign to self. The references are not lost.

      :param device_to_assign: :class:`~optimeed.InterfaceDevice.InterfaceDevice`
      :param resetAttribute:



