import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class BoatHardware:
    def __init__(self, config_path: str):
        """
        Класс, предоставляющий интерфейс для управления яхтой
        :param config_path: файл, содержащий параметры инициализации для яхты в формате .json
        """
        # TODO: parse hardware_configuration.json file and fill class members
        self._ledPin = 21
        GPIO.setup(self._ledPin, GPIO.OUT)

    def SetLed(self, led_number: int, state_flag: bool):
        """
        Устанавливает габаритный светодиод led_number в положение state_flag.
        Пример: SetLed(1, True) зажигает светодиод 1.
        :param led_number: номер светодиода (0..2)
        :param state_flag: состояние светодиода, True - вкл, False - выкл
        """
        if state_flag:
            GPIO.output(self._ledPin, GPIO.HIGH)
        else:
            GPIO.output(self._ledPin, GPIO.LOW)

    def SetSteeringWheel(self, grad: int):
        """
        Устанавливает руль в положение grad
        :param grad: положение руля, град. (- 90, 90)
        """
        pass

    def SetSpeed(self, speed: float):
        """
        Устанавливает скорость двигателя яхты, а также прямой и обратный ход.
        Отрицательное значение скорости включает реверс
        :param speed: скорость движения яхты (-1.0, ... , 0.0, ..., 1,0)
        :return:
        """
        pass


if __name__ == '__main__':
    # print('запустите скрпит main.py для работы с яхтой')
    yacht = BoatHardware("none")

    while True:
        yacht.SetLed(1, True)
        time.sleep(1)
        yacht.SetLed(1, False)
        time.sleep(1)