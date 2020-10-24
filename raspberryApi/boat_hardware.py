import RPi.GPIO as GPIO
import time
import logging

from .config import JSONConfig
from .servo import Servo
from .motor_controller import Controller as MotorController

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
        'pin': 13,
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

        config = JSONConfig(default_config=config_periph) if config_path is None else JSONConfig(config_path=config_path)

        self._noseLedPin = config['led']['nose']
        GPIO.setup(self._noseLedPin, GPIO.OUT)

        self._tailLedPin = config['led']['tail']
        GPIO.setup(self._tailLedPin, GPIO.OUT)

        self._servo = Servo(config['servo']['pin'], config['servo']['min_dc'], config['servo']['max_dc'])

        self._motor = MotorController(config['esc']['pin'])

    def set_led(self, led_number: int, state_flag: bool):
        """
        Устанавливает габаритный светодиод led_number в положение state_flag.
        Пример: set_led(21, True) зажигает светодиод GPIO21.
        :param led_number: номер светодиода из конфигурационного файла
        :param state_flag: состояние светодиода, True - вкл, False - выкл
        """
        GPIO.output(led_number, state_flag)

    def set_steering_wheel(self, angle: int):
        """
        Устанавливает руль в положение angle
        :param angle: положение руля, град. (- 90, 90)
        """
        if -90 <= angle <= 90:
            self._servo.set_angle(angle)
        else:
            logging.warning(f'{angle} value isn\'t belongs to range [-90, 90]. Setting angle to 0')
            self._servo.set_angle(0)

    def set_speed(self, speed: float):
        """
        Устанавливает скорость двигателя яхты, а также прямой и обратный ход.
        Отрицательное значение скорости включает реверс
        :param speed: скорость движения яхты (-1.0, ... , 0.0, ..., 1,0)
        :return:
        """
        if -1.0 <= speed <= 1.0:
            self._motor.set_speed(speed)
        else:
            logging.warning(f'{speed} value isn\'t belongs to range [-1.0, 1.0]. Setting speed to 0.0')
            self._motor.set_speed(0.0)
