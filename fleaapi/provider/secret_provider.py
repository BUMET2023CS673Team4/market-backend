import logging

import toml
from django.conf import settings


class SecretProvider:
    """
    Singleton class for reading secret toml file. The file path is specified in settings.FLEA_SECRET_FILE.
    Usage example:
        `test_key = SecretProvider().get_secret('test', 'test_key')`
    """

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.__init__()
        return cls.__instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        secret_file = settings.FLEA_SECRET_FILE
        self.secret = {}
        self.logger.info(f"Reading secret file {secret_file}")
        try:
            with open(secret_file, "r") as f:
                self.secret = toml.load(f)
        except FileNotFoundError as e:
            self.logger.error(
                f"Secret file {secret_file} not found, set all secrets to None"
            )
        except (TypeError, toml.TomlDecodeError) as e:
            self.logger.error(f"Secret file {secret_file} is not a valid TOML file")
            raise e
        except Exception as e:
            self.logger.error(f"Failed to read secret file {secret_file}")
            raise e

    def get_secret(self, category, key, default=None):
        if category in self.secret:
            return self.secret.get(category).get(key, default)
        return default
