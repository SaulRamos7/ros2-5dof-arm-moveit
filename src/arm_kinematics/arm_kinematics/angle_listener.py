import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class AngleListener(Node):
    def __init__(self):
        super().__init__('angle_listener_node')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        self.subscription = self.create_subscription(
            Float64,
            '/arm/joint_angle',
            self.listener_callback,
            qos_profile
        )
        self.get_logger().info('Nodo Listener iniciado. Esperando...')

    def listener_callback(self, msg):
        rad = msg.data
        deg = rad * (180.0 / math.pi)
        self.get_logger().info(f'Recibido: {rad:.4f} rad = {deg:.2f} grados')

def main(args=None):
    rclpy.init(args=args)
    node = AngleListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()