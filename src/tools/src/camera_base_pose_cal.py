import math
import argparse

def calculate_camera_poses(args):
    front_dist = args.front_distance
    rear_dist = args.rear_distance
    left_dist = args.left_distance
    right_dist = args.right_distance
    height = args.height

    poses = {
        "zed_front": (front_dist, 0.0, height, 0.0, 0.0, 0.0),
        "zed_rear":  (-rear_dist, 0.0, height, 0.0, 0.0, math.pi),
        "zed_left":  (0.0, left_dist, height, 0.0, 0.0, math.pi / 2.0),
        "zed_right": (0.0, -right_dist, height, 0.0, 0.0, -math.pi / 2.0),
    }

    print("-" * 75)
    print(f"{'Camera Link Name':<20} | {'X':>7} | {'Y':>7} | {'Z':>7} | {'Roll':>7} | {'Pitch':>7} | {'Yaw(rad)':>8}")
    print("-" * 75)
    
    for name, pose in poses.items():
        print(f"{name:<20} | {pose[0]:7.3f} | {pose[1]:7.3f} | {pose[2]:7.3f} | {pose[3]:7.3f} | {pose[4]:7.3f} | {pose[5]:8.3f}")
    
    print("-" * 75)

def main():
    parser = argparse.ArgumentParser(description="ZED Camera Transform Pose Calculator")
    
    parser.add_argument('--front_distance', type=float, default=0.5, help='Front distance in meters (default: 0.5)')
    parser.add_argument('--rear_distance', type=float, default=0.5, help='Rear distance in meters (default: 0.5)')
    parser.add_argument('--left_distance', type=float, default=0.3, help='Left distance in meters (default: 0.3)')
    parser.add_argument('--right_distance', type=float, default=0.3, help='Right distance in meters (default: 0.3)')
    parser.add_argument('--height', type=float, default=0.1, help='Camera installation height in meters (default: 0.1)')
    
    args = parser.parse_args()
    calculate_camera_poses(args)

if __name__ == "__main__":
    main()