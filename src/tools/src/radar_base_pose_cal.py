import math
import argparse

def calculate_radar_poses(args):
    
    front_yaw_deg = args.front_yaw_deg
    rear_yaw_deg = args.rear_yaw_deg
    height = args.height
    front_distance = args.front_distance
    rear_distance = args.rear_distance

    # --- Translation ---
    front_left_radar_x = front_distance * math.cos(math.radians(front_yaw_deg))
    front_left_radar_y = front_distance * math.sin(math.radians(front_yaw_deg))

    front_right_radar_x = front_distance * math.cos(math.radians(-front_yaw_deg))
    front_right_radar_y = front_distance * math.sin(math.radians(-front_yaw_deg))

    rear_left_radar_x = -rear_distance * math.cos(math.radians(rear_yaw_deg))
    rear_left_radar_y = rear_distance * math.sin(math.radians(rear_yaw_deg))

    rear_right_radar_x = -rear_distance * math.cos(math.radians(-rear_yaw_deg))
    rear_right_radar_y = rear_distance * math.sin(math.radians(-rear_yaw_deg))

    # --- Yaw (To radians) ---
    # front radars Yaw (facing forward)
    yaw_front_left = math.radians(front_yaw_deg)
    yaw_front_right = math.radians(-front_yaw_deg)
    # back radars Yaw (facing backward)
    yaw_rear_left = math.radians(180.0 - rear_yaw_deg)
    yaw_rear_right = math.radians(-180.0 + rear_yaw_deg)

    # --- Pitch (To radians) ---
    pitch_front = math.radians(args.front_pitch_deg)
    pitch_rear = math.radians(args.rear_pitch_deg)

    # --- Roll (To radians) ---
    roll_front = math.radians(args.front_roll_deg)
    roll_rear = math.radians(args.rear_roll_deg)


    poses = {
        "radar_front_left":  (front_left_radar_x, front_left_radar_y, height, yaw_front_left, pitch_front, roll_front),
        "radar_front_right": (front_right_radar_x, front_right_radar_y, height, yaw_front_right, pitch_front, roll_front),
        "radar_rear_left":   (rear_left_radar_x, rear_left_radar_y, height, yaw_rear_left, pitch_rear, roll_rear),
        "radar_rear_right":  (rear_right_radar_x, rear_right_radar_y, height, yaw_rear_right, pitch_rear, roll_rear),
    }

    print("-" * 65)
    print(f"{'Radar Position':<20} | {'X':>6} | {'Y':>6} | {'Z':>6} | {'Yaw':>6} | {'Pitch':>6} | {'Roll':>6}")
    print("-" * 65)
    
    for name, pose in poses.items():
        print(f"{name:<20} | {pose[0]:6.3f} | {pose[1]:6.3f} | {pose[2]:6.3f} | {pose[3]:6.3f} | {pose[4]:6.3f} | {pose[5]:6.3f}")
    
    print("-" * 65)


def main():
    parser = argparse.ArgumentParser(description="Radar Transform Pose Calculator Tool")
    
    # Define command-line input parameters and their default values
    parser.add_argument('--front_distance', type=float, default=0.5, help='Front distance in meters (default: 2.5)')
    parser.add_argument('--rear_distance', type=float, default=0.5, help='Rear distance in meters (default: 1.0)')
    parser.add_argument('--front_yaw_deg', type=float, default=45.0, help='Front yaw angle in degrees (default: 45.0)')
    parser.add_argument('--rear_yaw_deg', type=float, default=60.0, help='Rear yaw angle in degrees (default: 45.0)')
    parser.add_argument('--height', type=float, default=0.1, help='Radar height in meters (default: 0.5)')
    
    parser.add_argument('--front_pitch_deg', type=float, default=0.0, help='Front pitch angle in degrees (default: 0.0)')
    parser.add_argument('--rear_pitch_deg', type=float, default=0.0, help='Rear pitch angle in degrees (default: 0.0)')
    parser.add_argument('--front_roll_deg', type=float, default=0.0, help='Front roll angle in degrees (default: 0.0)')
    parser.add_argument('--rear_roll_deg', type=float, default=0.0, help='Rear roll angle in degrees (default: 0.0)')

    args = parser.parse_args()
    
    calculate_radar_poses(args)


if __name__ == "__main__":
    main()