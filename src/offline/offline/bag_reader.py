import os
import yaml
from ament_index_python.packages import get_package_share_directory

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

class RosbagReader:
    """
    A class to read ROS 2 bag files.
    """

    def __init__(self, bag_path: str, config_yaml = 'offline_pipeline.yaml', storage_id: str = 'sqlite3'):
        """
        Initializes the RosbagReader with the path to the bag file.

        :param bag_path: Path to the ROS 2 bag file.
        :param config_yaml: Path to the YAML configuration file, where topics to read are specified.
        :param storage_id: Storage Format.
        """
        self.bag_path = bag_path
        if not os.path.exists(self.bag_path):
            raise FileNotFoundError(f"Bag file not found at path: {self.bag_path}")

        try:
            bringup_dir = get_package_share_directory("bringup")
        except Exception as e:
            raise FileNotFoundError(f"Could not find 'bringup' package: {e}")

        config_path = os.path.join(bringup_dir, "config", self.config_yaml)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at path: {config_path}")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['pipeline_config']

        self.target_topics = self.config['topics_to_read']
        print(f"Initialized RosbagReader with bag file: {self.bag_path}")
        print(f"target topics: {self.target_topics}")

        self.reader = rosbag2_py.SequentialReader()

        storage_options = rosbag2_py.StorageOptions(uri=self.bag_path, storage_id=storage_id)
        converter_options = rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')

        self.reader.open(storage_options, converter_options)

        ## To be finished: get topic type map and deserialize messages in read_message function

    def _get_topic_type_map(self) -> dict:
        """
        Retrieves a mapping of topic names to their message types from the bag file.
        """
        topic_types = self.reader.get_all_topics_and_types()
        return  {topic.name: topic.type for topic in topic_types}

    def read_message(self, target_topic: list):
        """
        Reads messages from the specified topic(s) in the bag file.

        :param target_topic: List of topic names to read messages from.
        :return: A list of deserialized messages from the specified topics.
        """
        storage_filter = rosbag2_py.StorageFilter(topics=target_topic)
        self.reader.set_filter(storage_filter)

        while self.reader.has_next():
            (topic_name, data, timestamp) = self.reader.read_next()

            type_str = self.topic_type_map[topic_name]
            msg_class = self._get_msg_class(type_str)
            msg = deserialize_message(data, msg_class) 

            yield topic_name, msg, timestamp
        return messages
    