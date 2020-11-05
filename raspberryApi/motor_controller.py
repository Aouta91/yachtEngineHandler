import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Controller:
    def __init__(self, motor_pin: int, freq: int = 50):
        """
        Класс, предоставляющий интерфейс для управления бесколлекторным двигателем через ESC
        :param motor_pin: управляющий контакт ESC
        :param freq: частота PWM, Гц
        """
        GPIO.setmode(GPIO.BCM)
        self._pin = motor_pin

    def set_speed(self, speed: int):
        logger.info(f'setting motor speed to {speed} value')
