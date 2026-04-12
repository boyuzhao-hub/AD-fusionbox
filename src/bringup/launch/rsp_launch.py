import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Find the path to the Xacro file
    xacro_file = os.path.join(get_package_share_directory('bringup'), 'urdf', 'nissan_leaf.urdf.xacro')

    # Process the Xacro file to get the robot description
    robot_description_config = xacro.process_file(xacro_file)
    params = {'robot_description': robot_description_config.toxml()}

    # Launch the robot_state_publisher node with the robot description
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return LaunchDescription([
        node_robot_state_publisher
    ])