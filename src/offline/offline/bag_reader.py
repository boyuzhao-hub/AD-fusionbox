import os
import yaml
from ament_index_python.packages import get_package_share_directory

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

from drivers.can_parser import RadarDBCParser

class RosbagReader:
    """
    A class to read ROS 2 bag files.
    """

    def __init__(self, bag_path: str, pipeline_yaml = 'data_pipeline.yaml', storage_id: str = 'sqlite3'):
        """
        Initializes the RosbagReader with the path to the bag file.

        :param bag_path: Path to the ROS 2 bag file.
        :param config_yaml: Path to the YAML configuration file, where topics to read are specified.
        :param storage_id: Storage Format.
        """
        if not os.path.exists(self.bag_path):
            raise FileNotFoundError(f"Bag file not found at path: {self.bag_path}")

        self.bag_path = bag_path

        try:
            bringup_dir = get_package_share_directory("bringup")
        except Exception as e:
            raise FileNotFoundError(f"Could not find 'bringup' package: {e}")

        pipeline_path = os.path.join(bringup_dir, "config", self.pipeline_yaml)
        if not os.path.exists(pipeline_path):
            raise FileNotFoundError(f"Configuration file not found at path: {pipeline_path}")
        with open(pipeline_path, 'r') as f:
            self.config = yaml.safe_load(f)['data_pipeline']

        ############## To be added more topics according to the sensors ##############
        ## Get the topic list to read
        self.target_topics = self.config['offline_read']['read_topics']
        ## Initialize the radar DBC parser
        self.radar_parser = RadarDBCParser()

        print(f"Initialized RosbagReader with bag file: {self.bag_path}")
        print(f"target topics: {self.target_topics}")

        self.reader = rosbag2_py.SequentialReader()

        storage_options = rosbag2_py.StorageOptions(uri=self.bag_path, storage_id=storage_id)
        converter_options = rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
        self.reader.open(storage_options, converter_options)

        type_map = self._get_topic_type_map()

        self.topics_msg_classes = {}
        for topic in self.target_topics:
            if topic in type_map:
                self.topics_msg_classes[topic] = get_message(type_map[topic])
            else:
                print(f"Warning: Topic {topic} not found in the bag file. It will be skipped.")

        storage_filter = rosbag2_py.StorageFilter(topics=list(self.topics_msg_classes.keys()))
        self.reader.set_filter(storage_filter)

        ########## Design a router that only the topic that need a dbc parser will be parsed, if it doesn't need a parser, just deserialize it. ###########
        self.parser_router = {
            "/can/radar_front/rx": RadarDBCParser(),
            "/can/radar_rear/rx": RadarDBCpARSER(),
        }
        #################################################################################

        ## To be finished: get topic type map and deserialize messages in read_message function

    def _get_topic_type_map(self) -> dict:
        """
        Retrieves a mapping of topic names to their message types from the bag file.
        """
        topic_types = self.reader.get_all_topics_and_types()
        return  {topic.name: topic.type for topic in topic_types}

    def read_message(self):
        """
        Reads messages from the specified topic(s) in the bag file.

        :return: A list of deserialized messages from the specified topics.
        """

        while self.reader.has_next():
            topic, data, timestamp = self.reader.read_next()

            msg_class = self.topic_msg_classes[topic]
            msg_obj = deserialize_message(data, msg_class)

            #### if the topic inside the router, which means it needs to be parsed by the DBC parser.
            if topic in self.parser_router:
                parser = self.parser_router[topic]

                can_id = msg_obj.id
                can_data = bytes(msg_obj.data)

                parsed_dict = parser.parse_msg(can_id, can_data, timestamp)

                if parsed_dict:
                    yield topic, parsed_dict, timestamp

            else:
                yield topic, msg_obj, timestamp