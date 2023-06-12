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
    
    scanner_model = config["scan_settings"]["scanner"]
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
    scanner.location = config["scan_settings"]["scanner_location"]
    scanner.velodyne_model = scanner_model

    # for each object which should be scanned:
    for file_path in obj_files:

        # import object into the scene and place it in the center
        scan_object = bpy.ops.import_scene.obj(filepath=file_path)
        scan_object = bpy.context.selected_objects[0]
        scan_object.location = config["scan_settings"]["object_location"]
        
        # construct filename of lidar scan
        _, file = os.path.split(file_path)
        file_name, _ = file.split(".")
        file = file_name + ".pcd"

        # for each scan:
        for i in range(num_scans):            

            # construct path where the scan is saved
            file_save_path = os.path.join(save_path, file)

            # generate random rotation angles
            x_rot = random.randrange(0, 360)
            y_rot = random.randrange(0, 360)
            z_rot = random.randrange(0, 360)

            # rotate object randomly
            scan_object.rotation_euler[0] = x_rot
            scan_object.rotation_euler[1] = y_rot
            scan_object.rotation_euler[2] = z_rot
                
            # Scan the scene and save the results
            blensor.blendodyne.scan_advanced(scanner, rotation_speed = 10.0, 
                                                    simulation_fps=24, 
                                                    angle_resolution = 100, 
                                                    max_distance = 120,
                                                    evd_file= file_save_path,
                                                    noise_mu=0.0,
                                                    noise_sigma=0.03, 
                                                    start_angle = 0.0, 
                                                    end_angle = 360.0, 
                                                    evd_last_scan=False, 
                                                    add_blender_mesh = False, 
                                                    add_noisy_blender_mesh = False)
            
            # rename files because there are multiple scans
            bin_name_raw = save_path + "/" + file_name
            pcd_name_raw = save_path + "/" + file_name + "00000.pcd"
            pcd_name_noisy = save_path + "/" + file_name + "_noisy00000.pcd"

            scan_number = str(i).zfill(4)

            file_name_raw_conv = pcd_name_raw.replace("00000", scan_number)
            file_name_noisy_conv = pcd_name_noisy.replace("00000", scan_number)

            os.remove(bin_name_raw)
            os.rename(pcd_name_raw, file_name_raw_conv)
            os.rename(pcd_name_noisy, file_name_noisy_conv)

    # quit blensor
    bpy.ops.wm.quit_blender()


if __name__ == "__main__":
    main()
