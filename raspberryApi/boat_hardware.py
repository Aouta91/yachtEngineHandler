import RPi.GPIO as GPIO
import logging
import os

from .config import JSONConfig
from .servo import Servo
from .motor_controller import MotorController as MotorController

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

    @property
    def leds(self):
        """
        Возвращает словарь с информацией о состоянии светодиодов вида
        {'led1': {'pin': ..., 'state': ...}, {'led2': {'pin': ..., 'state': ...}},..., {'ledN': ...}}, где
        N - количество используемых светодиодов
        'pin': номер пина светодиода из конфигурационного файла, int
        'state': состояние светодиода, True/False, bool
        :return: dict
        """
        leds_state = {}
        keys = list(self._leds.keys())
        for i in range(len(keys)):
            leds_state[f"led{i}"] = {'pin': keys[i], 'state': self._leds[keys[i]]}
        return leds_state

    def set_led(self, led_number: int, state_flag: bool):
        """
        Устанавливает габаритный светодиод led_number в положение state_flag.
        Пример: set_led(21, True) зажигает светодиод GPIO21.
        :param led_number: номер светодиода из конфигурационного файла
        :param state_flag: состояние светодиода, True - вкл, False - выкл
        """
        if led_number not in self._leds.keys():
            logger.warning(f'Wrong GPIO number for LED: {led_number}')
        else:
            GPIO.output(led_number, state_flag)
            self._leds[led_number] = state_flag

    @property
    def steering_wheel(self):
        """
        Возвращает словарь с текущим состоянием сервопривода с ключами 'pin', 'angle', где
        'pin': управляющий пин сервопривода, int
        'angle': положение сервопривода, град [-90, 90], int
        :return: dict
        """
        return self._servo.angle

    def set_steering_wheel(self, angle: int):
        """
        Устанавливает руль в положение angle
        :param angle: положение руля, град. [- 90, 90]
        """
        if -90 <= angle <= 90:
            self._servo.angle = angle
        else:
            logger.warning(f'Angle {angle} isn\'t belongs to range [-90, 90]. Setting angle to 0')
            self._servo.angle = 0

    @property
    def motors(self):
        """
        Возвращает словарь с информацией о состоянии моторов вида
        {'left' : {'pin' : ...,  'speed': ...}, 'right' : {'pin': ..., 'speed': ...}}, где
        'left', 'right': str - ключи в словаре для левого и правого двигателя соответсвтенно
        'pin': управляющий пин двигателя, int
        'speed': скорость двигателя в процентах, [0, 100], int
        :return: dict
        """
        return {'left': self._left_motor.speed, 'right': self._right_motor.speed}

    def set_speed(self, speed: int, type: str):
        """
        Устанавливает скорость двигателя яхты, прямой ход.
        :param speed: скорость движения яхты в процентах. 100% - максимальная скорость [0...100]
        :param type: тип мотора. может принимать значения ["right", "left"]
        """
        if speed < 0 or speed > 100:
            logger.warning(f'Speed {speed} isn\'t belongs to range [0, 100]')
            speed = max(0, min(100, speed))

        if type == "left":
            self._left_motor.speed = speed
        elif type == "right":
            self._right_motor.speed = speed
        else:
            logger.warning(f'Incorrect motor type:{type}. Type must be \"left\" or \"right\"')

    def __str__(self):
        """
        Возвращает строку текущего состояния яхты
        :return: str
        """
        result = "BoatHardware current state:\n"
        result += f"leds: {self.leds}\n"
        result += f"steering wheel: {self.steering_wheel}\n"
        result += f"motors: {self.motors}\n"
        return result
