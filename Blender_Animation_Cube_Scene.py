import bpy
import random
from math import radians


# TO RUN THE CODE JUST OPEN BLENDER AND SELECT THIS PYTHON SCRIPT IN THE SCRIPTING TAB AND RUN.

# Delete all objects in the scene

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
    
bpy.ops.outliner.orphans_purge()
bpy.ops.outliner.orphans_purge()
bpy.ops.outliner.orphans_purge()


# Variables

light_intensity = 10
spacing = 2.2 # Space between Cubes
number_Objects = 30 # Number of Cubes
orthographic_scale_cam = 22.0

# ----------------- Render Engine ----------------- 

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.render.resolution_y = 1920
bpy.context.scene.render.resolution_x = 1920
 
# ----------------- World Settings ----------------- 
bpy.ops.world.new()
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0


# -----------------  Creating Mterials ----------------- 

Red_Mat = bpy.data.materials.new(name = "Red_Mat")
Red_Mat.use_nodes= True
mat_nodes = Red_Mat.node_tree.nodes
mat_nodes["Principled BSDF"].inputs["Metallic"].default_value= 0.8
mat_nodes["Principled BSDF"].inputs["Base Color"].default_value=1.0,0.0,0.78254,1.0
mat_nodes["Principled BSDF"].inputs["Roughness"].default_value= 1.0


Blue_Mat = bpy.data.materials.new(name = "Blue_Mat")
Blue_Mat.use_nodes= True
mat_nodes = Blue_Mat.node_tree.nodes
mat_nodes["Principled BSDF"].inputs["Base Color"].default_value=0.032281 ,0.048876,1,1.0
mat_nodes["Principled BSDF"].inputs["Roughness"].default_value= 1.0

Yellow_Mat = bpy.data.materials.new(name = "Yellow_mat")
Yellow_Mat.use_nodes= True
mat_nodes = Yellow_Mat.node_tree.nodes
mat_nodes["Principled BSDF"].inputs["Base Color"].default_value=0.006542,0.9,0.452878,1.0
mat_nodes["Principled BSDF"].inputs["Roughness"].default_value= 1.0



# ----------------- Create Collections for cubes -----------------

collection = bpy.data.collections.new("Cubes")
bpy.context.scene.collection.children.link(collection)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]


# ----------------- Array of cubes with ramdoms scales in z axis and materials -----------------


for x in range (number_Objects):
    for y in range (number_Objects):    
        location = (x*spacing, y*spacing, random.random()*4)
        bpy.ops.mesh.primitive_cube_add(size= 2,location = location, scale =(1, 1, random.random() * 4))
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.08
        bpy.context.object.modifiers["Bevel"].segments = 4
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True




        # ----------------- Assing Materials -----------------
        
        item = bpy.context.object
        if  random.random() < 0.25:
                item.data.materials.append(bpy.data.materials["Blue_Mat"])
        
        if  random.random() < 0.50:
                item.data.materials.append(bpy.data.materials["Yellow_mat"])
                
        else:
                item.data.materials.append(bpy.data.materials["Red_Mat"])
         
   
             
# ----------------- Animation Cubes Scale, Rotation and offset ----------------- 
                               
cubes  = bpy.data.collections["Cubes"].objects
offset = 2
  
for i in cubes:
    i.scale = [0,0,0]
    i.keyframe_insert(data_path = "scale", frame = 1 + offset)
    i.rotation_euler[2] += radians(0)
    i.keyframe_insert(data_path = "rotation_euler", frame = 1 + offset)
    i.scale = [1,1,5]
    i.keyframe_insert(data_path = "scale", frame = 50 + offset)
    i.scale = [1,1,.5]
    i.keyframe_insert(data_path = "scale", frame = 70 + offset)
    i.scale = [1,1,1]
    i  .keyframe_insert(data_path = "scale", frame = 80 + offset)
    offset += 1  
    i.rotation_euler[2] += radians(180)
    i.keyframe_insert(data_path = "rotation_euler", frame = 80 + offset)



# ----------------- Create Collections for Lights -----------------

collection = bpy.data.collections.new("Lights")
bpy.context.scene.collection.children.link(collection)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]


# ----------------- Create Lights -----------------

light_datas = bpy.data.lights.new("light", type = "SUN")
light = bpy.data.objects.new("light", light_datas)
bpy.context.collection.objects.link(light)
light.location = (25,10,30)
light.rotation_euler[1] += radians(45)
light.rotation_euler[2] += radians(20)
light_datas.energy = light_intensity

# ----------------- Create Cam -----------------

camera_data = bpy.data.cameras.new(name='Camera')
camera_object = bpy.data.objects.new('Camera', camera_data)
bpy.context.scene.collection.objects.link(camera_object)
camera_object.location = (-20,-35,30)
camera_object.rotation_euler =(25,0,10)
camera_data.type = 'ORTHO'
camera_data.ortho_scale = orthographic_scale_cam 


#----------------------Cam Keyframe Animation-------------------

camera_object.keyframe_insert(data_path="location",frame=0)
camera_object.location = (10,-35,30)
camera_object.keyframe_insert(data_path="location",frame=600)



# ----------------- Constrain (Track to) on Cam -----------------

bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', scale=(10, 10, 10))

target_obj = bpy.data.objects['Empty']

target_obj.location=(15, 35, 0)
target_obj.keyframe_insert(data_path="location",frame=0)

target_obj.location=(35, 38, 3)
target_obj.keyframe_insert(data_path="location",frame=600)
 
constraint = camera_object.constraints.new(type='TRACK_TO')
constraint.target = target_obj


 