# something like this... 
# http://www.youtube.com/watch?feature=player_detailpage&v=XCTSoOE9_os

import bpy
import os

def main(self, context):

	path = bpy.context.scene.render.filepath
	#path = "/home/salapati/Desktop/"
	
	if os.path.exists(path) == False:
		self.report({'WARNING'}, " Select a valid path") 
		
	else:
		# get the selection of objects
		init_selection = [ obj for obj in bpy.context.selected_objects if obj.type in ['MESH']]
		repeated_BB = [ obj for obj in init_selection if '.0' in obj.name ] + [ obj for obj in init_selection if "_BB_" in obj.name ] 
		selection = [obj for obj in init_selection if obj not in repeated_BB]
		
		if len(selection) == 0:
			## print this to the info tab
			self.report( {'WARNING'}, "please select objects to export")
		else:    
			# deselect all the objects
			bpy.ops.object.select_all(action='TOGGLE')
			
			for obj in selection:
				# get the name of the object
				name = obj.name
				
				# make it selected
				bpy.context.scene.objects[name].select = True        
				# make it active
				bpy.context.scene.objects.active = bpy.data.objects[name]
		
				# set the origin to geomentry's center of mass
				bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
				
				# get the loc and rot        
				loc = list(bpy.context.active_object.location)
				rot = list(bpy.context.active_object.rotation_euler)
				
				# clear loc and rot
				bpy.ops.object.location_clear()
				bpy.ops.object.rotation_clear()
						
				# export the object 
				bpy.ops.export_scene.obj(filepath= path + "\\" + name + ".obj", check_existing=True, use_selection=True, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_normals=True, use_uvs=True, use_materials=False, use_triangles=True, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=False, axis_forward='Z', axis_up='Y', global_scale=1, path_mode='AUTO')
							
				# apply back the loc and rot
				bpy.context.active_object.location = loc
				bpy.context.active_object.rotation_euler = rot
			
			    # get the name of the image
				try:
					img = bpy.context.active_object.data.uv_textures[0].data.values()[0].image.name
					# save the texture 
					bpy.data.images[img].save_render(filepath = path + img)
				except IndexError:
					pass     	
	
				# deselect the object
				bpy.context.scene.objects[name].select = False
			
			for each in init_selection:
				each.select = True
		self.report({'INFO'}, " Exported " + str(len(selection)) + " assets")
						
class ObjMultiExport(bpy.types.Operator):
	""" export multiple objects in one go"""
	bl_idname = "export.multi_obj"
	bl_label = "Obj multi Export"
		
	def execute(self, context):
		main(self, context)
		return {'FINISHED'}
