import yaml
import os
import logging
import json
from typing import Any
from abc import ABC, abstractmethod


"""Default values of configuration
"""
DEFAULT_CONFIG = {
    'LEDs': {
        'nose_led': 21,
        'tail_led': 20
    },
    'servo_pin': 17
}


class RaspberryConfig(ABC):
    """RaspberryConfig base class
    """

    def __init__(self, config_path: str = None):
        """RaspberryConfig __init__ method.

        Args:
            config_path (str): path to configuration file. If not None then configuration will be loaded.

        """
        self._config: dict = DEFAULT_CONFIG.copy()
        if config_path is not None:
            self.load(config_path)

    def __getitem__(self, item: str) -> Any:
        """RaspberryConfig __getitem__ method.

        Args:
            item (str): key

        Returns:
            value (Any)

        """
        return self._config.get(item, None)

    def __setitem__(self, item: str, value: Any):
        """RaspberryConfig __setitem__ method.

        Args:
            item (str): key
            value (Any): value

        Returns:
            None

        """
        self._config[item] = value

    def __repr__(self) -> str:
        """RaspberryConfig __repr__ method.

        Prettify configuration dictionary to print.

        Returns:
            pretty string representation (str)

        """
        return json.dumps(self._config, sort_keys=False, indent=4)

    def load(self, config_path: str):
        """RaspberryConfig load method.

        Loads configuration from file 'config_path'.

        Args:
            config_path (str): path to configuration file.

        Returns:
            None

        """
        config_path = os.path.abspath(config_path)
        if os.path.isfile(config_path):
            try:
                with open(config_path, 'r') as f:
                    self._config: dict = self.load_dict(f)
                logging.info(f"Config file '{config_path}' was successfully loaded.\nConfiguration:\n{self}.")
            except OSError as e:
                logging.error(f"Can not load config file '{config_path}. {e}.")
            except Exception as e:
                logging.error(f"Can not load config file '{config_path}. {e}.")
        else:
            logging.warning(f"Can not load config file '{config_path}'. File does not exist. "
                            f"Creating config file with default configuration.")
            self.save(config_path)

    def save(self, config_path: str):
        """RaspberryConfig save method.

        Saves current configuration to file 'config_path'.

        Args:
            config_path (str): path to configuration file.

        Returns:
            None

        """
        config_path = os.path.abspath(config_path)
        config_dir, config_name = os.path.split(config_path)
        if not os.path.isdir(config_dir):
            try:
                os.makedirs(config_dir)
            except OSError as e:
                logging.error(f"Can not create config file directory '{config_dir}. {e}.")
        try:
            with open(config_path, 'w') as f:
                self.dump_dict(self._config, f)
            logging.info(f"Config file '{config_path}' was successfully saved.\nConfiguration:\n{self}.")
        except OSError as e:
            logging.error(f"Can not save config file '{config_path}. {e}.")
        except Exception as e:
            logging.error(f"Can not save config file '{config_path}. {e}.")

    @staticmethod
    @abstractmethod
    def dump_dict(d: dict, stream: Any):
        """RaspberryConfig abstract static dump_dict method.

        Dumps dictionary to stream (ex. file stream).
        Must be implemented in concrete child class.

        Args:
            d (dict): dictionary to dump.
            stream (Any): stream to dump to.

        Returns:
            None

        Raises:
            Exception

        """
        pass

    @staticmethod
    @abstractmethod
    def load_dict(stream: Any) -> dict:
        """RaspberryConfig abstract static load_dict method.

        Loads dictionary from stream (ex. file stream).
        Must be implemented in concrete child class.

        Args:
            stream (Any): stream to load from.

        Returns:
            d (dict) loaded from stream

        Raises:
            Exception

        """
        pass


class RaspberryJSONConfig(RaspberryConfig):
    """RaspberryJSONConfig class for JSON-file configurations
    """

    @staticmethod
    def dump_dict(d: dict, stream: Any):
        """RaspberryJSONConfig static dump_dict method implementation.

        Dumps dictionary to stream (ex. file stream) in JSON-format.

        Args:
            d (dict): dictionary to dump.
            stream (Any): stream to dump to.

        Returns:
            None

        Raises:
            Exception

        """
        json.dump(d, stream, sort_keys=False, indent=4)

    @staticmethod
    def load_dict(stream: Any) -> dict:
        """RaspberryJSONConfig static load_dict method implementation.

        Loads dictionary from stream (ex. file stream) in JSON-format.

        Args:
            stream (Any): stream to load from.

        Returns:
            d (dict) loaded from stream

        Raises:
            Exception

        """
        return json.load(stream)


class RaspberryYAMLConfig(RaspberryConfig):
    """RaspberryYAMLConfig class for YAML-file configurations
    """

    @staticmethod
    def dump_dict(d: dict, stream: Any):
        """RaspberryYAMLConfig static dump_dict method implementation.

        Dumps dictionary to stream (ex. file stream) in YAML-format.

        Args:
            d (dict): dictionary to dump.
            stream (Any): stream to dump to.

        Returns:
            None

        Raises:
            Exception

        """
        yaml.dump(d, stream, sort_keys=False)

    @staticmethod
    def load_dict(stream: Any) -> dict:
        """RaspberryYAMLConfig static load_dict method implementation.

        Loads dictionary from stream (ex. file stream) in YAML-format.

        Args:
            stream (Any): stream to load from.

        Returns:
            d (dict) loaded from stream

        Raises:
            Exception

        """
        return yaml.load(stream, Loader=yaml.FullLoader)


__all__ = ['RaspberryJSONConfig', 'RaspberryYAMLConfig']
