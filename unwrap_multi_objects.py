### unwrapping rocks ###

import bpy

# get selection
rocks = bpy.context.selected_objects

# get the mesh objects in the selection

for rock in rocks:

	bpy.context.scene.objects.active = rock
	
	bpy.ops.object.transform_apply(location = True, rotation = True,scale = True)
	
	bpy.ops.object.origin_set(type)
	
	selected_idx = [i.index for i in bpy.context.object.data.vertices ]
	
	for idx in selected_idx:
	
		z_value = bpy.context.object.data.vertices[idx].co[2]
		
		if z_value < 0:
			bpy.context.active_object.data.vertices[idx].select = True
			
	bpy.ops.object.editmode_toggle()
	
	bpy.ops.mesh.select_mode(face, toggle)

	bpy.ops.mesh.select_more()
	
	
	bpy.ops.uv.unwrap(method = 'angle based')
	
	bpy.ops.mesh.select_all(action = 'INVERT')

	bpy.ops.mesh.select_more()
	
	bpy.ops.uv.unwrap()
	
	bpy.ops.mesh.select_all(action = toggle)
	
	bpy.ops.mesh.select_all(action - toggle)
	
	bpy.ops.uv.select_all (action = 'toggle')
	
	bpy.ops.uv.pack_islands(margin = 1)
	
	bpy.ops.uv.seams_from_islands(mark_seams = True)
	
	
	
	bpy.ops.object.editmode_toggle()
	
### unwrapping uvs ###

import bpy

sel = bpy.context.selected_objects

for obj in sel:
	bpy.context.scene.objects.active = obj
	obj_name = obj.name
	
	if bpy.data.objects[obj_name].type = obj
		print ('select mesh object')
	else:
		bpy.ops.object.editmode_toggle()
		bpy.ops.uv.unwrap()
		bpy.ops.object.editmode_toggle()
	
