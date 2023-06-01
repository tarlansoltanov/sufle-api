"""
Components module for Django Project Settings.

This module contains the settings that are common to all environments. The
settings are divided into several files, each of which contains a specific
category of settings.
"""

from pathlib import Path

from decouple import AutoConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent

# Loading `.env` files
# See docs: https://gitlab.com/mkleehammer/autoconfig
config = AutoConfig(search_path=BASE_DIR.joinpath('config'))
