import RPi.GPIO as GPIO
import logging
import os

from .config import JSONConfig
from .servo import Servo
from .motor_controller import MotorController as MotorController

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

"""
default peripheral configuration
"""
config_periph = {
    'led': {
        'nose': 21,
        'tail': 20,
    },
    'servo': {
        'pin': 12,
        'freq_Hz': 50,
        'min_dc': 2.5,
        'max_dc': 10
    },
    'esc': {
        'left_motor_pin': 13,
        'right_motor_pin': 6,
        'freq_Hz': 50,
        'min_dc': 2.5,
        'max_dc': 10
    }
}


class BoatHardware:
    def __init__(self, config_path: str = None):
        """
        Класс, предоставляющий интерфейс для управления яхтой
        :param config_path: файл, содержащий параметры инициализации для яхты
        """
        GPIO.setmode(GPIO.BCM)

        config_path = config_path or os.path.join(os.path.abspath(os.getcwd()), 'config_periph.json')
        config = JSONConfig(config_path=config_path, default_config=config_periph)

        self._leds = {}
        for led_pin in config['led'].values():
            GPIO.setup(led_pin, GPIO.OUT)
            self._leds[led_pin] = False

        self._servo = Servo(config['servo']['pin'], config['servo']['min_dc'], config['servo']['max_dc'])

        self._left_motor = MotorController(config['esc']['left_motor_pin'])
        self._right_motor = MotorController(config['esc']['right_motor_pin'])

    def set_led(self, led_number: int, state_flag: bool):
        """
        Устанавливает габаритный светодиод led_number в положение state_flag.
        Пример: set_led(21, True) зажигает светодиод GPIO21.
        :param led_number: номер светодиода из конфигурационного файла
        :param state_flag: состояние светодиода, True - вкл, False - выкл
        """
        if led_number not in self._leds.keys():
            logger.warning(f'wrong GPIO number for LED: {led_number}')
        else:
            GPIO.output(led_number, state_flag)
            self._leds[led_number] = state_flag

    def led_status(self):
        """
        Возвращает словарь с информацией о состоянии светодиодов вида {led_pin : state}, где
        led_pin: int, номер пина светодиода из конфигурационного файла,
        state: bool, состояние светодиода, True/False
        :return: dict
        """
        return dict(self._leds)

    def set_steering_wheel(self, angle: int):
        """
        Устанавливает руль в положение angle
        :param angle: положение руля, град. [- 90, 90]
        """
        if -90 <= angle <= 90:
            self._servo.set_angle(angle)
        else:
            logger.warning(f'{angle} value isn\'t belongs to range [-90, 90]. Setting angle to 0')
            self._servo.set_angle(0)

    def steering_wheel_status(self):
        """
        Возвращает словарь с информацией о положении руля вида {pin : angle}, где
        pin: int, номер управляющего пина руля из конфигурационного файла,
        angle: int, положение руля [-90, 90]
        :return: dict
        """
        return self._servo.state()

    def set_speed(self, speed: int, type: str):
        """
        Устанавливает скорость двигателя яхты, прямой ход.
        :param speed: скорость движения яхты в процентах. 100% - максимальная скорость [0...100]
        :param type: тип мотора. может принимать значения ["right", "left"]
        """
        if speed < 0 or speed > 100:
            logger.warning(f'{speed} value isn\'t belongs to range [0, 100]. Setting speed to 0')
            speed = 0

        if type == "left":
            self._left_motor.set_speed(speed)
        elif type == "right":
            self._right_motor.set_speed(speed)
        else:
            logger.warning(f'Incorrect type:{type}. Type must be \"left\" or \"right\"')

    def motor_status(self):
        """
        Возвращает словарь с информацией о состоянии моторов вида {'left' : {pin : speed}, 'right' : {pin: speed}}, где
        'left', 'right': str - ключи в словаре для левого и правого двигателя соответсвтенно,
        pin: int - номер управляющего пина двигателя из конфигурационного файла,
        speed: int - скорость двигателя в условных единицах, [0, 100]
        :return: dict
        """
        return {'left': self._left_motor.state(), 'right': self._right_motor.state()}

    def __str__(self):
        """
        Возвращает строку текущего состояния яхты
        :return: str
        """
        result = "BoatHardware current state:\n"
        result += "leds: " + str(self.led_status()) + "\n"
        result += "steering wheel: " + str(self.steering_wheel_status()) + "\n"
        result += "motors: " + str(self.motor_status()) + "\n"
        return result
