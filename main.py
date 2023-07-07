import os
import yaml 
import glob
import random
import shutil

import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

import blensor



def deg_to_rad(deg_angle):
    """
    This function converts an angle from degree to radiant.

    Arguments:
        - deg_angle: Angle in degree.
    
    Returns:
        - rad_angle: Angle in radiant.
    """

    rad_angle = (deg_angle * pi) / 180

    return rad_angle



def main():

    # load config
    config = yaml.safe_load(open('./config.yaml', 'r'))
    
    # get current working directory
    working_dir = os.getcwd()

    # construct paths for loading and saving data
    data_dir = os.path.join(working_dir, 'scan_objects')
    save_dir = os.path.join(working_dir, 'training_data')
    pointcloud_dir = os.path.join(save_dir, 'pointclouds')
    label_dir = os.path.join(save_dir, 'labels')

    # create folders for saving data if they do not exist
    os.makedirs(pointcloud_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)
    
    # number of scans which are conducted for the object
    num_scans = config['scan_settings']['num_scans']

    # load path to the object file
    obj_files = []
    obj_files.extend(glob.glob(data_dir + "/*.obj"))
    file_path = obj_files[0]

    # create scanner and configure it according to the azure kinect settings
    scanner = bpy.data.objects['Camera']
    scanner.scan_type = 'kinect'
    scanner.kinect_xres=config['azure_kinect_settings']['x_res']
    scanner.kinect_yres=config['azure_kinect_settings']['y_res']
    scanner.kinect_flength=config['azure_kinect_settings']['focal_length']
    scanner.kinect_max_dist=config['azure_kinect_settings']['max_scan_dist']
    scanner.kinect_min_dist=config['azure_kinect_settings']['min_scan_dist']
    scanner.kinect_inlier_distance=config['azure_kinect_settings']['inlier_distance']
    scanner.kinect_noise_mu=config['azure_kinect_settings']['noise_center']
    scanner.kinect_noise_sigma=config['azure_kinect_settings']['noise_sigma']
    scanner.kinect_noise_scale=config['azure_kinect_settings']['noise_scale']
    scanner.kinect_noise_smooth=config['azure_kinect_settings']['noise_smoothness']
    scanner.kinect_ref_dist=config['azure_kinect_settings']['reflectivity_distance']
    scanner.kinect_ref_limit=config['azure_kinect_settings']['reflectivity_limit']
    scanner.kinect_ref_slope=config['azure_kinect_settings']['reflectivity_slope']
    scanner.add_scan_mesh=False
    
    # translate and rotate scanner according to real setup (angles are transformed from deg to rad)
    scanner.location = config['scan_settings']['scanner_location']
    scanner_rotation = config['scan_settings']['scanner_rotation']
    for i, deg_value in enumerate(scanner_rotation):
        rad_value = deg_to_rad(deg_value)
        scanner_rotation[i] = rad_value
    scanner.rotation_euler = scanner_rotation

    # remove the cube object which is placed within the scene per default
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select = True
    bpy.ops.object.delete()

    # import object into the scene and place it in the center
    scan_object = bpy.ops.import_scene.obj(filepath=file_path)
    scan_object = bpy.context.selected_objects[0]
    
    # construct filename of kinect scan
    _, file = os.path.split(file_path)
    file_name, _ = file.split('.')
    file = file_name + '.pcd'

    # for each scan:
    for i in range(num_scans):            

        # construct path where the scan file is saved
        file_save_path = os.path.join(save_dir, file)

        # load object area
        object_area = config['scan_settings']['object_location_area']

        # get higher bound of area range
        x_trans_range_high = float(object_area[0])
        y_trans_range_high = float(object_area[1])
        z_trans_range_high = float(object_area[2])

        # get lower bound of area range
        x_trans_range_low = float(object_area[0]*-1)
        y_trans_range_low = float(object_area[1]*-1)
        z_trans_range_low = float(object_area[2]*-1)

        # generate random translation within object area
        x_trans = round(random.uniform(x_trans_range_low, x_trans_range_high), 3)
        y_trans = round(random.uniform(y_trans_range_low, y_trans_range_high), 3)
        z_trans = round(random.uniform(z_trans_range_low, z_trans_range_high), 3)

        # translate object
        scan_object.location[0] = x_trans
        scan_object.location[1] = y_trans
        scan_object.location[2] = z_trans

        # position of the object is converted from Blensor coordinate system to camera coordinate system
        x_trans_cam_to_object = round(scan_object.location[0] - scanner.location[0], 3)
        y_trans_cam_to_object = round(scan_object.location[1] - scanner.location[1], 3)
        z_trans_cam_to_object = round(scan_object.location[2] - scanner.location[2], 3)

        # generate random rotation
        x_rot_deg = random.randrange(0, 360)
        y_rot_deg = random.randrange(0, 360)
        z_rot_deg = random.randrange(0, 360)

        # convert random rotation angles from degree to radiant
        x_rot_rad = deg_to_rad(x_rot_deg)
        y_rot_rad = deg_to_rad(y_rot_deg)
        z_rot_rad = deg_to_rad(z_rot_deg)

        # rotate object
        scan_object.rotation_euler[0] = x_rot_rad
        scan_object.rotation_euler[1] = y_rot_rad
        scan_object.rotation_euler[2] = z_rot_rad
            
        # conduct scan
        blensor.kinect.scan_advanced(scanner,
                                     evd_file=file_save_path,
                                     evd_last_scan=False,
                                     timestamp=0.0
                                    )

        # rename files
        bin_name_raw = save_dir + '/' + file_name
        pcd_name_raw = save_dir + '/' + file_name + '00000.pcd'
        pcd_name_noisy = save_dir + '/' + file_name + '_noisy00000.pcd'

        scan_number = str(i).zfill(4)

        file_name_raw_conv = pcd_name_raw.replace('00000', scan_number)
        file_name_noisy_conv = pcd_name_noisy.replace('00000', scan_number)

        os.remove(bin_name_raw)
        os.rename(pcd_name_raw, file_name_raw_conv)
        os.rename(pcd_name_noisy, file_name_noisy_conv)

        # create label file
        label_name = file_name_raw_conv.replace('.pcd', '.txt')
        label_path = os.path.join(label_dir, label_name)
        with open(label_path, "w") as label_file:
            label_file.write(str(x_trans_cam_to_object))
            label_file.write("\n")
            label_file.write(str(y_trans_cam_to_object))
            label_file.write("\n")
            label_file.write(str(z_trans_cam_to_object))
            label_file.write("\n")
            label_file.write(str(x_rot_deg))
            label_file.write("\n")
            label_file.write(str(y_rot_deg))
            label_file.write("\n")
            label_file.write(str(z_rot_deg))

        # move pointcloud files into data folder and label files into label folder
        shutil.move(file_name_raw_conv, pointcloud_dir)
        shutil.move(file_name_noisy_conv, pointcloud_dir)
        shutil.move(label_name, label_dir)

    # quit blensor
    bpy.ops.wm.quit_blender()


if __name__ == '__main__':
    main()
