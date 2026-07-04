import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

class ArmStatePublisher(Node):
    def __init__(self):
        super().__init__('arm_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        
        # Corremos el bucle rápido a 50 Hz para que el movimiento se vea muy fluido
        self.timer = self.create_timer(0.02, self.timer_callback)
        
        # 1. LA RUTINA (Waypoints)
        # Cada fila es una pose exacta: [Base, Hombro, Codo, Muñeca_Pitch, Muñeca_Roll] (en radianes)
        self.waypoints = [
            [0.0, 0.0, 0.0, 0.0, 0.0],          # Punto 0: Posición de descanso (Home / Vertical)
            [1.57, 0.5, -0.8, 0.3, 0.0],        # Punto 1: Girar 90° a la izquierda y bajar a "escanear"
            [-1.57, 0.5, -0.8, 0.3, 0.0],       # Punto 2: Girar 180° a la derecha manteniendo la altura
            [0.0, 1.0, -1.5, 0.5, 0.0]          # Punto 3: Plegar el brazo hacia arriba de frente
        ]
        
        self.target_index = 0  # A qué punto nos dirigimos actualmente
        self.current_positions = [0.0, 0.0, 0.0, 0.0, 0.0] # Dónde estamos ahora
        self.speed = 0.015     # Velocidad a la que se mueven los motores por cada 'tic' del procesador
        
        self.get_logger().info('Iniciando rutina de exploración autónoma...')

    def timer_callback(self):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = [
            'base_yaw_joint', 
            'shoulder_pitch_joint', 
            'elbow_pitch_joint', 
            'wrist_pitch_joint', 
            'wrist_roll_joint'
        ]
        
        # Obtenemos la coordenada a la que queremos llegar
        target = self.waypoints[self.target_index]
        llegamos = True
        
        # 2. EL ALGORITMO DE INTERPOLACIÓN (El Cerebro)
        # Revisamos motor por motor si ya llegó a su destino
        for i in range(5):
            distancia = target[i] - self.current_positions[i]
            
            # Si el motor todavía está lejos de su objetivo (margen de error de 0.02 rad)
            if abs(distancia) > 0.02:
                llegamos = False
                # Da un paso hacia adelante o hacia atrás dependiendo de dónde está el objetivo
                if distancia > 0:
                    self.current_positions[i] += self.speed
                else:
                    self.current_positions[i] -= self.speed
            else:
                # Si ya está muy cerca, lo anclamos exactamente en el objetivo
                self.current_positions[i] = target[i]
                
        msg.position = self.current_positions
        self.publisher_.publish(msg)
        
        # 3. CAMBIO DE ESTADO
        # Si todos los motores llegaron a su destino, pasamos al siguiente Waypoint
        if llegamos:
            self.get_logger().info(f'¡Llegamos al Waypoint {self.target_index}!')
            self.target_index += 1
            
            # Si terminamos la lista, volvems a empezar el ciclo
            if self.target_index >= len(self.waypoints):
                self.target_index = 0

def main(args=None):
    rclpy.init(args=args)
    node = ArmStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()