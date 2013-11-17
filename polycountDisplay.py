# The original author of this script is Anamalous Underdog
# http://anomalousunderdog.blogspot.in/
# main credit goes to him for developing the whole addon
# I was just fooling around with the script and trying to implement the following

# dynamic update of the selection in edit mode and object mode 
# Along with triangles list... verts, edges, 
# For the whole scene, selected object, selection in edit mode

#   All     obj     sel   
# V  
# E
# F
# T
# Test Ui https://www.dropbox.com/s/3wptscpdcszl2qk/ui.png
# give the option to the user to choose from the list of things to display

import bpy, bmesh
import blf
import bgl

#
# show how many triangles your 3d model would have
# if its faces were all converted to triangles
# this is mostly useful for videogame models
# where polygon budget is quantified in triangles
# since game engines convert everything to triangles anyway
#
# Limitations:
#
# 1. Only works properly on one 3D View for now. Multiple 3D Views don't display triangle count properly
# 2. Doesn't update while a mesh is being edited. Only updates once the user goes back to object mode.
# 3. Triangle count of selection only works on objects as a whole. Doesn't count per selected faces while in edit mode.
#

bl_info = {
    "name": "Polygon Count Display",
    "author": "Anomalous Underdog",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "location": "View3D > Properties panel > Poly Count Display",
    "description": "Shows how many triangles your 3d model would have if its faces were all converted to triangles.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": 'TESTING',
    "category": "3D View"
}

class PolyCountPanel(bpy.types.Panel):
    bl_label = "Poly Count Display"
    bl_idname = "OBJECT_PT_poly_count"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        sc = context.scene
        wm = context.window_manager
        layout = self.layout

        if not wm.polycount_run:
            layout.operator("view3d.polycount", text="Start display",
                icon='PLAY')
        else:
            layout.operator("view3d.polycount", text="Stop display",
                icon='PAUSE')

        col = layout.column(align=True)
        #row = col.row(align=True)
        #row.prop(sc, "polycount_show_in_3d_view")
        row = col.row(align=True)
        row.prop(sc, "polycount_pos_x")
        row.prop(sc, "polycount_pos_y")
        row = col.row(align=True)
        row.prop(sc, "polycount_font_size")

        layout.prop(sc, "polycount_font_color")


# properties used by the script
def init_properties():
    scene = bpy.types.Scene
    #view3d = bpy.types.SpaceView3D
    wm = bpy.types.WindowManager

    scene.polycount_pos_x = bpy.props.IntProperty(
        name="Pos X",
        description="Margin on the x axis",
        default=23,
        min=0,
        max=100)
    scene.polycount_pos_y = bpy.props.IntProperty(
        name="Pos Y",
        description="Margin on the y axis",
        default=20,
        min=0,
        max=100)
    scene.polycount_font_size = bpy.props.IntProperty(
        name="Font",
        description="Fontsize",
        default=15, min=10, max=150)
    scene.polycount_font_color = bpy.props.FloatVectorProperty(
        name="Color",
        description="Font color",
        default=(1.0, 1.0, 1.0),
        min=0,
        max=1,
        subtype='COLOR')

    #view3d._polycount_show_in_3d_view = bpy.props.BoolProperty(
    #    name="Show poly count in 3d View",
    #    description = "Shows poly count in 3d view if true.",
    #    default = False)
    #view3d.polycount_show_in_3d_view = property(showget, showset)

    wm.polycount_run = bpy.props.BoolProperty(default=False)

# removal of properties when script is disabled
def clear_properties():
    props = ["polycount_run", "polycount_pos_x", "polycount_pos_y",
     "polycount_font_size", "polycount_font_color",
     "polycount_show_in_3d_view"]
    for p in props:
        if bpy.context.window_manager.get(p) != None:
            del bpy.context.window_manager[p]
        try:
            x = getattr(bpy.types.WindowManager, p)
            del x
        except:
            pass


