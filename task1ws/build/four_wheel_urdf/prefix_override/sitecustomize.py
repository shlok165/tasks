import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/slok/TASK/task1ws/install/four_wheel_urdf'
