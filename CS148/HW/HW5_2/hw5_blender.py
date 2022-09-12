import bpy #blender python functions
import numpy as np
import json
#You may want to refer to: https://docs.blender.org/api/current/info_tips_and_tricks.html

import os

"""TODO0: 
    Change HW5_DIR to point to your HW5 directory, 
    then run this script with the play button above.
    take a look at run_main() at the bottom, and figure out 
    what the sample_function() is doing.
    you can run this script a couple of times!
"""
HW5_DIR="my_cs148_dir/HW5" 

def sample_function():
    #this function takes the object_pose object,
    #and modifies its coordinate frame,
    #by taking the z_component of the euler angle representation of rotation,
    # and adding 45 degrees
    frame = bpy.data.objects["frame_bunny"]       # selects the bunny coordinate frame
    z_angle_prev = frame.rotation_euler.z         # gets the current z component of the euler angle
    z_angle_next = z_angle_prev + 45*(np.pi/180)  # NOTE ROTATION IS RADIANS 
    frame.rotation_euler.z = z_angle_next
    print(f"The z-angle of the bunny went from {z_angle_prev*180/np.pi} to {z_angle_next*180/np.pi}")

def write_image(filename):
    # This function generates a render,
    # and sets the output render path to HW5_DIR/images/filename
    # Documentation at https://docs.blender.org/api/current/bpy.ops.render.html
    bpy.context.view_layer.update() # get most updated version of the scene
    bpy.context.scene.render.filepath = f"{HW5_DIR}/images/{filename}" # set filepath
    bpy.ops.render.render(write_still=True)
    
def change_z_rotation(object_name, z_angle_degrees):
    """TODO1
    write a function that takes in the name of an object 
    (ex. "frame_bunny", "frame_light", "ground_plane")
    and sets the z component of the corresponding object's 
    euler angle to [z_angle_degrees] degrees.
    HINT: this will be very similar to sample_function()!
    """    
    # TODO1 START
    pass
    # TODO1 END


def generate_renders(file_prefix, n_light_rotations, n_bunny_rotations):
    """
    TODO2.1
    write out M * N renders, with M rotations for the light and N rotations for the bunny.
    the rotations for both are evenly spaced between 0 and 180 degrees.
    
    each render is written in the format '{prefix}_{i}_{j}.png' corresponding to 
    the i-th z-angle rotation for the light and the j-th z-angle rotation for the bunny.
    
    For example, 
    generate_renders('todo2', 3, 5) would write out 15 renders.
    'todo2_1_1.png' would have light z-angle rotation= 0 degrees, bunny z-angle rotation = 0 degrees
    'todo2_2_2.png' would have light z-angle rotation= 90 degrees, bunny z-angle rotation = 45 degrees
    'todo2_3_5.png' would have light z-angle rotation= 180 degrees, bunny z-angle rotation = 180 degrees
    
    TODO2.2
    write out a dictionary where the key of each item is the image filename, 
    and the value is another dictionary, with the light and bunny z-angle values 
    corresponding to that image. For example: the dictionary for 
    generate_renders('todo2', 3, 5) would look like
    {
    'todo2_1_1.png': {'z_light':0.0,   'z_bunny':0.0},
    'todo2_1_2.png': {'z_light':0.0,   'z_bunny':45.0},
    'todo2_1_3.png': {'z_light':0.0,   'z_bunny':90.0},
    ...
    }
    """
    # NOTE: you may edit this function however you see fit 
    # (don't have to limit yourself to within the TODO blocks)
    parameter_dict={}
    
    for i in range(n_light_rotations):
        for j in range(n_bunny_rotations):
            filename=f"{file_prefix}_{i+1}_{j+1}.png"
            
            # TODO2 START
            # (Hint: consider using change_z_rotation and write_image as helper functions!)
            # TODO2 END
            
            # TODO3 START
            # modify this code to have the correct angles corresponding to 
            # the rendered image at HW5_DIR/images/[filename]!
            parameter_dict[filename]={"z_light":0, "z_bunny":0} 
            # TODO3 END
            
    with open(f"{HW5_DIR}/{file_prefix}.json","w") as fp:
        json.dump(parameter_dict,fp)

def run_main():
    # TODO0: run this script repeatedly (either with play button or through script editor) 
    # and see how the bunny object's z rotation angle changes!
    print("Let's increment the z-angle rotation here!")
    sample_function()
    
    # TODO1: implement change_z_rotation above, then uncomment these lines
    #change_z_rotation("frame_light", 120.0) 
    #change_z_rotation("frame_bunny", 55.0)
    #write_image("todo1.png")
    
    
    # TODO2: implement generate_renders above, and uncomment the line
    # TODO3: rerun this function once you're done with the dictionary writing
    #generate_renders("todo2", 6, 7)
    
    # TODO4 -- move to the jupyter notebook!
    
    # TODO5 START
    #uncomment and change this to your own predictions from the notebook!
    #predictions={'predicted_z_light': 0, 'predicted_z_bunny': 0}
    #change_z_rotation("frame_light", predictions['predicted_z_light']) 
    #change_z_rotation("frame_bunny", predictions['predicted_z_bunny'])
    #write_image("todo5.png")
    # TODO5 END
    
    bpy.context.view_layer.update()  #updates the scene

if __name__=="__main__":
    run_main()