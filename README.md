# AD-fusionbox
A sensors - vehicle data fusion box based on ROS2 Humble

## Hardwares
Computers - Heterogeneous computing
- Perception Layer: Jetson AGX Orin 64 GB
- Decision Layer: ARK 2251

Sensors:
- 4 $\times$ Continental SRR3-A Short Range Radar,
- 4 $\times$ ZED X Stereo Cameras,
- 1 $\times$ Continental SC13S 6-DoF IMU,
- 2 $\times$ RTK GNSS

Vechicle:
- Nissan LEAF MY2012

## This repo
- msgs: All self-defined ```.msg```, ```.srv```, ```.action```.
- drivers: Read and publish ROS2 Topic of ZED SDK, Radars, GNSS, etc data.
- perception: Perception algorithm. Subscribe sensors data and execute object detection, object trajectory, snesor fusion, etc.
- localizaiton: Localization algorithm. Subscribe IMU, GNSS, Visual Odometry, etc for accurate pose.
- bringup: System start-up configurations, including ```.launch.py```, or ```.yaml``` etc.
- offline: Offline ros2bag data analysis.

## Documents
- [Understand DBC File](src/bringup/config/understand_dbc_file.md)
