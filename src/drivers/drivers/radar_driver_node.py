from rclpy.node import Node
from can_msgs.msg import Frame
from msgs.msg import RadarObject, RadarObjectList

from drivers.can_parser import RadarDBCParser

class RadarDriverNode(Node):
    def __init__(self):
        super().__init__('radar_driver_node')

        self.get_logger().info("Radar Driver Node has been started.")

        self.parser = RadarDBCParser()
        self.get_logger().info("Radar DBC Parser has been initialized.")

        self.can_subscription = self.create_subscription(
            Frame,
            '/can_frames',
            self.can_callback,
            10
        )
        


    def can_callback(self, msg: Frame):
        parsed_data = self.parser.parse_msg(msg.id, msg.data, msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9)
        
        if isinstance(parsed_data, dict) and parsed_data.get('msg_type') == 'RADAR_OBJECT':
            radar_object = RadarObject()
            radar_object.timestamp = parsed_data['timestamp']
            radar_object.sensor_id = parsed_data['sensor_id']
            radar_object.object_id = parsed_data.get('object_id', -1)
            radar_object.distance = parsed_data.get('distance', -1.0)
            radar_object.velocity = parsed_data.get('velocity', -1.0)
            radar_object.angle = parsed_data.get('angle', -1.0)

            radar_object_list_msg = RadarObjectList()
            radar_object_list_msg.objects.append(radar_object)
            self.publisher.publish(radar_object_list_msg)