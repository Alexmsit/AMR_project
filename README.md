# AMR Projekt: Blensor-Pipeline zur Generierung von Trainingsdaten für 6D-Pose-Estimation


## Setup

1. Download the modified Blensor App Image from [here](https://drive.google.com/file/d/1liuBE2CTji_6wocjWjEGQ2Uy11DPg7fL/view?usp=sharing) and place it inside the root directory of this repository.
2. Give permission to execute the AppImage with the command below. 
    ```
    chmod +x Blender-x86_64.AppImage
    ```
2. Place the object file inside the scan_objects folder. 
3. Modify the settings within the `config.yaml` as shown below.


<hr>

## Config

The config file `config.yaml` contains all settings regarding the scans itself and the data paths.
The settings need to be adapted to your system and real world setup as described below:

First the paths within the **data** section need to be adapted to your system.
Next the translation and rotation of the sensor, as well as the location of the object need to be configured within the **scan_settings** section.
These values should match the real world setup in which the system is used.
At last the number of scans needs to be configured.

The **azure_kinect_settings** section does not need to be modified, but provides information about the configuration of the sensor which could be useful for debugging.


**data**:
- object_folder: Absolute path to the folder which contains the object.
- save_folder: Absolute path to the folder where the scan files are saved.

**scan_settings**:
- scanner_location: List with the x, y and z position of the scanner in meter.
- scanner_rotation: List with the rotation of the scanner along the x, y and z axis in degree.
- object_location: List with the x, y and z position of the object in meter.
- num_scans: Int Number of scans which are conducted per object.

**azure_kinect_settings**
- x_res: Resolution of the sensor in x-direction in pixel.
- y_res: Resolution of the sensor in y-direction in pixel.
- hor_fov: Horizontal field of view in degree.
- ver_fov: Vertical field of view in degree.
- focal_length: Focal length of the sensor.
- max_scan_dist: Maximum distance which the scanner can see.
- noise_center: Expected value (mu) of the added noise.
- noise_sigma: Standard Deviation (sigma) of the added noise.

<hr>

## Usage

The command below starts Blensor and runs the `main.py` script.

```
./Blender-x86_64.AppImage -P main.py
```

The script scans the object folder and saves all paths to the object files which were found. Then the first object is placed into the Blensor scene and rotated randomly along all three axis. After rotation, the simulated lidar scan is conducted according to the settings within the config file. This process of rotation and scanning is repeated until the specified number of scans is reached, then the next object is placed into the scene for scanning.

The simulated lidar scans are saved in .pcd format within the pointcloud_files folder.


<hr>

## File Format

<p>For each scan the following two files are generated:</p>

    1. OBJNAME_XXXX.pcd          Contains the simulated lidar points without noise

    2. OBJNAME_noisy_XXXX.pcd    Contains the simulated lidar points with noise

Thereby OBJNAME stands for the name of the object and XXXX stands for the number of the scan.

Each file consists of one integer(N) and N*15 tuples which represent the laser echos. The file ends with an integer that has the value -1.

Each tuple contains the following data:

- timestamp (double)
- yaw (double)
- pitch (double)
- distance (double)
- noisy distance (double)
- x (double)
- y (double)
- z (double)
- noisy x (double)
- noisy y (double)
- noisy z (double)
- red (double)
- green (double)
- blue (double)
- object id (double)

