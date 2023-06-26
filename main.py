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

    # paths for loading objects and saving lidar scans
    data_path = config["data"]["object_folder"]
    save_path = config["data"]["save_folder"]
    
    # number of scans
    num_scans = config["scan_settings"]["num_scans"]

    # create save directory
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    
    # get all objects which should be scanned and save the filepaths
    obj_files = []
    obj_files.extend(glob.glob(data_path + "/*.obj"))
    obj_files.sort()

    # create scanner
    scanner = bpy.data.objects["Camera"]
    scanner.scan_type = 'tof'

    # translate and rotate scanner according to real setup (angles are transformed from deg to rad)
    scanner.location = config["scan_settings"]["scanner_location"]
    scanner_rotation = config['scan_settings']['scanner_rotation']
    for i, deg_value in enumerate(scanner_rotation):
        rad_value = (deg_value * pi) / 180
        scanner_rotation[i] = rad_value
    scanner.rotation_euler = scanner_rotation

    # remove the cube object which is placed within the scene per default
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select = True
    bpy.ops.object.delete()

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
                
            # conduct scan
            blensor.tof.scan_advanced(scanner, 
                                        max_distance=config['azure_kinect_settings']['max_scan_dist'],
                                        evd_file=file_save_path,
                                        add_blender_mesh=False,
                                        add_noisy_blender_mesh=False,
                                        tof_res_x= config['azure_kinect_settings']['x_res'],
                                        tof_res_y=config['azure_kinect_settings']['y_res'],
                                        lens_angle_w=config['azure_kinect_settings']['hor_fov'],
                                        lens_angle_h=config['azure_kinect_settings']['ver_fov'],
                                        flength=config['azure_kinect_settings']['focal_length'],
                                        evd_last_scan=False,
                                        noise_mu=config['azure_kinect_settings']['noise_center'],
                                        noise_sigma=config['azure_kinect_settings']['noise_sigma'],
                                        timestamp = 0.0,
                                        backfolding=False
                                        )

            """
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
            """

    # quit blensor
    bpy.ops.wm.quit_blender()


if __name__ == "__main__":
    main()
