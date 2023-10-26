import logging

import toml
from django.conf import settings


class SecretProvider(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            cls.instance.__init__()
        return cls.instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        secret_file = settings.FLEA_SECRET_FILE
        self.secret = {}
        self.logger.info(f"Reading secret file {secret_file}")
        try:
            with open(secret_file, "r") as f:
                self.secret = toml.load(f)
        except FileNotFoundError as e:
            self.logger.error(f"Secret file {secret_file} not found")
            raise e
        except (TypeError, toml.TomlDecodeError) as e:
            self.logger.error(f"Secret file {secret_file} is not a valid TOML file")
            raise e
        except Exception as e:
            self.logger.error(f"Failed to read secret file {secret_file}")
            raise e

    def get_secret(self, key, default=None):
        return self.secret.get(key, default)
