import FreeCAD
import FreeCADGui
import Draft
import Mesh
import Part
import MeshPart
import importDXF
from PySide import QtGui

import numpy as np
import flatmesh

doc = FreeCAD.ActiveDocument

selection = FreeCADGui.Selection.getSelectionEx()
if len(selection) > 0:
	facebinder = Draft.make_facebinder(selection)
	#Draft.autogroup(facebinder)

	shape = Part.getShape(facebinder)
	mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=1)

	points = np.array([[i.x, i.y, i.z] for i in mesh.Points])
	faces = np.array([list(i) for i in  mesh.Topology[1]])

	flattener = flatmesh.FaceUnwrapper(points, faces)
	flattener.findFlatNodes(64, 0.99)
	boundaries = flattener.getFlatBoundaryNodes()

	wires = map(lambda boundary: Part.makePolygon([App.Vector(*node) for node in boundary]), boundaries)
	unwrappedParts = [Part.show(Part.Wire(wire)) for wire in wires]


	fileName = QtGui.QFileDialog.getSaveFileName(None, 'Save to Dxf', selectedFilter='*.dxf')[0]
	print(unwrappedParts, fileName)
	importDXF.export(unwrappedParts, fileName)
