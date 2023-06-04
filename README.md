# AMR Projekt: Blensor-Pipeline zur Generierung von Trainingsdaten für 6D-Pose-Estimation


## Setup

1. Download the modified Blensor App Image from [here](https://drive.google.com/file/d/1liuBE2CTji_6wocjWjEGQ2Uy11DPg7fL/view?usp=sharing) and place it inside the root directory of this repository.
2. Place one or more object files inside the `scan_objects` folder. 
2. Modify the datapaths and scan settings within `config.yaml`.


<hr>

## Usage

The command below starts Blensor and runs the `main.py` script.

The script first scans the object folder and saves all paths to the object files which were found. Then the first object is placed into the Blensor scene and rotated randomly along all three axis. After rotation, the simulated lidar scan is conducted according to the settings within the config file. This process of rotation and scanning is repeated until the specified number of scans is reached. The process is then also repeated for all other objects within the object folder.

The files are saved within the `pointcloud_files` folder.



```
./Blender-x86_64.AppImage -P main.py
```

<hr>

## File Format