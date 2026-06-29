import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class FKPublisher(Node):
    def __init__(self):
        super().__init__('fk_publisher_node')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        self.publisher_ = self.create_publisher(Float64, '/arm/joint_angle', qos_profile)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('Nodo FK Publisher iniciado. Transmitiendo...')

    def timer_callback(self):
        msg = Float64()
        msg.data = random.uniform(0.0, 3.14159)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {msg.data:.4f} rad')

def main(args=None):
    rclpy.init(args=args)
    node = FKPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()