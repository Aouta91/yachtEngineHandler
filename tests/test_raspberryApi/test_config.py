import pytest
from raspberryApi import YAMLConfig, JSONConfig


def test_yaml():
    """Test YAMLConfig class
    """
    config = YAMLConfig(default_config={'test': 1})
    assert config['test'] == 1
    config['test'] = 2
    config.save('./tests/test_raspberryApi/raspberry_config.yaml')
    config_ = YAMLConfig('./tests/test_raspberryApi/raspberry_config.yaml')
    assert config_['test'] == 2


def test_json():
    """Test JSONConfig class
    """
    config = JSONConfig(default_config={'test': 1})
    assert config['test'] == 1
    config['test'] = 2
    config.save('./tests/test_raspberryApi/raspberry_config.json')
    config_ = JSONConfig('./tests/test_raspberryApi/raspberry_config.json')
    assert config_['test'] == 2
