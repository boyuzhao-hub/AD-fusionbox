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



    @abstractmethod
    def parse_frame(self, can_msg_id: int, can_data: bytes, timestamp: float) -> dict:
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
    def __init__(self, sensor_id: int = 0):
        super().__init__(rule_yaml_name = 'radar_extraction_rules.yaml', device_model_key = 'radar_srr308')
        self.sensor_id = sensor_id

        # For multiple radars, identify different radar by the suffix of the id (_0, _1, _2, ..., _7)
        # Create a set of valid CAN IDs based on the DBC file and the sensor ID suffix.
        self.valid_can_ids = set()
        self.suffix = f"_{self.sensor_id}"

        for msg in self.dbc_file.messages:
            if msg.name.endswith(self.suffix):
                self.valid_can_ids.add(msg.frame_id)
    


    def parse_frame(self, can_id: int, can_data: bytes, timestamp: float) -> dict:
        """
        Parses a CAN message according to the customized rules.

        :param can_id: The CAN message ID.
        :param can_data: The raw CAN data bytes.
        :param timestamp: The timestamp of the CAN message.
        :return: A dictionary containing the parsed message fields and their values.
        """

        if can_id not in self.valid_can_ids:
            return None

        try:
            raw_dict = self.dbc_file.decode_message(can_id, can_data)
            msg_name = self.dbc_file.get_message_by_frame_id(can_id).name

            normalized_dict = {}
            # Clean signal name, if the signal name ends with suffic, remove it, otherwise keep it.
            # The current radar srr308 dbc file does not have suffix in signal name, but we keep this logic here for future compatibility.
            for key, value in raw_dict.items():
                if key.endswith(self.suffix):
                    normalized_key = key[:-len(self.suffix)] // Remove the suffix to get the normalized key
                else:
                    cleaned_key = key

                normalized_dict[key] = value

            # Clean message name, if the message name ends with suffic, remove it, otherwise keep it.
            if msg_name.endswith(self.suffix):
                cleaned_msg_name = msg_name[:-len(self.suffix)]
            else:
                cleaned_msg_name = msg_name

            normalized_dict['msg_type'] = cleaned_msg_name
            normalized_dict['sensor_id'] = self.sensor_id
            normalized_dict['timestamp'] = timestamp
        msg_definition = self.dbc_file.get_message_by_frame_id(can_id)
        msg_name = msg_definition.name


        if msg_name not in self.target_rules:
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

    def encode_command(self, command_name: str, command_data: dict) -> (int, bytes):
        """
        Encodes a command into CAN message ID and data bytes according to the DBC file.

        :param command_name: The name of the command to encode.
        :param command_data: A dictionary containing the command fields and their values.
        :return: A tuple containing the CAN message ID and the encoded data bytes. (CAN_ID, CAN_DATA IN)
        """
        msg_definition = self.dbc_file.get_message_by_name(command_name)
        if not msg_definition:
            raise ValueError(f"Command '{command_name}' not found in DBC file.")

        can_msg_id = msg_definition.frame_id
        can_data = self.dbc_file.encode_message(command_name, command_data)

        return can_msg_id, can_data


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