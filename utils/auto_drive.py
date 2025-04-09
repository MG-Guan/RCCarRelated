import math
import time

from steering_control import SteeringControl
from longitudinal_control import LongitudinalControl

FIXED_FORWARD_SPEED = 10.0  # units per second

class CarController:
    def __init__(self, car_kinematics_conf_path='car_kinematics.yaml', steering_conf_path='steering.yaml'):
        """
        self.longitudinal_control = LongitudinalControl()
        self.steering_control = SteeringControl()
        """
        self.longitudinal_control = LongitudinalControl(master=None, gui=False)
        self.steering_control = SteeringControl(car_kinematics_conf_path, steering_conf_path)

    def update_drive(self, gear: str, speed: float, steering_angle: float):
        """
        Update the car's drive speed and steering angle.
        
        Args:
            speed (float): The forward speed command.
            steering_angle (float): The steering command in degrees (0.0 means straight).
        """
        assert self.longitudinal_control.set_gear(gear)
        assert self.longitudinal_control.set_speed(speed) == speed # Make sure speed is set correctly
        self.steering_control.set_angle_degrees(steering_angle)

    def test_drive(self, gear: str, speeds, steering_angles, FPS=30):
        """
        Drives the car at a fixed forward speed.
        """
        assert len(speeds) == len(steering_angles), "Speeds and steering angles must have the same length"

        time_delay = 1.0 / FPS
        print("Starting auto drive...")
        try:
            for speed, steering_angle in zip(speeds, steering_angles):
                self.update_drive(gear, speed, steering_angle)
                time.sleep(time_delay)
        except KeyboardInterrupt:
            print("Auto drive stopped by the user.")

def main():
    controller = CarController('../conf/car_kinematics.yaml', '../conf/steering.yaml')

    speeds = [] 
    angles = []
    for i in range(100):
        speeds.append(FIXED_FORWARD_SPEED)
        angles.append(math.sin(i / 10) * 20)  # Example: sine wave steering angle
    print(angles)
