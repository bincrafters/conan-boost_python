#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_boost_default

python_path = os.getenv("CONAN_BOOST_PYTHON_PATH", "")
args = "-o boost_python:python=" + python_path
    
if __name__ == "__main__":

    builder = build_template_boost_default.get_builder(args=args)

    builder.run()