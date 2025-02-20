import os
import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Path to package
    pkg_dir = get_package_share_directory('four_wheel_urdf')
    
    # Paths to files
    default_xacro_path = os.path.join(pkg_dir, 'urdf', 'four_wheel.urdf.xacro')  # Changed from four_wheels to four_wheel
    default_rviz_path = os.path.join(pkg_dir, 'config', 'four_wheel.rviz')
    
    # Print path for debugging
    print(f"Looking for xacro file at: {default_xacro_path}")
    
    # Generate URDF from xacro
    robot_description_content = Command([
        'xacro ',
        default_xacro_path
    ])
    
    robot_description = {'robot_description': robot_description_content}

    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', default_rviz_path],
        output='screen'
    )

    return launch.LaunchDescription([
        DeclareLaunchArgument(
            name='gui',
            default_value='True',
            description='Flag to enable joint_state_publisher_gui'
        ),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])