``pyqtgraphRedefine``
==========================================================================

.. py:module:: optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraphRedefine


Module Contents
---------------

.. data:: isOnWindows
   

   Other modified files (directly): ScatterPlotItem.py, to change point selection. Ctrl + clic: select area. Clic: only one single point:


   class OnClicSelector:
       def __init__(self):
           self.p_list = []

       def add_point(self, newp):
           self.p_list.append(newp)

       def draw(self, painter):
           if len(self.p_list) > 2:
               pen = fn.mkPen(1)
               pen.setWidthF(2)
               painter.setPen(pen)
               painter.drawPolyline(QtGui.QPolygonF(self.p_list))

       def reset(self):
           self.p_list = []

       def getPath(self):
           return path.Path([(p.x(), p.y()) for p in self.p_list] + [(self.p_list[-1].x(), self.p_list[-1].y())])

   ------------------------------
       def mouseDragEvent(self, ev):
           if ev.modifiers() and QtCore.Qt.ControlModifier:
               ev.accept()
               self.clicSelector.add_point(ev.pos())
               if ev.isFinish():
                   path = self.clicSelector.getPath()
                   points = self.points()
                   contains_points = path.contains_points([(p.pos().x(), p.pos().y()) for p in points])
                   indices = [i for i, cond in enumerate(contains_points) if cond]
                   points_clicked = [points[i] for i in indices]
                   self.ptsClicked = points_clicked
                   self.sigClicked.emit(self, self.ptsClicked)
                   self.clicSelector.reset()
               self.update()
           else:
               ev.ignore()


.. py:class:: myGraphicsLayoutWidget(parent=None, **_kwargs)

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraph.GraphicsView`

   .. method:: useOpenGL(self, b=True)


      Overwrited to fix bad antialiasing while using openGL



.. py:class:: myGraphicsLayout

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraph.GraphicsLayout`

   .. method:: addItem(self, item, row=None, col=None, rowspan=1, colspan=1)


      Add an item to the layout and place it in the next available cell (or in the cell specified).
      The item must be an instance of a QGraphicsWidget subclass.


   .. method:: set_graph_disposition(self, item, row=1, col=1, rowspan=1, colspan=1)


      Function to modify the position of an item in the list

      :param item: WidgetPlotItem to set
      :param row: Row
      :param col: Column
      :param rowspan:
      :param colspan:
      :return:



.. py:class:: myItemSample(item)

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraph.graphicsItems.LegendItem.ItemSample`

   .. method:: set_offset(self, offset)



   .. method:: set_width_cell(self, width)



   .. method:: paint(self, p, *args)


      Overwrites to make matlab-like samples



.. py:class:: myLegend(size=None, offset=(30, 30), is_light=False)

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraph.LegendItem`

   Legend that fixes bugs (flush left + space) from pyqtgraph's legend

   .. method:: set_space_sample_label(self, theSpace)


      To set the gap between the sample and the label


   .. method:: set_offset_sample(self, offset)


      To tune the offset between the sample and the text


   .. method:: set_width_cell_sample(self, width)


      Set width of sample


   .. method:: updateSize(self)



   .. method:: addItem(self, item, name)


      Overwrites to flush left


   .. method:: apply_width_sample(self)



   .. method:: set_font(self, font_size, font_color, fontname=None)



   .. method:: paint(self, p, *args)


      Overwrited to select background color


   .. method:: set_position(self, position, offset)


      Set the position of the legend, in a corner.

      :param position: String (NW, NE, SW, SE), indicates which corner the legend is close
      :param offset: Tuple (xoff, yoff), x and y offset from the edge
      :return:



.. py:class:: myLabelItem

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraph.LabelItem`

   .. method:: setText(self, text, **args)


      Overwrited to add font-family to options 



.. py:class:: myAxis(orientation)

   Bases: :class:`optimeed.visualize.gui.widgets.graphsVisualWidget.pyqtgraph.AxisItem`

   .. method:: get_label_pos(self)


      Overwrited to place label closer to the axis


   .. method:: resizeEvent(self, ev=None)


      Overwrited to place label closer to the axis


   .. method:: set_label_pos(self, orientation, x_offset=0, y_offset=0)



   .. method:: set_number_ticks(self, number)




