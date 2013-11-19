# UDIM Layout
# Divide the object to multiple parts.
# Assign the mtl groups to each part.
# unwrap the parts and place the uvlayouts on top of each other in 0 to 1 uv space.
#
# go to edit mode.
# deselect the mesh
# Keep the mouse in uv Editor and press Shift + U.
#
# Based on the mtl groups this will create the udim layout.
# creates a new uvLayout with the name "_UVMap_Mari" preceding it.
#

bl_info = {
    "name": "UDIM UV Layout",
    "description": " Layout uvs in the mari style - UDIM.",
    "author": "Sreenivas Alapati",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "category": "UV"}

import bpy

def main(context):

    C = bpy.context
    O = bpy.ops

    object_active = C.active_object
    object_data = bpy.data.objects[object_active.name].data

    # get the list of the material sot items.
    material_slots = len(object_active.material_slots.items())
    slot = x_tran = y_tran = 0

    # add  new uv Map 
    O.mesh.uv_texture_add()

    # rename it to the objectName_uvMap_Mari
    object_data.uv_textures.active.name = C.object.name + '_UVMap_Mari' 

    # iterate through the list of material slots
    while slot < material_slots:

        # set the index of the mtl to the current active mtl
        C.object.active_material_index = slot

        # select the vertices from the current mtl slot
        O.object.material_slot_select()

        # select the uvs from the vertices
        O.uv.select_all()    

        # Move the uv layout to the next grid
        O.transform.translate(value=(x_tran, y_tran, 0))

        # deselect the selected mtl slot
        O.object.material_slot_deselect()

        # increase slot 
        slot += 1
        value = str(slot) 
        if slot < 10:
            x_tran, y_tran = int(value[0]), 0           
        else:
            x_tran, y_tran = int(value[1]), int(value[0])

class udimUvLayout(bpy.types.Operator):
    """Layouts uvs in the mari uv format - UDIM """
    bl_idname = "object.udim_uv_layout"
    bl_label = "udim uv layout"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(udimUvLayout)
    km = bpy.context.window_manager.keyconfigs.default.keymaps['UV Editor']
    kmi = km.keymap_items.new("object.udim_uv_layout", 'U', 'PRESS', shift=True)

def unregister():
    bpy.utils.unregister_class(udimUvLayout)
    km = bpy.context.window_manager.keyconfigs.default.keymaps['UV Editor']
    for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"object.udim_uv_layout", }):
        km.keymap_items.remove(kmi) 

if __name__ == "__main__":
    register()