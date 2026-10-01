import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import serial


class DistanceNode(Node):

    def __init__(self):
        super().__init__('distance_node')

        self.publisher = self.create_publisher(Float32,'distance',10)
        self.serial_port = serial.Serial('/dev/ttyACM0',115200,timeout=1)
        self.timer = self.create_timer(0.1,self.read_distance)
        self.get_logger().info('ESP32 distance node started!')

    def read_distance(self):
        line = self.serial_port.readline().decode().strip()

        if line:
            try:
                distance = float(line)
                msg = Float32()
                msg.data = distance
                self.publisher.publish(msg)
            except ValueError:
                pass


def main(args=None):
    rclpy.init(args=args)
    node = DistanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()