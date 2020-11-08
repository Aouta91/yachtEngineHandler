import pytest
from raspberryApi.boat_hardware import BoatHardware


def test_set_steering_wheel():
    yacht = BoatHardware()
    steering_wheel = yacht.steering_wheel
    assert steering_wheel['angle'] == 0

    angle = 45
    yacht.set_steering_wheel(angle)
    steering_wheel = yacht.steering_wheel
    assert steering_wheel['angle'] == angle


def test_set_led():
    yacht = BoatHardware()
    leds = yacht.leds
    assert leds['led1']['state'] is False

    yacht.set_led(leds['led1']['pin'], True)
    leds = yacht.leds
    assert leds['led1']['state'] is True


def test_set_speed():
    yacht = BoatHardware()
    motors = yacht.motors
    assert motors['right']['speed'] == 0

    speed = 37
    yacht.set_speed(speed, 'right')
    motors = yacht.motors
    assert motors['right']['speed'] == speed
