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

    builds_with_updated_options = []

    for settings, options, env_vars, build_requires, reference in builder.items:
         builds_with_options.append([settings, updated_options, env_vars, build_requires])
    
    builder.builds = builds_with_updated_options    
    
    builder.run()