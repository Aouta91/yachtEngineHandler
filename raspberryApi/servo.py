import RPi.GPIO as GPIO


class Servo:
    def __init__(self, servoPin: int):
        """
        Класс, предоставляющий интерфейс для управления сервомотором
        :param servoPin: управляющий контакт сервопривода
        """
        GPIO.setmode(GPIO.BCM)
        self._pin = servoPin

        deg0Pulse = 0.5       # ms
        deg180Pulse = 2.5     # ms
        freq = 50.0           # 50 Hz
        period = 1000 / freq
        k = 100 / period
        self._deg0Duty = deg0Pulse * k
        pulseRange = deg180Pulse - deg0Pulse
        self._dutyRange = pulseRange * k

        GPIO.setup(self._pin, GPIO.OUT)
        self._pwm = GPIO.PWM(self._pin, freq)
        self._pwm.start(0)

    def setAngle(self, angle: int):
        """
        Функция, устанавливающая угол сервопривода
        :param angle: значение угла в градусах от 0 до 180
        """
        # TODO: придумать как ограничить диапазон углов от 0 до 180
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        duty = self._deg0Duty + (angle / 180) * self._dutyRange
        # print(f'duty: {duty}')
        self._pwm.ChangeDutyCycle(duty)


if __name__ == '__main__':
    print('запустите скрпит main.py для работы с яхтой')
