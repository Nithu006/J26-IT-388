"""Configuration tests need no FastAPI or model dependencies."""
import importlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from backend.app import config


class ConfigurationTests(unittest.TestCase):
    def tearDown(self):
        importlib.reload(config)

    def test_safe_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            importlib.reload(config)
            self.assertFalse(config.TRUSTED_MODEL)
            self.assertEqual(config.MODEL_DIR, config.ROOT / 'ml/artifacts/models/exploratory_vectors')
            self.assertEqual(config.CORS_ORIGINS, ['http://127.0.0.1:5173', 'http://localhost:5173'])

    def test_relative_and_absolute_paths(self):
        self.assertEqual(config.model_directory(' models/demo '), config.ROOT / 'models/demo')
        absolute = config.ROOT / 'private-models'
        self.assertEqual(config.model_directory(str(absolute)), absolute)
        self.assertEqual(config.model_directory('  '), config.model_directory(None))

    def test_cors_whitespace_empty_and_duplicates(self):
        self.assertEqual(config.cors_origins(' http://localhost:5173, ,http://localhost:5173,https://example.test '),
                         ['http://localhost:5173', 'https://example.test'])
        self.assertEqual(config.cors_origins(' , '), [])

    def test_explicit_trust_only(self):
        for value, expected in [(' TRUE ', True), ('1', False), ('yes', False), ('', False)]:
            with self.subTest(value=value), patch.dict(os.environ, {'TRUSTED_MODEL': value}):
                importlib.reload(config)
                self.assertEqual(config.TRUSTED_MODEL, expected)
