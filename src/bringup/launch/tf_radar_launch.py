import math
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    geometry_param_file = os.path.join(
        get_package_share_directory("bringup"),
        "param",
        "tf_radar_params.yaml"
    )

    with open(geometry_param_file, 'r') as f:
        geometry_params = yaml.safe_load(f)["radar_geometry"]

    alpha_deg = geometry_params['alpha_deg']
    beta_deg = geometry_params['beta_deg']
    height = geometry_params['height']
    front_distance = geometry_params['front_distance']
    rear_distance = geometry_params['rear_distance']

    # --- Translation ---
    front_left_radar_x = front_distance * math.cos(math.radians(alpha_deg))
    front_left_radar_y = front_distance * math.sin(math.radians(alpha_deg))

    front_right_radar_x = front_distance * math.cos(math.radians(-alpha_deg))
    front_right_radar_y = front_distance * math.sin(math.radians(-alpha_deg))

    rear_left_radar_x = -rear_distance * math.cos(math.radians(beta_deg))
    rear_left_radar_y = rear_distance * math.sin(math.radians(beta_deg))

    rear_right_radar_x = -rear_distance * math.cos(math.radians(-beta_deg))
    rear_right_radar_y = rear_distance * math.sin(math.radians(-beta_deg))

    # --- Yaw (transfer to radians) ---
    # front radars Yaw (facing forward)
    yaw_front_left = math.radians(alpha_deg)
    yaw_front_right = math.radians(-alpha_deg)
    # rear radars Yaw (facing backward)
    yaw_rear_left = math.radians(180.0 - beta_deg)
    yaw_rear_right = math.radians(-180.0 + beta_deg)

    return LaunchDescription([
        # front left radar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='radar_front_left_tf',
            arguments=[
                '--x', str(front_left_radar_x), 
                '--y', str(front_left_radar_y), 
                '--z', str(height),
                '--yaw', str(yaw_front_left), 
                '--pitch', '0', 
                '--roll', '0', 
                '--frame-id', 'base_link',
                '--child-frame-id', 'radar_front_left'
            ]
        ), 

        # front right radar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='radar_front_right_tf',
            arguments=[
                '--x', str(front_right_radar_x),
                '--y', str(front_right_radar_y),
                '--z', str(height),
                '--yaw', str(yaw_front_right),
                '--pitch', '0',
                '--roll', '0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'radar_front_right'
            ]
        ), 

        # rear left radar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='radar_rear_left_tf',
            arguments=[
                '--x', str(rear_left_radar_x),
                '--y', str(rear_left_radar_y),
                '--z', str(height),
                '--yaw', str(yaw_rear_left),
                '--pitch', '0',
                '--roll', '0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'radar_rear_left'
            ]
        ),

        # rear right radar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='radar_rear_right_tf',
            arguments=[
                '--x', str(rear_right_radar_x),
                '--y', str(rear_right_radar_y),
                '--z', str(height),
                '--yaw', str(yaw_rear_right),
                '--pitch', '0',
                '--roll', '0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'radar_rear_right'
            ]
        )
    ])