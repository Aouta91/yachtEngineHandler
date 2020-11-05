import RPi.GPIO as GPIO
import logging
import os

from .config import JSONConfig
from .servo import Servo
from .motor_controller import Controller as MotorController

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

        GPIO.setup(config['led']['nose'], GPIO.OUT)
        GPIO.setup(config['led']['tail'], GPIO.OUT)
        self._leds = {x: False for x in config['led'].values()}

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
        Возвращает словарь с информацией о состоянии светодиодов вида {led_number : state},
        где led_number : int - номер светодиода из конфигурационного файла,
        state : bool - состояние светодиода, True/False
        :return: {'led_number' : bool}
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

    def set_speed(self, speed: int, type: str):
        """
        Устанавливает скорость двигателя яхты, а также прямой и обратный ход.
        Отрицательное значение скорости включает реверс
        :param speed: скорость движения яхты [0...20]
        :param type: тип мотора. может принимать значения ["right", "left"]
        """
        if speed < 0 or speed > 20:
            logger.warning(f'{speed} value isn\'t belongs to range [0, 20]. Setting speed to 0')
            speed = 0

        if type == "left":
            self._left_motor.set_speed(speed)
        elif type == "right":
            self._right_motor.set_speed(speed)
        else:
            logger.warning(f'Incorrect type:{type}. Type must be \"left\" or \"right\"')
