import bpy
from math import radians
bpy.ops.mesh.primitive_cube_add()

so = bpy.context.active_object

so.location[0] = 5

so.rotation_euler[0] += radians(45)

mod_subsurf = so.modifiers.new("My Modifier", 'SUBSURF')
mod_subsurf.levels = 3
#bpy.ops.object.shade_smooth()
mesh = so.data
for face in mesh.polygons:
    face.use_smooth = True