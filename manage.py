#!/usr/bin/env python3

# Django code for Aprigi
# Description: The app for my April girl
# Copyright (C) 2016-present Anh Tranngoc
# This file is distributed under the same license as the aprigi package.
# Anh Tranngoc <naa@sfc.wide.ad.jp>, 2016.

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aprigi.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
