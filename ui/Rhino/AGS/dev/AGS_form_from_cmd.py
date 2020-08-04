from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import rhinoscriptsyntax as rs
import compas_rhino

from compas_ags.diagrams import FormGraph
from compas_ags.diagrams import FormDiagram
from compas_ags.diagrams import ForceDiagram

from compas.geometry import Line
from compas.geometry import is_point_on_line
from compas_rhino.utilities import get_object_layers

__commandname__ = "AGS_form_from"


def RunCommand(is_interactive):

    if 'AGS' not in sc.sticky:
        compas_rhino.display_message('AGS has not been initialised yet.')
        return

    system = sc.sticky['AGS']['system']
    scene = sc.sticky['AGS']['scene']

    options = ["Obj", "Lines", "Layer", "Json", ]

    option = compas_rhino.rs.GetString("Construct FormDiagram from", strings=options)

    if not option:
        return

    if option == "Obj":
        filepath = compas_rhino.browse_for_file('Select an input file.', folder=system['session.dirname'], filter='obj')
        if not filepath:
            return
        graph = FormGraph.from_obj(filepath)

    elif option == "Lines":
        guids = compas_rhino.select_lines(message='Select Form Diagram Lines')
        if not guids:
            return
        rs.HideObjects(guids)
        lines = compas_rhino.get_line_coordinates(guids)
        graph = FormGraph.from_lines(lines)

    elif option == "Layer":
        layer = rs.CurrentLayer()
        layer_name = compas_rhino.rs.GetString("Layer to construct FormDiagram", layer)
        guids = compas_rhino.get_lines(layer=layer_name)
        if not guids:
            return
        rs.HideObjects(guids)
        lines = compas_rhino.get_line_coordinates(guids)
        graph = FormGraph.from_lines(lines)

    elif option == "Json":
        filepath = compas_rhino.browse_for_file('Select an input file.', folder=system['session.dirname'], filter='json')
        if not filepath:
            return
        graph = FormGraph.from_json(filepath)

     # check planarity
     
    if not graph.is_planar_embedding():
        raise ValueError("The graph is not planar. Check your graph!")

    form = FormDiagram.from_graph(graph)

    scene.add(form, name='Form', layer='AGS::FormDiagram')

    scene.clear()
    scene.update()


# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':

    RunCommand(True)
