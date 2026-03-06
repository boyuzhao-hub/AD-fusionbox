from abc import ABC, abstractmethod

class MessageParser(ABC):

    @abstractmethod
    def parse(self, message, timestamp)-> dict:
        pass

class RadarStringParser(MessageParser):

    def parse(self, message, timestamp) -> dict:
        """
        Parses a ROS 2 String message and returns a dictionary with the content and timestamp.

        :param message: The ROS 2 String message to parse.
        :param timestamp: The timestamp associated with the message.
        :return: A dictionary containing the parsed message content and timestamp.
        """

        raw_jason_str = message.data
        try:
            json_data = json.loads(raw_jason_str)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from message: {raw_jason_str}")
            return None

        
        flat_dict = {
            "timestamp": timestamp,
            "msg_id": parsed_data.get("id", None),
        }
        
        value_data = parsed_data.get("value", {})

        # id = 1546 stands for global radar object list, which contains the number of objects and their attributes
        # id = 1547 stands for radar object list, which contains the attributes of each object, such as position, velocity, etc.
        if flat_dict["msg_id"] == 1546: 
            flat_dict["type"] = "Header"
            flat_dict["Obj_NofObjects"] = value_data.get("Obj_NofObjects")

            if "ros_timestamp" in parsed_data:
                flat_dict["ros_sec"] = parsed_data["ros_timestamp"].get("sec")

        elif flat_dict["msg_id"] == 1547:
            flat_dict["type"] = "Object"
            flat_dict["Obj_ID"] = value_data.get("Obj_ID")
            flat_dict["Obj_DistLong"] = value_data.get("Obj_DistLong")
            flat_dict["Obj_Lat"] = value_data.get("Obj_Lat")
            flat_dict["Obj_VreLong "] = value_data.get("Obj_VreLong")
            flat_dict["Obj_VreLat"] = value_data.get("Obj_VreLat")


