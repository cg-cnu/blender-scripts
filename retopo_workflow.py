'''
Just to improve and automate the workflow of retopo
put all the necessary things in one click
http://cgcookie.com/blender/2011/08/08/retopology-with-the-bsurfaces-add-on/
'''
import bpy 

C = bpy.context
D = bpy.data
O = bpy.ops

def main(context):
    ## check if there is a selected object.
    if C.selected_objects == []:
        print ('Please select a mesh object')
    else:
        name = C.active_object.name
        if D.objects[name].type != 'MESH':
            print ('You have selected a non mesh object')
        else:
            # add mesh
            O.mesh.primitive_plane_add()
            # set its positon to lidar's origin 
            C.object.location.xyz = bpy.data.objects[name].location.xyz
            # rename the object as name_retopo
            C.active_object.name = name + '_retopo'
            # get the name of the object as retopo         
            retopo = C.active_object.name    
            
            # apply shrinkwrap and rename
            O.object.modifier_add(type='SHRINKWRAP')      
            D.objects[retopo].modifiers['Shrinkwrap'].target = bpy.data.objects[name]
            D.objects[retopo].modifiers['Shrinkwrap'].name = name + '_Shrinkwrap'
            
            # delete the verts    
            O.object.editmode_toggle()
            O.mesh.delete(type='VERT')
            O.object.editmode_toggle()

            # create a new grease pencil layer and rename it
            O.gpencil.data_add()
            O.gpencil.layer_add()        
            D.objects[name + '_retopo'].grease_pencil.name = name + '_gpencil'
            # set the layer mode to surface
            D.grease_pencil[name + '_gpencil'].draw_mode = 'SURFACE'

class RetopoWorkflow(bpy.types.Operator):
    """ sets the object ready for retopo """
    bl_idname = "object.retopo_workflow"
    bl_label = "Retopo Workflow"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RetopoWorkflow)

def unregister():
    bpy.utils.unregister_class(RetopoWorkflow) 

if __name__ == "__main__":
    register()