class PolyCountOperator(bpy.types.Operator):
    bl_idname = "view3d.polycount"
    bl_label = "Polygon Count Display Tool"
    bl_description = "Display polygon count in the 3D-view"

    _handle = None
    #_timer = None

    visible_triangle_count = dict()
    selection_triangle_count = dict()
    #show = dict()

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        self.update_polycount(context)

        if not context.window_manager.polycount_run:
            # stop script
            view3dId = get_space_id(context.space_data)
            context.region.callback_remove(self._handle)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def cancel(self, context):
        if context.window_manager.polycount_run:
            context.region.callback_remove(self._handle)
            context.window_manager.polycount_run = False
        return {'CANCELLED'}

    #@classmethod
    #def poll(cls, context):
    #    print("poll")
    #    
    #    cls.update_polycount(context)
    #    
    #    return context.active_object is not None

    def update_polycount(self, context):
        select_tris = 0
        visible_tris = 0
        select_tris_edit = 0 

        for object in context.selected_objects:
            if (object.type == 'MESH'):
                select_tris += get_triangle_count(object)

        for object in context.visible_objects:
            if (object.type == 'MESH'):
                visible_tris += get_triangle_count(object)
               
        for object in context.selected_objects:
            if (object.type =='MESH'):
                select_tris_edit += get_triangle_count_edit(object)
                
        sc = context.scene

        view3dId = get_space_id(context.space_data)

        PolyCountOperator.visible_triangle_count[view3dId] = visible_tris
        PolyCountOperator.selection_triangle_count[view3dId] = select_tris_edit


    #def execute(self, context):
    #    print("execute")
    #    return {'FINISHED'}

    def invoke(self, context, event):
        #print("invoke")

        if context.area.type == 'VIEW_3D':
            if context.window_manager.polycount_run == False:
                # operator is called for the first time, start everything
                print("initialized")
                context.window_manager.polycount_run = True
                context.window_manager.modal_handler_add(self)

                self._handle = context.region.callback_add(draw_callback_px,
                    (self, context), 'POST_PIXEL')

                return {'RUNNING_MODAL'}
            else:
                # operator is called again, stop displaying
                context.window_manager.polycount_run = False
                print("stopped")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "View3D not found, can't run operator")
            return {'CANCELLED'}

def get_display_location(context):
    scene = context.scene

    width = context.region.width
    height = context.region.height

    pos_x = scene.polycount_pos_x
    pos_y = height - scene.polycount_pos_y

    return(pos_x, pos_y)

def draw_callback_px(self, context):
    wm = context.window_manager
    sc = context.scene

    if not wm.polycount_run:
        return

    font_size  = sc.polycount_font_size
    pos_x, pos_y = get_display_location(context)

    # draw text in the 3d-view
    # ========================
    blf.size(0, sc.polycount_font_size, 72)
    r, g, b = sc.polycount_font_color
    bgl.glColor3f(r, g, b)

    view3dId = get_space_id(context.space_data)

    visible_tri_count = PolyCountOperator.visible_triangle_count.get(view3dId, -1)

    if visible_tri_count > -1:
        text = "All: " + format(visible_tri_count, 'd') + "triangles"
        text1height = blf.dimensions(0, text)[1]

        blf.position(0, pos_x, pos_y - text1height, 0)
        blf.draw(0, text)

    selection_tri_count = PolyCountOperator.selection_triangle_count.get(view3dId, -1);

    if selection_tri_count > 0:
        text = "Selection: " + format(selection_tri_count, ',d') + " triangles"
        text2height = blf.dimensions(0, text)[1]

        blf.position(0, pos_x, pos_y - text1height - text2height - 5, 0)
        blf.draw(0, text)

#
# a quad would convert to 2 triangles
# a 5-sided polygon would convert to 3 triangles
# a hexagon would convert to 4 triangles
# etc.
#
# so formula is:
#  triangle count = number of corners > 2 ? number of corners - 2 : 0
#

def get_triangle_count_edit(object):
    obj = bpy.context.active_object
    if obj.mode == 'OBJECT':
        sel_tris = 0
    else:
        bm = bmesh.from_edit_mesh(obj.data)
        sel_faces = [face for face in bm.faces if face.select]
        sel_tris = sum([len(sel_faces[i].verts)-2 for i in range(0,len(sel_faces))])
#    print(sel_tris)
    return sel_tris


def get_triangle_count(object):
    triangle_count = 0
    decimateIdx = -1

    for modifierIdx, modifier in enumerate(list(object.modifiers)):
        if modifier.type == 'DECIMATE' and modifier.show_viewport:
            triangle_count = modifier.face_coun
            decimateIdx = modifierIdx

    if decimateIdx == -1:
        for p in object.data.polygons:
            count = p.loop_total
            if count > 2:
                triangle_count += count - 2

    for modifierIdx, modifier in enumerate(list(object.modifiers)):
        if modifier.type == 'MIRROR' and modifier.show_viewport and modifierIdx > decimateIdx:
            if modifier.use_x:
                triangle_count *= 2
            if modifier.use_y:
                triangle_count *= 2
            if modifier.use_z:
                triangle_count *= 2

    return triangle_count

def get_vertex_count(object):
    return len(object.data.vertices)


classes = [PolyCountOperator, PolyCountPanel]


def register():
    init_properties()
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    clear_properties()


# Screen -> Area -> Space
def get_space_id(object):
    screenList = list(bpy.data.screens)
    for screenIdx, screen in enumerate(screenList):
        for areaIdx, area in enumerate(list(screen.areas)):
            for spaceIdx, space in enumerate(list(area.spaces)):
                if (space == object):
                    return str(screenIdx) + "." + str(areaIdx) + "." + str(spaceIdx)


if __name__ == "__main__":
    register()
