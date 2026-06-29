from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Arranca el nodo publicador
        Node(
            package='arm_kinematics',
            executable='fk_publisher',
            name='fk_publisher_node'
        ),
        # Arranca el nodo suscriptor
        Node(
            package='arm_kinematics',
            executable='angle_listener',
            name='angle_listener_node'
        )
    ])