import os
import argparse
import pandas as pd

from bag_reader import RosbagReader

def main():
    parser = argparse.ArgumentParser(description="Tool to export data from ROS 2 bag file to CSV format")
    parser.add_argument('--bag_path', required = True, help = "Path to the ROS 2 bag file")
    parser.add_argument('--output_dir', default = 'datasets/extracted_rosbag', help = "Directory to save the exported CSV files")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Initialize the RosbagReader
    print(f"Reading bag file from: {args.bag_path}")
    bag_reader = RosbagReader(args.bag_path)

    collected_data = defaultdict(list)

    for topic_name, parsed_data in bag_reader.read_message():
        if isinstance(parsed_data, dict):  # if dict, it means it has been parsed by a DBC parser
            collected_data[topic_name].append(parsed_data)

        else:                              # if not, which means the topic not does not come from CAN bus.
#            if hasattr(prsed_data, 'linear_acceleration'):
#               collected_data[topic_name].append({})
            pass                           # To be finished

    print(f"Exporting data to CSV files in directory: {args.output_dir}")

    if not collected_data:
        print("No valid data, please check configurtion file or recorded rosbag")

    for topic, data_list in collected_data.items():
        rename = topic.replace("/", "_").strip("_")  # Replace '/' with '_' and remove leading/trailing underscores
        csv_path = os.path.join(args.output_dir, f"{rename}.csv")

        df = pd.DataFrame(data_list)
        df.to_csv(csv_path, index=False)
        print(f"Exported {len(data_list)} records to {csv_path}")

    print(f"Data export completed to {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main()