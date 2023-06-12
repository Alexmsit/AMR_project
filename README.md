# AMR Projekt: Blensor-Pipeline zur Generierung von Trainingsdaten für 6D-Pose-Estimation


## Setup

1. Download the modified Blensor App Image from [here](https://drive.google.com/file/d/1liuBE2CTji_6wocjWjEGQ2Uy11DPg7fL/view?usp=sharing) and place it inside the root directory of this repository.
2. Give permission to execute the AppImage with the command below. 
    ```
    chmod +x Blender-x86_64.AppImage
    ```
2. Place one or more object files inside the scan_objects folder. 
3. Modify the settings within the `config.yaml` as shown below.


<hr>


## Config

The config file `config.yaml` contains all settings regarding the scans itself and the data paths.
The structure of the config file with all possible settings is shown below.

**data**:
- object_folder: Absolute path to the folder which contains the objects.
- save_folder: Absolute path to the folder where the scan files are saved.

**scan_settings**:
- scanner: Name of the scanner which will be used, either "hdl64e2" or "hdl32e".
- num_scans: Number of scans which are conducted for a single object.

**custom_scan_settings**:
- use_custom: Either "True" or "False", determines if the custom scan settings will be used.
- rotation_speed: Speed of the rotation of the lidar scanner in Hz.
- simulation_fps: Speed of the simulation in FPS.
- angle_resolution: Angular (vertical) resolution of the scanner.
- max_distance: Maximum distance which the lidar scanner sees.
- noise_mu: Center of the noise.
- noise_sigma: Sigma of the noise.
- start_angle: Starting angle of the lidar scan.
- end_angle: Ending angle of the lidar scan.
- evd_last_scan: ?
- add_blender_mesh: ?
- add_noisy_blender_mesh: ?

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

