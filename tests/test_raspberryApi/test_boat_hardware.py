import pytest
from raspberryApi.boat_hardware import BoatHardware


def test_set_steering_wheel():
    yacht = BoatHardware()
    steering_wheel_status = yacht.steering_wheel_status
    pin = list(steering_wheel_status.keys())[0]
    assert steering_wheel_status[pin] == 0

    angle = 45
    yacht.set_steering_wheel(angle)
    steering_wheel_status = yacht.steering_wheel_status
    assert steering_wheel_status[pin] == angle


def test_set_led():
    yacht = BoatHardware()
    led_status = yacht.led_status
    pin = list(led_status.keys())[0]
    assert led_status[pin] is False

    yacht.set_led(pin, True)
    led_status = yacht.led_status
    assert led_status[pin] is True


def test_set_speed():
    yacht = BoatHardware()
    motor_status = yacht.motor_status
    pin = list(motor_status['right'].keys())[0]
    assert motor_status['right'][pin] == 0

    speed = 37
    yacht.set_speed(speed, 'right')
    motor_status = yacht.motor_status
    assert motor_status['right'][pin] == speed
