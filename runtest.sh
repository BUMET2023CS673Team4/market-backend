#!/bin/bash
export DJANGO_SETTINGS_MODULE=fleasite.settings_debug
pytest --exitfirst $@