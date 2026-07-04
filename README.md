# ROS 2 5-DOF Robotic Arm Simulation & Kinematics

Un entorno de simulación completo y configuración cinemática para un brazo robótico de 5 Grados de Libertad (GDL), desarrollado de forma nativa en Ubuntu utilizando ROS 2 Humble.

## Descripción del Proyecto
Este proyecto demuestra la arquitectura de software completa para el control lógico de un manipulador robótico. Desde el diseño físico en formato XML hasta la planificación de trayectorias en RViz. El sistema fue depurado a nivel de controladores para permitir simulaciones aisladas de hardware mediante `FakeSystem` y `ros2_control`.

## Características Técnicas y Arquitectura
* **Modelado URDF/XACRO:** Creación del modelo físico del brazo, definiendo eslabones, articulaciones, propiedades de inercia y límites de colisión.
* **Integración MoveIt 2:** Configuración avanzada del Asistente de MoveIt para generar la Semántica del Robot (SRDF).
* **Cinemática Inversa y Planificación (OMPL):** Implementación de solucionadores de cinemática inversa y algoritmos de planificación de trayectorias en el espacio 3D.
* **Gestión de Hardware Simulado:** Resolución de conflictos de asignación aislando Gazebo y configurando un entorno puro de RViz apoyado por el framework `ros2_control`.

##  Stack Tecnológico
* **Framework:** ROS 2 (Humble)
* **OS:** Linux (Ubuntu)
* **Herramientas:** MoveIt 2, RViz, Colcon, XML, YAML.
