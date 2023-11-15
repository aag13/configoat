#!/usr/bin/env python

"""Tests for `pyenvconfig` package."""

import pytest

# from click.testing import CliRunner

from pyenvconfig.pyenvconfig import PyEnvConfig
# from pyenvconfig.pyenvconfig import cli


# @pytest.fixture
# def response():
#     """Sample pytest fixture.
#
#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
#
#
# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string
#
#
# # def test_command_line_interface():
# #     """Test the CLI."""
# #     runner = CliRunner()
# #     result = runner.invoke(cli.main)
# #     assert result.exit_code == 0
# #     assert 'pyenvconfig.cli.main' in result.output
# #     help_result = runner.invoke(cli.main, ['--help'])
# #     assert help_result.exit_code == 0
# #     assert '--help  Show this message and exit.' in help_result.output
#
#
# def test__build_data_dict():
#     temp = PyEnvConfig()
#     temp.initialize(config="/home/hose2406101891a/Desktop/rrndd/pyenvconfig/tests/templates/main.yaml", env="dev")
#     assert temp.get("var1") == {'k':2,'Y':3}
#     print(type(temp.get('var1')))
#     assert temp.get("var2") == "var2 value"
