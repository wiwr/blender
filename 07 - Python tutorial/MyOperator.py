import bpy
from math import radians
from bpy.props import *

class MyOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.my_operator"
    bl_label = "My Operator"
    bl_option = {'REGISTER', 'UNDO'}

    noice_scale : FloatProperty(
        name = "Noise Scale",
        description = "The scale of the noise",
        default = 1.0,
        min = 0.0,
        max = 2.0
    
    )
    
    def execute(self, context):
        
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

        # texture    
        mod_displace = so.modifiers.new("My Displacement", 'DISPLACE')
        new_text = bpy.data.textures.new("My Texture", 'DISTORTED_NOISE')
        new_text.noise_scale = self.noice_scale
        mod_displace.texture = new_text

        # material
        new_mat = bpy.data.materials.new(name = "My Material")
        so.data.materials.append(new_mat)
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes

        material_output = nodes.get("Material Output")
        node_emission = nodes.new(type='ShaderNodeEmission')

        node_emission.inputs[0].default_value = ( 0.0, 0.3, 1.0, 1 ) 
        node_emission.inputs[1].default_value = 500.0

        links = new_mat.node_tree.links
        new_link = links.new(node_emission.outputs[0], material_output.inputs[0])
                
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MyOperator.bl_idname, text=MyOperator.bl_label)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(MyOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MyOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.my_operator()
