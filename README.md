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
</td>
</tr>
<tr>
<td class="tg-0pky">1 &times; ARK 2251</td>
<td class="tg-0pky">
<a href="https://www.advantech.com/en-us/products/ark-2000_series_embedded_box_pcs/ark-2251/mod_de661626-e644-4813-a0f0-be7f006923c1">ARK2251 Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-bold" rowspan="4"><b>Sensors</b></td>
<td class="tg-0pky">4 &times; Continental SRR3-A Short Range Radar</td>
<td class="tg-0pky">
<a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiM1Yjs94qTAxVGgv0HHbzaOP0QFnoECBAQAQ&url=https%3A%2F%2Fwww.freecon.co.kr%2F%3Fact%3Dcommon.download_goods%26fseq%3D587%26u%3Dmanual&usg=AOvVaw2fEY5i-01AC0OZ5UTRRtOW&opi=89978449">SRR308 Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-0pky">4 &times; ZED X Stereo Camera (with IMU)</td>
<td class="tg-0pky">
<a href="https://cdn.sanity.io/files/s18ewfw4/staging/ec78a504b36ab95d6620ac720ffa5feaa2e8948b.pdf/ZED%20X%20Datasheet%20v1.2.pdf">ZED X Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-0pky">1 &times; Continental SC13S 6-DoF IMU</td>
<td class="tg-0pky">
<a href="https://www.continental-aftermarket.com/media/3746/continental_inertialsensor6dof_salessheet_v1.pdf">SC13S Datasheet</a>
</td>
</tr>
<tr>
<td class="tg-0pky">2 &times; RTK GNSS (Syslogic RMLA4AGX64-h202S)</td>
<td class="tg-0pky">
<a href="https://www.syslogic.com/jetson-agx-orin/rugged-edge-ai-computer-rpc-rml-a4agx">Syslogic RMLA4AGX64 Datasheet</a>
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
