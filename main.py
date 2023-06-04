import os
import yaml 
import glob
import random

import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

import blensor


def main():

    # load config
    config = yaml.safe_load(open("./config.yaml", "r"))

    # get paths for loading objects and saving lidar scans
    data_path = config["data"]["object_folder"]
    save_path = config["data"]["save_folder"]
    
    num_scans = config["scan_settings"]["num_scans"]

    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    
    # get all objects which should be scanned and save the filepaths
    obj_files = []
    obj_files.extend(glob.glob(data_path + "/*.obj"))
    obj_files.sort()

    # remove the cube object which is placed within the scene per default
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select = True
    bpy.ops.object.delete()

    # create scanner object and move it away from the origin of the scene
    scanner = bpy.data.objects["Camera"]
    scanner.location = (5,0,0)

    # for each object which should be scanned:
    for file_path in obj_files:

        # import object which sould be scanned into the scene
        scan_object = bpy.ops.import_scene.obj(filepath=file_path)
        scan_object_ = bpy.context.selected_objects[0]

        # for each scan:
        for i in range(num_scans):

            # get file
            _, file = os.path.split(file_path)

            # get name and extension of file
            file_name, file_extension = file.split(".")

            # add running number to filename because there are multiple scans of the same object
            file_name = file_name + str(i).zfill(4)

            # reconstruct file with extension in pointcloud format
            file = file_name + ".pcd"

            # construct path where the scan is saved
            file_save_path = os.path.join(save_path, file)

            # generate random rotation angles
            x_rot = random.randrange(0, 360)
            y_rot = random.randrange(0, 360)
            z_rot = random.randrange(0, 360)

            # rotate object randomly
            scan_object_.rotation_euler[0] = x_rot
            scan_object_.rotation_euler[1] = y_rot
            scan_object_.rotation_euler[2] = z_rot
                
            # Scan the scene and save the results
            blensor.blendodyne.scan_advanced(scanner, rotation_speed = 10.0, 
                                            simulation_fps=24, angle_resolution = 0.1728, 
                                            max_distance = 120, evd_file= file_save_path,
                                            noise_mu=0.0, noise_sigma=0.03, start_angle = 0.0, 
                                            end_angle = 360.0, evd_last_scan=True, 
                                            add_blender_mesh = False, 
                                            add_noisy_blender_mesh = False)
            


    # quit blensor
    bpy.ops.wm.quit_blender()


if __name__ == "__main__":
    main()
