import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    pkg_bringup = get_package_share_directory('bringup')
    zed_wrapper_launch_path = os.path.join(
        get_package_share_directory('zed_wrapper'), 'launch', 'zed_camera.launch.py')

    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bringup, 'launch', 'rsp_launch.py')
        )
    )

    # Device id is dependent on how the cameras are connected through GMSL2 interface. Adjust accordingly.
    cameras = [
        {'name': 'zed_front', 'link': 'zed_front_camera_link', 'id': 0},
        {'name': 'zed_rear',  'link': 'zed_rear_camera_link',  'id': 1},
        {'name': 'zed_left',  'link': 'zed_left_camera_link',  'id': 2},
        {'name': 'zed_right', 'link': 'zed_right_camera_link', 'id': 3},
    ]

    camera_instances = []
    for cam in cameras:
        camera_instances.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(zed_wrapper_launch_path),
                launch_arguments={
                    'camera_name': cam['name'],
                    'camera_model': 'zedx',
                    'base_frame': cam['link'], 
                    'device_id': str(cam['id']),
                    # 'publish_depth': 'false', 
                }.items()
            )
        )

    return LaunchDescription([
        rsp_launch,
        *camera_instances
    ])