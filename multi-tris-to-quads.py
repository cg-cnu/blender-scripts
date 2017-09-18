###
# Select a bunch of objects 
# all the selected objects will be converted to quads
###

import bpy

# cycle though all selected objects
for obj in bpy.context.selected_objects:
    # make the current selected object active
    bpy.context.scene.objects.active = obj
    # select all the vertices
    for v in bpy.context.active_object.data.vertices:
        v.select = True
    # enter edit mode
    bpy.ops.object.editmode_toggle()
    # make all tris->quads
    bpy.ops.mesh.tris_convert_to_quads() 
    # exit edit mode
    bpy.ops.object.editmode_toggle()
