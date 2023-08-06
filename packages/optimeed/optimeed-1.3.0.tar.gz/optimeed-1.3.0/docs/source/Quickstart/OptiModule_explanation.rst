Quickstart Optimization
=======================

An optimization process can be presented as following:

.. image:: optiScheme.svg


* **Optimization algorithm:** :class:`~optimeed.optimize.optiAlgorithms.algorithmInterface`. This is the algorithm that performs the optimization, and outputs a vector of variables between [0, 1[.
* **Maths to physics:** :class:`~optimeed.optimize.mathsToPhysics.interfaceMathsToPhysics`. Transforms the output vector of the optimization algorithm  to the variables of a :class:`~optimeed.core.interfaceDevice.InterfaceDevice`. The usage of this block becomes meaningful for more complex optimization problem, such as optimizing a BLDC motor while keeping the outer diameter constant. In this case, a good implementation of the M2P block automatically scales the inner dimensions of the motor to comply with this constraint.
* **Characterization:** :class:`~optimeed.optimize.characterization.interfaceCharacterization`. Based on the attributes of the device, performs some computation. This block is nearly useless for simple optimization problems (when the objective function is easily computed) but becomes interesting for more complex problems, where many things need to be precalculated before obtaining the objective functions and constraints. This for example can hold an analytical or a FEM magnetic model. A sub-optimization could also be performed there.
* **Objective and constraints:** :class:`~optimeed.optimize.objAndCons.interfaceObjCons`. These classes correspond to either what has to be minimized, or which constraints <=0 has to be complied with.


Quick example: :math:`\min_{x, y \in [0, 2]} f(x) = \sqrt{ 1 + (y+3) \cdot x^2 }, g(x) = 4 + 2 \sqrt{y+3} \cdot \sqrt{1+(x-1)^2}`, under the constrained that :math:`x \leq 0.55`. This is a bi-objective problem and will lead to a pareto front.

.. literalinclude:: ../../../tutorial/simpleFunctionOptimizationWithVisual/example.py
