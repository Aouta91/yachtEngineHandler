import RPi.GPIO as GPIO


class Servo:
    def __init__(self, servo_pin: int, min_dc: float, max_dc: float, freq: int = 50):
        """
        Класс, предоставляющий интерфейс для управления сервомотором
        :param servo_pin: управляющий контакт сервопривода
        :param min_dc: минимальное значение duty cycle для PWM
        :param max_dc: максимальное значение duty cycle для PWM
        :param freq: частота PWM, Гц
        """
        GPIO.setmode(GPIO.BCM)
        self._pin = servo_pin
        self._min_dc = min_dc
        self._max_dc = max_dc

        GPIO.setup(self._pin, GPIO.OUT)
        self._pwm = GPIO.PWM(self._pin, freq)
        self._pwm.start(self._min_dc)
        self._angle = 0
        self.angle = self._angle

    @property
    def angle(self):
        """
        Возвращает словарь с текущим состоянием сервопривода с ключами 'pin', 'angle', где
        'pin': управляющий пин сервопривода, int
        'angle': положение сервопривода, град [-90, 90], int
        :return: dict
        """
        return {'pin': self._pin, 'angle': self._angle}

    @angle.setter
    def angle(self, angle: int):
        """
        Функция, устанавливающая угол сервопривода
        :param angle: значение угла в градусах от -90 до 90
        """
        self._angle = angle
        dc = (self._angle + 90) * (self._max_dc - self._min_dc) / 180 + self._min_dc
        self._pwm.ChangeDutyCycle(dc)
