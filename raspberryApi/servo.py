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
        self.set_angle(0)

    def set_angle(self, angle: int):
        """
        Функция, устанавливающая угол сервопривода
        :param angle: значение угла в градусах от -90 до 90
        """
        dc = (angle + 90) * (self._max_dc - self._min_dc) / 180 + self._min_dc
        self._pwm.ChangeDutyCycle(dc)
