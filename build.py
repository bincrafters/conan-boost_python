#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_boost_default

    
if __name__ == "__main__":

    args = []
    python_version = os.getenv("CONAN_BOOST_PYTHON_VERSION", None)
    python_path = os.getenv("CONAN_PYTHON_PATH", "python")
    
    if python_version:
        args.extend(["-o","boost_python:python_version=" + python_version])
    if python_path:
        args.extend(["-o","python_dev_config:python=" + python_path])
    
    builder = build_template_boost_default.get_builder(args=args)

    builder.run()