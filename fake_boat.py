import subprocess
import unittest


class FakeBoat:

    def __init__(self):
        self._speed = 0
        self._angle = 0
        self._leds = [False, False]

    def set_speed(self, speed):
        assert type(speed) == int
        self._speed = speed
        self._say("Got speed " + str(self._speed))

    def get_speed(self):
        return self._speed

    def set_angle(self, angle):
        assert type(angle) == int
        self._angle = angle
        self._say("Got angle " + str(self._angle))

    def get_angle(self):
        return self._angle

    def set_led(self, state, idx):
        assert type(state) == bool
        assert type(idx) == int
        assert 0 <= idx < len(self._leds)
        self._leds[idx] = state
        self._say("Got led " + str(self._leds))

    def get_led(self, idx):
        assert type(idx) == int
        assert 0 <= idx < len(self._leds)
        return self._leds[idx]

    def __str__(self):
        return f"FakeBoat: <Speed: {self._speed}, Angle: {self._angle}, Leds: {self._leds}>"

    @staticmethod
    def _say(msg):
        print(subprocess.run(f"cowsay {msg}", shell=True))


class TestFakeBoat(unittest.TestCase):

    def test_interface(self):
        boat = FakeBoat()
        speed = 150
        boat.set_speed(speed)
        self.assertEqual(speed, boat.get_speed())
        angle = -60
        boat.set_angle(angle)
        self.assertEqual(angle, boat.get_angle())
        led1, led2 = True, False
        led1_idx, led2_idx = 0, 1
        boat.set_led(led1, led1_idx)
        boat.set_led(led2, led2_idx)
        self.assertEqual(led1, boat.get_led(led1_idx))
        self.assertEqual(led2, boat.get_led(led2_idx))

    def test_exceptions(self):
        def invalid_speed():
            boat = FakeBoat()
            boat.set_speed("asdas")

        def invalid_angle():
            boat = FakeBoat()
            boat.set_angle(False)

        def invalid_led():
            boat = FakeBoat()
            boat.set_led(True, 3)
        self.assertRaises(Exception, invalid_speed)
        self.assertRaises(Exception, invalid_angle)
        self.assertRaises(Exception, invalid_led)


if __name__ == "__main__":
    unittest.main()
