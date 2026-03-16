# AD-fusionbox
A heterogeneous, omnidirectional **Sensor - Vehicle Data Fusion Box** based on ROS 2 Humble

## Hardware
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

### Topology
![Hardware Topology](./docs/assets/Hardware_Topology.drawio.svg)

## Software Architecture
### Sequence Diagram
<!--[Sequence Diagram](./docs/assets/Software_Sequence_Diagram.drawio.svg) -->
To be finalized.


## Repository Structure
```text
├── src/
│   ├── bringup/                # System start-up configurations (launch files, parameters, etc)
│   ├── drivers/                # Hardware interfaces (ZED SDK, CAN parsers, GNSS, etc)
│   ├── localization/           # State estimation (IMU, GNSS, Visual Odometry, etc)
│   ├── perception/             # Perception and fusion algorithms (object detection, radar tracking, sensor fusion)
│   ├── offline/                # Tools and scripts for offline rosbag2 data analysis and evaluation
│   ├── msgs/                   # Custom ROS 2 interfaces (.msg, .srv, .action files)
│   └── zed-ros2-wrapper/       # Thirdy party ros2_wrapper from ZED.
├── docs/
│   ├── assets/                 # Images, architecture diagrams, and hardware topology charts
│   ├── datasheets/             # Official hardware manuals and specifications (ZED, Radar, IPC)
│   └── wiki/                   # Knowledge base, tutorials (e.g., DBC parsing, PTP setup) and API docs
└── README.md                   # Project overview and quick-start guide
```

## Tutorials & Knoledge Base
To help readers quickly understand basic concepts related to this topic, several detailed guides are provided for reference.
### Sensors
- [Understand the DBC File](./docs/wiki/understand_dbc_file.md)
- [How RTK GNSS Delivers Superior Performance](./docs/wiki/rtk_gnss.md)
### ROS 2
- [What is Serialization in ROS 2?](./docs/wiki/ros2_message_serialization.md)

## 🚀 Getting Started
### Prerequisites
* JetPack 6.2.2
* ROS 2 Humble
* CUDA 12.6
* Ubuntu 22.04 LTS

### Installation
To be finalized.

## Usage
* Connect the sensors and ensure PTP is synced between Jetson and ARK.
* Source the workspace: source install/setup.bash
* Launch the core system
  
To be finalized.