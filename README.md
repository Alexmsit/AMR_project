# AMR Projekt: Blensor-Pipeline zur Generierung von Trainingsdaten für 6D-Pose-Estimation

## Info

This repository containes the code for the AMR semester project `Erzeugen einer Blensor-Pipeline zur Generierung von Trainingsdaten für 6D-Pose-Estimation`.
The goal of this project was to automate the generation of synthetic training data for 6d-pose-estimation using Blensor. Therefore the Azure Kinect DK was implemented in Blensor and a small pipeline was built to automate it.

<hr>

## Setup

1. Download the modified Blensor App Image and place it inside the root directory of this repository.
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


**data**
- object_folder: Absolute path to the folder which contains the object.
- save_folder: Absolute path to the folder where the scan files are saved.

**scan_settings**
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

The script scans the object folder for the object file, loads it and places it into the Blensor scene. The object is then rotated randomly along all three axis. After rotation, the simulated Azure Kinect Scan is conducted according to the settings within the config file. 

This process of rotation and scanning is repeated until the specified number of scans is reached, then Blensor should quit automatically.

The simulated Azure Kinect Pointcloud data is saved in .pcd format, while the corresponding Ground Truth Labels are saved in .txt format. For more information about the file format see the section below.


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

<hr>

## Modification of the AppImage

The Appimage which is used in this project is based on the [original Blensor Appimage](https://www.blensor.org/pages/downloads.html) and just contains a few more python modules.
For future works on this project it could be necessary to add more python modules.
The steps to achieve this are described below:


**1. Extract the Appimage**

First the Appimage needs to be extracted with the following command.
This command will generate a folder "squashfs-root" with the extracted Appimage data next to the original Appimage.

```
/PATH/TO/YOUR/Blender-x86_64.AppImage --appimage-extract
```

**2. Add python modules**

Next the python modules need to be placed inside the following folder within the extracted Appimage.

```
/PATH/TO/YOUR/squashfs-root/2.79/python/lib
```

**3. Rebuild the Appimage**

Lastly, the Appimage needs to be rebuild with the command below.
To execute the command the [appimagetool](https://github.com/AppImage/AppImageKit/releases) needs to be downloaded first.

```
./appimagetool-x86_64.AppImage -v /PATH/TO/YOUR/squashfs-root
```


