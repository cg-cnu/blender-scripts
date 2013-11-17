# Wireframe on shaded
# Toggle the display of wireframe on the objects visible in the viewport
# written by Sreenivas Alapati

import bpy

def main(context):            
    objects_list = [ obj for obj in bpy.data.objects if obj.type in ['MESH']]
    objects_with_wire = [obj for obj in objects_list if obj.show_wire == True]
    
    if len(objects_with_wire) == 0:
        for ob in objects_list:
            ob.show_wire = ob.show_all_edges = True             
    else:
        for ob in objects_with_wire:
            ob.show_wire = ob.show_all_edges = False            

class wireframeOnShaded(bpy.types.Operator):
    """ Displays wire frame on shaded with draw all edges on all objects"""
    bl_idname = "object.wireframe_on_shaded"
    bl_label = "Wireframe on shaded"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(wireframeOnShaded)
    km = bpy.context.window_manager.keyconfigs.default.keymaps['Object Mode']
    kmi = km.keymap_items.new("object.wireframe_on_shaded", 'W', 'PRESS', shift=True)
   
def unregister():
    bpy.utils.unregister_class(wireframeOnShaded)
    km = bpy.context.window_manager.keyconfigs.default.keymaps['Object Mode']
    for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"object.wireframe_on_shaded", }):
        km.keymap_items.remove(kmi) 

if __name__ == "__main__":
    register()
