from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Nodo de publicacion de estados, este no lo había guardado y no jalaba
        Node(
            package='arm_kinematics',
            executable='arm_state_publisher', 
            name='arm_state_publisher_node'
        ),
        # 2. publicar cinemática
        Node(
            package='arm_kinematics',
            executable='fk_publisher',
            name='fk_publisher_node'
        ),
        # 3. el listener de angulos
        Node(
            package='arm_kinematics',
            executable='angle_listener',
            name='angle_listener_node'
        )
    ])