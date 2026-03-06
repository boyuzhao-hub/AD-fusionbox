# AD-fusionbox
An omnidirectional **Sensors - Vehicle Data Fusion Box** based on ROS2 Humble

## Hardwares
<table class="tg">
<tbody>
<tr>
<td class="tg-bold"><b>Vehicle</b></td>
<td class="tg-0pky">1 &times; Nissan LEAF MY2012</td>
<td class="tg-0pky">
<a href="https://docs.openvehicles.com/en/latest/components/vehicle_nissanleaf/docs/index.html" target="_blank">Nissan Leaf OpenVehicles</a>
</td>
</tr>
<tr>
<td class="tg-bold" rowspan="2"><b>Computers</b></td>
<td class="tg-0pky">1 &times; Jetson AGX Orin 64 GB</td>
<td class="tg-0pky">
<a href="https://developer.nvidia.com/embedded/learn/jetson-agx-orin-devkit-user-guide/index.html" target="_blank">Jetson AGX Orin Guide</a>
<br/>
<a href="./docs/hardware/Computer_Jetson_AGX_Orin_Module_Carrier_Board_Specification.pdf" target="_blank">Jetson AGX Orin Board Specifications</a>
</td>
</tr>
<tr>
<td class="tg-0pky">1 &times; ARK 2251</td>
<td class="tg-0pky">
<a href="./docs/hardware/Computer_ARK_2251_Datasheet.pdf">ARK2251 Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-bold" rowspan="4"><b>Sensors</b></td>
<td class="tg-0pky">4 &times; Continental SRR3-A Short Range Radar</td>
<td class="tg-0pky">
<a href="./docs/hardware/Sensor_SRR308_Datasheet.pdf">SRR308 Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-0pky">4 &times; ZED X Stereo Camera (with IMU)</td>
<td class="tg-0pky">
<a href="./docs/hardware/Sensor_ZED_X_Datasheet.pdf">ZED X Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-0pky">1 &times; Continental SC13S 6-DoF IMU</td>
<td class="tg-0pky">
<a href="./docs/hardware/Sensor_IMU_SC13S.pdf">SC13S Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-0pky">2 &times; RTK GNSS (Syslogic RMLA4AGX64-h202S)</td>
<td class="tg-0pky">
<a href="./docs/hardware/Sensor_GNSS_ accessing_GNSS_on_Syslogic_systems.pdf">Syslogic RMLA4AGX64 Datasheet</a>
</td>
</tr>
</tbody>
</table>

## Hardware Topology
![Hardware Topology](./docs/assets/hardware_topology.drawio.svg)

## Software Architecture
To be finalized.


## This Repository
- src: Source code    
  - msgs: All self-defined ```.msg```, ```.srv```, ```.action```.
  - drivers: Read and publish ROS2 Topic of ZED SDK, Radars, GNSS, etc data.
  - perception: Perception algorithm. Subscribe sensors data and execute object detection, object trajectory, snesor fusion, etc.
  - localizaiton: Localization algorithm. Subscribe IMU, GNSS, Visual Odometry, etc for accurate pose.
  - bringup: System start-up configurations, including ```.launch.py```, or ```.yaml``` etc.
  - offline: Offline ros2bag data analysis.

## Documents
- [Understand the DBC File](./docs/understand_dbc_file.md)
