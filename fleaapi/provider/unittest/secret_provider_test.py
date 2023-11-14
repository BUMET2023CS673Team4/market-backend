import logging
from unittest.mock import MagicMock, mock_open, patch

import pytest
from django.test import Client, TestCase


class SecretProviderTest(TestCase):
    def test_get_existing_secret(self):
        with patch(
            'builtins.open', mock_open(read_data='[test]\ntest_key = "test_value"')
        ):
            from fleaapi.provider.secret_provider import SecretProvider

            secret_provider = SecretProvider()
            assert secret_provider.get_secret('test', 'test_key') == 'test_value'

    def test_get_non_existing_secret(self):
        with patch(
            'builtins.open', mock_open(read_data='[test]\ntest_key = "test_value"')
        ):
            from fleaapi.provider.secret_provider import SecretProvider

            secret_provider = SecretProvider()
            assert secret_provider.get_secret('test', 'test_key2') == None

    def test_get_non_existing_category(self):
        with patch(
            'builtins.open', mock_open(read_data='[test]\ntest_key = "test_value"')
        ):
            from fleaapi.provider.secret_provider import SecretProvider

            secret_provider = SecretProvider()
            assert secret_provider.get_secret('test2', 'test_key') == None

    def test_get_non_existing_secret_fallback(self):
        with patch(
            'builtins.open', mock_open(read_data='[test]\ntest_key = "test_value"')
        ):
            from fleaapi.provider.secret_provider import SecretProvider

            secret_provider = SecretProvider()
            assert (
                secret_provider.get_secret('test', 'test_key2', 'test_value2')
                == 'test_value2'
            )

    def test_get_non_existing_category_fallback(self):
        with patch(
            'builtins.open', mock_open(read_data='[test]\ntest_key = "test_value"')
        ):
            from fleaapi.provider.secret_provider import SecretProvider

            secret_provider = SecretProvider()
            assert (
                secret_provider.get_secret('test2', 'test_key', 'test_value2')
                == 'test_value2'
            )

    def test_get_non_existing_secret_file(self):
        logger = logging.getLogger('fleaapi.provider.secret_provider')
        with patch.object(logger, logger.error.__name__) as mock_logger_error:
            with patch(
                'builtins.open', mock_open(read_data='[test]\ntest_key = "test_value"')
            ) as m:
                m.side_effect = FileNotFoundError()
                from fleaapi.provider.secret_provider import SecretProvider

                SecretProvider()

                assert mock_logger_error.called

    def test_get_non_toml_secret_file(self):
        with patch(
            'builtins.open', mock_open(read_data='{"test":{"test_key":"test_value"}}')
        ) as m:
            import toml

            from fleaapi.provider.secret_provider import SecretProvider

            with pytest.raises(toml.TomlDecodeError):
                SecretProvider()
