import RPi.GPIO as GPIO
import json

GPIO.setmode(GPIO.BCM)


class BoatHardware:
    def __init__(self, config_path: str):
        """
        Класс, предоставляющий интерфейс для управления яхтой
        :param config_path: файл, содержащий параметры инициализации для яхты в формате .json
        """
        configData = None
        try:
            with open(config_path) as f:
                configData = json.load(f)
        except FileNotFoundError:
            configData = {'LEDs': {}}
            configData['LEDs'].update({'nose_led': 21})
            configData['LEDs'].update({'tail_led': 20})
            with open('raspberryApi/hardware_configuration.json', 'w') as f_out:
                json.dump(configData, f_out, indent=4)
                print(f'create file {f_out.name} with default configuration')

        self._noseLedPin = configData['LEDs']['nose_led']
        GPIO.setup(self._noseLedPin, GPIO.OUT)

    def SetLed(self, led_number: int, state_flag: bool):
        """
        Устанавливает габаритный светодиод led_number в положение state_flag.
        Пример: SetLed(1, True) зажигает светодиод 1.
        :param led_number: номер светодиода (0..2)
        :param state_flag: состояние светодиода, True - вкл, False - выкл
        """
        GPIO.output(self._noseLedPin, state_flag)

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
    print('запустите скрпит main.py для работы с яхтой')
