Loading and saving data
=======================

You will probably have to often manipulate data, saving them and loading them.


Imagine the following structure to be saved:

.. code-block:: python

    class TopoA:
        def __init__(self):
            self.R_in = 3e-3
            self.R_out = 5e-3


    class MyMotor:
        def __init__(self):
            self.rotor = TopoA()
            self.length = 5e-3
            self.dummyVariableToNotSave = 1234

optimeed provides a way to export that directly in JSON format. It detects the variables to save from type hints:

.. code-block:: python
   :emphasize-lines: 2, 3, 11, 12

    class TopoA:
        R_in: float
        R_out: float

        def __init__(self):
            self.R_in = 3e-3
            self.R_out = 5e-3


    class MyMotor:
        rotor: TopoA
        length: float

        def __init__(self):
            self.rotor = TopoA()
            self.length = 5e-3
            self.dummyVariableToNotSave = 1234

If type hint is not possible because some type is not known before the running time, optimeed provides an additional tool :class:`~optimeed.core.myjson.SaveableObject`:

.. code-block:: python
   :emphasize-lines: 1, 5, 6, 13, 14, 21, 22

    from optimeed.core import SaveableObject


    class TopoA:
        R_in: float
        R_out: float

        def __init__(self):
            self.R_in = 3e-3
            self.R_out = 5e-3


    class MyMotor(SaveableObject):
        length: float

        def __init__(self):
            self.rotor = TopoA()
            self.length = 5e-3
            self.dummyVariableToNotSave = 1234

        def get_additional_attributes_to_save(self):
            return ["rotor"]

The item can then be converted to a dictionary using :meth:`~optimeed.core.myjson.obj_to_json`, which can then be converted to string liberal using "json.dumps" and written on a file. To recover
To recover the object, read the file and interpret is as a dictionary using "json.load". Then, convert the dictionary by using :meth:`~optimeed.core.myjson.json_to_obj`

Alternatively, it might be simpler to use the class :class:`~optimeed.core.collection.ListDataStruct` (or similar user-custom class), which provides high-level save and load option. This is what is done in :class:`~optimeed.optimize.optimizer.OptiHistoric`
