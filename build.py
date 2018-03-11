#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_boost_default

args = ""
python_version = os.getenv("CONAN_BOOST_PYTHON_VERSION", None)
if python_version:
    args += " -o boost_python:python_version=" + python_version
python_path = os.getenv("CONAN_PYTHON_PATH", "python")
if python_path:
    args += " -o python_dev_config:python=" + python_path

if __name__ == "__main__":

    builder = build_template_boost_default.get_builder(args=args)

    builder.run()