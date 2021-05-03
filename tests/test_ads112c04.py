#!/usr/bin/env python

"""Tests for `ads112c04` package."""


import unittest
from click.testing import CliRunner

from ads112c04 import ads112c04
from ads112c04 import cli


class TestAds112c04(unittest.TestCase):
    """Tests for `ads112c04` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'ads112c04.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
