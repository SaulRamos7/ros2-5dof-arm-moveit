import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

#Importamos el formato estándar para servicios tipo "gatillo"
from std_srvs.srv import Trigger 

class FKPublisher(Node):
    def __init__(self):
        super().__init__('fk_publisher_node')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        #Tópico 
        self.publisher_ = self.create_publisher(Float64, '/arm/joint_angle', qos_profile)
        
        # servicio, creamos un servidor esperando llamadas en la línea '/arm/reset'
        self.srv = self.create_service(Trigger, '/arm/reset', self.reset_callback)
        
        # memoria interna guardamos el ángulo actual en la memoria RAM del nodo
        self.current_angle = 0.0 
        
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('Nodo FK Publisher iniciado con Servicio de Reset listo.')

    def timer_callback(self):
        # simulamos movimiento sumando un poquito al ángulo actual cada 0.5 seg
        self.current_angle += random.uniform(0.05, 0.2)
        
        msg = Float64()
        msg.data = self.current_angle
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {msg.data:.4f} rad')

    #  callback del servicio Esto SOLO se ejecuta cuando alguien hace la llamada
    def reset_callback(self, request, response):
        self.get_logger().info('¡PETICIÓN RECIBIDA! Interrumpiendo operación para resetear...')
        
        # Ejecutamos la tarea solicitada
        self.current_angle = 0.0
        
        # Llenamos el paquete de respuesta para que el cliente sepa que terminamos
        response.success = True
        response.message = "Operación exitosa: Ángulo regresado a 0.0 radianes"
        
        return response

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
