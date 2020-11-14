import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class MotorController:
    def __init__(self, motor_pin: int, freq: int = 50):
        """
        Класс, предоставляющий интерфейс для управления бесколлекторным двигателем через ESC
        :param motor_pin: управляющий контакт ESC
        :param freq: частота PWM, Гц
        """
        GPIO.setmode(GPIO.BCM)
        self._pin = motor_pin
        self._speed = 0

    @property
    def speed(self):
        """
        Возвращает словарь с текущим состоянием двигателя с ключами 'pin', 'speed', где
        'pin': управляющий пин двигателя, int
        'speed': скорость двигателя в процентах, [0, 100], int
        :return: dict
        """
        return {'pin': self._pin, 'speed': self._speed}

    @speed.setter
    def speed(self, speed: int):
        logger.info(f'setting motor speed to {speed} value')
        self._speed = speed
