#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_boost_default

    
if __name__ == "__main__":

    updated_options = {
        "boost_python:python_version" : os.getenv("CONAN_BOOST_PYTHON_VERSION", None),
        "python_dev_config:python" : os.getenv("CONAN_PYTHON_PATH", "python"),
    }
    
    builder = build_template_boost_default.get_builder()
    
    builder.run()