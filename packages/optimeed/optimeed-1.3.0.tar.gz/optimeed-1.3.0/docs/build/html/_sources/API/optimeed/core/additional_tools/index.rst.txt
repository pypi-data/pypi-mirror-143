``additional_tools``
=====================================

.. py:module:: optimeed.core.additional_tools


Module Contents
---------------

.. py:class:: fast_LUT_interpolation(independent_variables, dependent_variables)

   Class designed for fast interpolation in look-up table when successive searchs are called often.
   Otherwise use griddata

   .. method:: interp_tri(xyz)
      :staticmethod:



   .. method:: interpolate(self, point, fill_value=np.nan)


      Perform the interpolation
      :param point: coordinates to interpolate (tuple or list of tuples for multipoints)
      :param fill_value: value to put if extrapolated.
      :return: coordinates



.. function:: interpolate_table(x0, x_values, y_values)

   From sorted table (x,y) find y0 corresponding to x0 (linear interpolation)


.. function:: derivate(t, y)


.. function:: linspace(start, stop, npoints)


.. function:: reconstitute_signal(amplitudes, phases, numberOfPeriods=1, x_points=None, n_points=50)

   Reconstitute the signal from fft. Number of periods of the signal must be specified if different of 1


.. function:: my_fft(y)

   Real FFT of signal Bx, with real amplitude of harmonics. Input signal must be within a period.


.. function:: cart2pol(x, y)


.. function:: pol2cart(rho, phi)


.. function:: partition(array, begin, end)


.. function:: quicksort(array)


.. function:: dist(p, q)

   Return the Euclidean distance between points p and q.
   :param p: [x, y]
   :param q: [x, y]
   :return: distance (float)


.. function:: sparse_subset(points, r)

   Returns a maximal list of elements of points such that no pairs of
   points in the result have distance less than r.
   :param points: list of tuples (x,y)
   :param r: distance
   :return: corresponding subset (list), indices of the subset (list)


.. function:: integrate(x, y)

   Performs Integral(x[0] to x[-1]) of y dx

   :param x: x axis coordinates (list)
   :param y: y axis coordinates (list)
   :return: integral value


.. function:: my_fourier(x, y, n, L)

   Fourier analys

   :param x: x axis coordinates
   :param y: y axis coordinates
   :param n: number of considered harmonic
   :param L: half-period length
   :return: a and b coefficients (y = a*cos(x) + b*sin(y))


.. function:: get_ellipse_axes(a, b, dphi)

   Trouve les longueurs des axes majeurs et mineurs de l'ellipse, ainsi que l'orientation de l'ellipse.
   ellipse: x(t) = A*cos(t), y(t) = B*cos(t+dphi)
   Etapes: longueur demi ellipse CENTRéE = sqrt(a^2 cos^2(x) + b^2 cos^2(t+phi)
   Minimisation de cette formule => obtention formule tg(2x) = alpha/beta


