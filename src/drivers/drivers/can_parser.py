import os
import yaml
import cantools
from ament_index_python.packages import get_package_share_directory
from abc import ABC, abstractmethod


class BaseDBCParser(ABC):
    """
    A class to parse radar DBC files and extract message definitions according to the customized rules in ./bringup/config/rules.
    """

    def __init__(self, rule_yaml_name: str, device_model_key: str):
        """
        Initializes the BaseDbCParser with the path to the customized device rule and DBC file.

        :param rule_yaml_name: Name of the rule YAML file.
        :param device_model_key: Key for the device model in the rule YAML, include radar_srr308 and imu_sc13s.
        """

        bringup_dir = get_package_share_directory("bringup")
        rule_file = os.path.join(
            get_package_share_directory("bringup"),
            "config",
            "rules",
            rule_yaml_name
        )
        with open(rule_file, 'r') as f:
            self.config = yaml.safe_load(f)[device_model_key]

        dbc_path = os.path.join(bringup_dir, 'config', self.config['dbc_file'])
        self.dbc_file = cantools.database.load_file(dbc_path)

        self.target_rules = self.config['messages_to_extract']

    @abstractmethod
    def parse_msg(self, can_msg_id: int, can_data: bytes, timestamp: float) -> dict:
        """
        Parses a CAN message according to the customized rules.

        :param can_msg_id: The CAN message ID.
        :param can_data: The raw CAN data bytes.
        :param timestamp: The timestamp of the CAN message.
        :return: A dictionary containing the parsed message fields and their values.
        """
        pass


class RadarDBCParser(BaseDBCParser):
    """
    A class to parse radar DBC files and extract message definitions according to the customized rules in ./bringup/config/rules.
    """
    def __init__(self):
        super().__init__(rule_yaml_name = 'radar_extraction_rules.yaml', device_model_key = 'radar_srr308')


    def parse_msg(self, can_message_id: int, can_data: bytes, timestamp: float) -> dict:
        """
        Parses a CAN message according to the customized rules.

        :param can_msg_id: The CAN message ID.
        :param can_data: The raw CAN data bytes.
        :param timestamp: The timestamp of the CAN message.
        :return: A dictionary containing the parsed message fields and their values.
        """
        msg_definition = self.dbc_file.get_message_by_frame_id(can_message_id)
        msg_name = msg_definition.name

        # For multiple radars, identify different radar by the suffix of the id (_0, _1, _2, ..., _7)
        parts = msg_name.rsplit('_', 1)
        if len(parts) != 2:
            return "None"

        base_name, sensor_id_str = parts[0], parts[1]

        if base_name not in self.target_rules:
            return "Not in customized rules"

        decoded_all = self.dbc_file.decode_message(can_message_id, can_data)
        
        filtered_data = {
            "timestamp": timestamp,
            "sensor_id": int(sensor_id_str),
            'msg_type': base_name
        }

        for sig_name in self.target_rules[base_name]:
            filtered_data[sig_name] = decoded_all.get(sig_name,None)

        return filtered_data


## Test
if __name__ == "__main__":

    parser = RadarDBCParser()
    
    # Lookup data of Obj_1_General_2 
    # According to DBC, CAN ID of Obj_1_General_2 is 1579.
    mock_can_id = 1579
    
    # Makeup a random hexadecimal data with 8 bits in represent radar information.
    mock_can_data = bytes.fromhex('01 23 45 67 89 AB CD EF') 
    mock_timestamp = 176787321.05
    

    result = parser.parse_msg(mock_can_id, mock_can_data, mock_timestamp)
    
    print("\n--- Test - Radar - Test: The information from Radar is ---")
    import pprint
    pprint.pprint(result)