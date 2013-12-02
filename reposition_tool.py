import bpy

C = bpy.context
selection = C.selected_objects
active_object = C.active_object
selection.remove(active_object)
target_location = C.object.location.xyz
target_rotation = C.object.rotation_euler
saved_cursor_loc = bpy.context.scene.cursor_location.copy()

if active_object_mode = 'OBJECT':
  for obj in selection:
    C.scene.objects.active = obj
    C.objects.location.xyz = target_location
    C.object.rotation_euler = target_rotation
    
else:
  for obj in selection:
    C.scene.objects.active = obj
    
    bpy.ops.view3d.snap_cursor_to_active
    
    target_location = bpy.context.scene.cursor_location
    
    C.object.location.xyz = target_location
    C.object.rotation_euler = target_rotation
    
    
bpy.context.scene.cursor_location = saved_cursor_loc

