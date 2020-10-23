import pytest
from raspberryApi import RaspberryYAMLConfig, RaspberryJSONConfig
import logging
import sys


def test_yaml():
    """Test RaspberryYAMLConfig class
    """
    config = RaspberryYAMLConfig()
    assert config['servo_pin'] == 17
    config['servo_pin'] = 18
    config.save('./tests/test_raspberryApi/raspberry_config.yaml')
    config_ = RaspberryYAMLConfig('./tests/test_raspberryApi/raspberry_config.yaml')
    assert config_['servo_pin'] == 18


def test_json():
    """Test RaspberryJSONConfig class
    """
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    config = RaspberryJSONConfig()
    assert config['servo_pin'] == 17
    config['servo_pin'] = 18
    config.save('./tests/test_raspberryApi/raspberry_config.json')
    config_ = RaspberryYAMLConfig('./tests/test_raspberryApi/raspberry_config.json')
    assert config_['servo_pin'] == 18
